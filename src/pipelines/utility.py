import os
from datetime import datetime

from kfp.dsl import ContainerOp
from kubernetes.client.models import V1EnvFromSource, V1SecretEnvSource


def setup_components(
    operator: ContainerOp,
    component_name: str,
    docker_image: str,
    env: str,
    cache_expiration: str = "P0D",
    memory_req: str = "4G",
    memory_lim: str = "4G",
    cpu_req: str = "2",
    cpu_lim: str = "2",
):
    operator.container.image = docker_image
    operator.container.add_env_from(V1EnvFromSource(secret_ref=V1SecretEnvSource(env)))
    operator.display_name = component_name
    operator.execution_options.caching_strategy.max_cache_staleness = cache_expiration
    operator.set_memory_request(memory_req)
    operator.set_memory_limit(memory_lim)
    operator.set_cpu_request(cpu_req)
    operator.set_cpu_limit(cpu_lim)
    return operator
