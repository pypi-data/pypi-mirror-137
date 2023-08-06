import docker

from roheboam.engine.integrations.docker.utils import stream_docker_logs


def run_docker_container(image, port="5000", gpus=None):
    client = docker.from_env()
    run_params = {"image": image, "ports": {"5000/tcp": str(port)}, "detach": True}
    if gpus is not None:
        run_params["runtime"] = "nvidia"
    container = client.containers.run(**run_params)
    return container
