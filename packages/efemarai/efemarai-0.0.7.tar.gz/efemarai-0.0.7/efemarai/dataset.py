import os
import zipfile

from time import sleep

import boto3
from appdirs import user_data_dir
from botocore.errorfactory import ClientError

from rich.console import Console
from rich.prompt import Confirm, Prompt

from efemarai.problem_type import ProblemType

console = Console()

class Dataset:
    @staticmethod
    def create(
        project,
        name,
        format,
        stage,
        data_url,
        annotations_url,
        credentials,
        upload,
        num_datapoints,
    ):
        if name is None or data_url is None or annotations_url is None:
            return None

        if format is not None:
            assert format in ("COCO",)
        else:
            format = "COCO"

        if stage is not None:
            assert stage in ("train", "validation", "test")
        else:
            stage = "test"

        session = project._session

        response = session._put(
            f"api/dataset/undefined/{project.id}",
            json={
                "name": name,
                "stage": stage,
                "data_url": data_url,
                "annotations_url": annotations_url,
                "access_token": credentials,
                "upload": upload,
                "projectId": project.id,
                "num_samples": num_datapoints,
            },
        )
        dataset_id = response["id"]

        if upload:
            endpoint = f"api/dataset/{dataset_id}/upload"
            session._upload(annotations_url, endpoint)
            session._upload(data_url, endpoint)
            session._post(endpoint, json={"num_samples": num_datapoints})

        return Dataset(
            project, dataset_id, name, format, stage, data_url, annotations_url
        )

    def __init__(self, project, id, name, format, stage, data_url, annotations_url):
        self.project = project
        self.id = id
        self.name = name
        self.format = format
        self.stage = stage
        self.data_url = data_url
        self.annotations_url = annotations_url

    def __repr__(self):
        res = f"{self.__module__}.{self.__class__.__name__}("
        res += f"\n  id={self.id}"
        res += f"\n  name={self.name}"
        res += f"\n  format={self.format}"
        res += f"\n  stage={self.stage}"
        res += f"\n  data_url={self.data_url}"
        res += f"\n  annotations_url={self.annotations_url}"
        res += f"\n)"
        return res

    def delete(self):
        self.project._session._delete(f"api/dataset/{self.id}/{self.project.id}")

    def download(
        self, num_samples=None, dataset_format=None, path=None, unzip=True, ignore_cache=False,
    ):
        if path is None:
            path = user_data_dir(appname="efemarai")

        path = os.path.join(path, self.id)

        if dataset_format is None:
            if self.project.problem_type == ProblemType.Classification:
                dataset_format = "imagenet"
            elif self.project.problem_type == ProblemType.ObjectDetection:
                dataset_format = "coco"
            elif self.project.problem_type == ProblemType.InstanceSegmentation:
                dataset_format = "coco"

        if dataset_format is None:
            console.print(":poop: Unsupported problem type.", style="red")
            return None

        if not ignore_cache:
            name = os.path.join(path, f"dataset_{dataset_format}")

            if num_samples:
                name += f"_{num_samples}"

            if os.path.exists(name):
                return name

            name += ".zip"
            if os.path.exists(name + ".zip"):
                return name

        access = self.project._session._post(
            "api/downloadDataset",
            json={
                "id": self.id,
                "format": dataset_format,
                "num_samples": num_samples,
                "async_download": True,
            },
        )

        s3 = boto3.client(
            "s3",
            aws_access_key_id=access["AccessKeyId"],
            aws_secret_access_key=access["SecretAccessKey"],
            aws_session_token=access["SessionToken"],
            endpoint_url=access["Url"],
        )

        with console.status(f"Preparing '{self.name}' dataset download"):
            while True:
                try:
                    response = s3.head_object(
                        Bucket=access["Bucket"], Key=access["ObjectKey"]
                    )
                    size = response["ContentLength"]
                    break
                except ClientError:
                    sleep(1)

        with self.project._session._progress_bar() as progress:
            task = progress.add_task(f"Downloading dataset ", total=float(size))
            callback = lambda num_bytes: progress.advance(task, num_bytes)

            os.makedirs(path, exist_ok=True)
            filename = os.path.join(path, os.path.basename(access["ObjectKey"]))

            s3.download_file(
                access["Bucket"], access["ObjectKey"], filename, Callback=callback
            )

        if unzip:
            with console.status(f"Unzipping dataset"):
                dirname = os.path.splitext(filename)[0]
                with zipfile.ZipFile(filename, "r") as f:
                    f.extractall(dirname)

                os.remove(filename)

                filename = dirname

        console.print(
            (f":heavy_check_mark: Downloaded '{self.name}' dataset to\n  {filename}"),
            style="green",
        )

        return filename
