from typing import NamedTuple


def data_generation_op(
    config_gcs_path: str, experiment: str, parent_run_id: str
) -> NamedTuple("Outputs", [("run_id", str)]):
    import mlflow
    from mlflow import MlflowClient
    from mlflow.utils.mlflow_tags import MLFLOW_PARENT_RUN_ID, MLFLOW_RUN_NAME

    from caelum.config_parser import Config

    from src.common.constant import Path, Folder
    from src.common.utility import download_file, download_files, setup_folder

    from src.operators.data_generation.core import DataGenerator

    # Setup empty folder
    setup_folder()

    # Downloading config
    download_file(config_gcs_path, Path.CONFIG)

    # Load config
    config = Config(Path.CONFIG)

    # Downloading dependencies
    deps = config["dependencies"]
    deps = [
        (deps["query_train"], Path.QUERY_TRAIN),
        (deps["query_val"], Path.QUERY_VAL),
        (deps["query_test"], Path.QUERY_TEST),
    ]
    download_files(deps)

    client = MlflowClient()

    # Create mlflow run
    experiment_id = client.get_experiment_by_name(experiment).experiment_id
    run = client.create_run(
        experiment_id=experiment_id,
        tags={MLFLOW_PARENT_RUN_ID: parent_run_id, MLFLOW_RUN_NAME: "data_generation"},
    )

    # Run core functionality
    with mlflow.start_run(run_id=run.info.run_id):
        generator = DataGenerator(config)
        generator()

        # Logging artifacts
        mlflow.log_artifacts(Folder.DATA)

    return (run.info.run_id,)


# Driver code
if __name__ == "__main__":
    config_gcs_path = ...
    parent_run_id = ...
    experiment = ...
    
    data_generation_op(config_gcs_path, experiment, parent_run_id)