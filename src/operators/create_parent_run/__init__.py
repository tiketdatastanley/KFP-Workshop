from typing import NamedTuple


def create_mlflow_parent_run_op(
    pod_name: str,
    run_name: str,
    experiment: str,
) -> NamedTuple("Outputs", [("run_id", str)]):
    import mlflow
    from mlflow import MlflowClient
    from mlflow.utils.mlflow_tags import MLFLOW_RUN_NAME

    client = MlflowClient()

    experiment_id = client.get_experiment_by_name(experiment).experiment_id
    run = client.create_run(
        experiment_id=experiment_id,
        tags={MLFLOW_RUN_NAME: run_name},
    )

    with mlflow.start_run(run_id=run.info.run_id):
        workflow_name = "-".join(pod_name.split("-")[:-1])
        mlflow.set_tag("kubeflow_workflow_name", workflow_name)

    return (run.info.run_id,)


# Driver code
if __name__ == "__main__":
    pod_name = ...
    run_name = ...
    experiment = ...
    
    create_mlflow_parent_run_op(pod_name, run_name, experiment)
