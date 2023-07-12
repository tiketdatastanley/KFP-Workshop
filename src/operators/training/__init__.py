from typing import NamedTuple


def training_op(
    parent_run_id: str, data_run_id: str, config_gcs_path: str, experiment: str
) -> NamedTuple("Outputs", [("run_id", str)]):
    import mlflow
    from mlflow import MlflowClient
    from mlflow.utils.mlflow_tags import MLFLOW_PARENT_RUN_ID, MLFLOW_RUN_NAME

    from caelum.config_parser import Config

    from src.common.constant import Path, Folder
    from src.common.utility import (
        download_file,
        download_artifacts,
        setup_folder,
        callback_metrics,
        callback_model,
    )

    from src.operators.training.core import Trainer

    # Setup empty folder
    setup_folder()

    # Downloading config
    download_file(config_gcs_path, Path.CONFIG)

    # Load config
    config = Config(Path.CONFIG)

    # Downloading dependencies
    download_artifacts(data_run_id, Folder.DATA)

    client = MlflowClient()

    # Create mlflow run
    experiment_id = client.get_experiment_by_name(experiment).experiment_id
    run = client.create_run(
        experiment_id=experiment_id,
        tags={MLFLOW_PARENT_RUN_ID: parent_run_id, MLFLOW_RUN_NAME: "training"},
    )

    # Run core functionality
    with mlflow.start_run(run_id=run.info.run_id):
        trainer = Trainer(config)
        trainer(callback_metrics=callback_metrics, callback_model=callback_model)

    return (run.info.run_id,)


# Driver code
if __name__ == "__main__":
    parent_run_id = ...
    data_run_id = ...
    config_gcs_path = ...
    experiment = ...
    
    training_op(
        parent_run_id,
        data_run_id,
        config_gcs_path,
        experiment
    )