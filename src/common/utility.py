import os
import mlflow
from mlflow import MlflowClient

from caelum.gcs_ops import Client

from src.common.constant import Folder
from src.common.logger import create_logger


logger = create_logger("workshop:utils")


def read_query_from_file(file_path: str, params={}):
    query_file = open(file_path, "r")
    query_raw = "".join(query_file.readlines())
    query = query_raw.format(**params)
    return query


def download_file(gcs_uri, dst):
    logger.info(f"downloading from {gcs_uri} to {dst}")
    path = gcs_uri.split("/")
    bucket = path[2]
    src = "/".join(path[3:])
    gcs = Client(bucket_name=bucket)
    gcs.download_file(src=src, dst=dst)


def download_files(dependencies):
    for gcs_uri, dst in dependencies:
        download_file(gcs_uri, dst)


def download_artifacts(run_id: str, dst_path: str):
    os.makedirs(dst_path, exist_ok=True)
    client = MlflowClient()
    artifacts = client.list_artifacts(run_id)
    for artifact in artifacts:
        mlflow.artifacts.download_artifacts(
            run_id=run_id, artifact_path=artifact.path, dst_path=dst_path
        )


def setup_folder():
    os.makedirs(Folder.RESOURCE, exist_ok=True)
    os.makedirs(Folder.DATA, exist_ok=True)


def callback_metrics(metrics):
    for key, value in metrics.items():
        mlflow.log_metric(key, value)


def callback_model(model):
    mlflow.sklearn.log_model(sk_model=model, artifact_path="model")


def callback_artifact(path):
    mlflow.log_artifacts(path)


def load_mlflow_model(run_id, model_path):
    return mlflow.sklearn.load_model(f"runs:/{run_id}/{model_path}")
