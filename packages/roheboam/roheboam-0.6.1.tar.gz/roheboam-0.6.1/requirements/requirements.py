import os
import platform
import sys

python_version = int(f"{sys.version_info.major}{sys.version_info.minor}")
version_string = f"{python_version}m" if python_version <= 37 else python_version
chip_architecture = platform.uname().processor

torch_install_string = None
torchvision_install_string = None


if os.environ.get("ROHEBOAM_ENV") == "dev":
    # since the current dev machine uses a RTX3090 and Pytorch by default does not ship with CUDA10 yet see here:
    # https://discuss.pytorch.org/t/pytorch-with-cuda-11-compatibility/89254/19
    torchvision_install_string = f"torchvision @ \
            https://download.pytorch.org/whl/cu113/torchvision-0.11.0%2Bcu113-cp{python_version}-cp{version_string}-linux_x86_64.whl"
    torch_install_string = f"torch @ \
            https://download.pytorch.org/whl/cu113/torch-1.10.0%2Bcu113-cp{python_version}-cp{version_string}-linux_x86_64.whl"
else:
    torchvision_install_string = "torchvision"
    torch_install_string = "torch"


REQUIREMENTS = [
    # Project Dependencies
    "nose==1.3.7",
    "fastprogress==0.1.15",
    "albumentations==1.0.3",
    # Need to pin pyparsing so that miniutils doesn't use 3.x.x
    # `operatorPrecendence` is deprecated in version 3
    "pyparsing==2.4.7",
    "miniutils==1.0.1",
    "matplotlib==3.2.2",
    "tqdm>=4.32.2=pypi_0",
    "albumentations==1.0.3",
    torchvision_install_string,
    torch_install_string,
    "pytorch-lightning==1.5.4",
    "scikit-learn==0.23.2",
    "pretrainedmodels==0.7.4",
    "opencv-python==4.5.5.62",
    "docker==4.4.1",
    "pyvips==2.1.14",
    "mlflow==1.23.0",
    "flask==1.1.2",
    "awscli",
]
