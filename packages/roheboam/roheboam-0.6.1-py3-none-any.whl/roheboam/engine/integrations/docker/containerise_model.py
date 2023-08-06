import shutil
import sys
import tempfile
from pathlib import Path

import docker

from roheboam.engine.integrations.docker.utils import stream_docker_logs


def containerise_model(model_path, model_image, build_env_image="roheboam:latest", model_format="mlflow"):
    model_path = Path(model_path)
    if build_env_image == "roheboam:latest":
        docker_template = _create_roheboam_docker_template(model_path, model_format)
        image = _build_model_docker_image(docker_template, model_path, model_image)
        return image


def _create_roheboam_docker_template(model_path, model_format):
    major_version, minor_version, *_ = sys.version_info
    docker_template = ""
    docker_template += f"FROM python:{major_version}.{minor_version}\n"
    docker_template += f"""RUN apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get install \
    'ffmpeg'\
    'libsm6' \
    'libxext6' \
    'libvips-dev' -y\n
    """
    docker_template += f"RUN pip install roheboam\n"
    docker_template += f"RUN mkdir /model\n"
    docker_template += f"WORKDIR /model\n"
    docker_template += f"COPY {model_path.name} /model\n"
    docker_template += f'ENTRYPOINT ["roheboam"]\n'
    docker_template += f'CMD ["serve", "--model_path", "/model", "--model_format", "{model_format}"]'
    return docker_template


def _build_model_docker_image(docker_template, model_path, model_image_tag):
    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copytree(model_path, f"{temp_dir}/{model_path.name}")
        with (Path(temp_dir) / "Dockerfile").open("w") as f:
            f.write(docker_template)

        client = docker.from_env()
        image, log_generator = client.images.build(path=temp_dir, tag=model_image_tag)
        stream_docker_logs(log_generator)
        return image


def containerise_model_debug(source_path, model_path, model_image, model_format="mlflow"):
    docker_template = _create_roheboam_dev_docker_template(model_path, model_format)
    image = _build_model_dev_docker_image(source_path, docker_template, model_path, model_image)
    return image


def _create_roheboam_dev_docker_template(model_path, model_format):
    major_version, minor_version, *_ = sys.version_info
    docker_template = ""
    # docker_template += f"FROM python:{major_version}.{minor_version}\n"
    docker_template += f"""FROM nvcr.io/nvidia/pytorch:21.06-py3\n"""
    docker_template += f"""RUN apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get install \
    'ffmpeg'\
    'libsm6' \
    'libxext6' \
    'libvips-dev' -y\n
    """
    docker_template += f"RUN mkdir /build\n"
    docker_template += f"COPY roheboam /build\n"
    docker_template += f"WORKDIR /build\n"
    docker_template += f"RUN pip install -e .\n"
    docker_template += f"RUN mkdir /model\n"
    docker_template += f"WORKDIR /model\n"
    docker_template += f"COPY {model_path.name} /model\n"
    docker_template += f'ENTRYPOINT ["roheboam"]\n'
    docker_template += f'CMD ["serve", "--model_path", "/model", "--model_format", "{model_format}"]'
    return docker_template


def _build_model_dev_docker_image(source_path, docker_template, model_path, model_image_tag):
    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copytree(model_path, f"{temp_dir}/{model_path.name}")
        shutil.copytree(str(Path(source_path) / "roheboam"), f"{temp_dir}/roheboam/roheboam")
        shutil.copytree(str(Path(source_path) / "requirements"), f"{temp_dir}/roheboam/requirements")
        shutil.copy2(str(Path(source_path) / "setup.py"), f"{temp_dir}/roheboam/setup.py")
        with (Path(temp_dir) / "Dockerfile").open("w") as f:
            f.write(docker_template)
        client = docker.from_env()
        image, log_generator = client.images.build(path=temp_dir, tag=model_image_tag)
        stream_docker_logs(log_generator)
        return image
