import os

from kfp.dsl import ContainerOp, pipeline
from kfp.compiler import Compiler
from kfp.components import create_component_from_func

from src.operators.create_parent_run import create_mlflow_parent_run_op
from src.operators.data_generation import data_generation_op
from src.operators.training import training_op
from src.operators.evaluation import evaluation_op

from .utility import setup_components


pipeline_name = "[WORKSHOP] Data Generation"


@pipeline(name=pipeline_name, description="Create model")
def pipeline(
    run_name: str,
    experiment: str,
    config_gcs_uri: str,
    secret_name: str,
    docker_image_tag: str,
):
    image = f"asia-docker.pkg.dev/tk-test-data/kubebuild/workshop/train_model:{docker_image_tag}"

    op_1 = create_component_from_func(create_mlflow_parent_run_op)(
        "{{pod.name}}", run_name, experiment
    )
    step_1 = setup_components(op_1, "Create Parent Run", image, secret_name)
    parent_run_id = step_1.outputs["run_id"]

    op_2 = create_component_from_func(data_generation_op)(
        config_gcs_uri, experiment, parent_run_id
    )
    step_2 = setup_components(op_2, "Data Generation", image, secret_name)
    data_generator_run_id = step_2.outputs["run_id"]
    step_2.after(step_1)


if __name__ == "__main__":
    pipeline_filename = f"data_generation.yml"

    Compiler().compile(
        pipeline_func=pipeline,
        package_path=os.path.join(".template", pipeline_filename),
    )
