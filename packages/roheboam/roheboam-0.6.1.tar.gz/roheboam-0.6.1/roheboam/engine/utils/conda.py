import subprocess

import yaml


def get_current_conda_env(env_name=None):
    command = ["conda", "env", "export", "--no-builds"]
    if env_name:
        command.extend(["--name", env_name])
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return yaml.load(stdout.decode("UTF-8"), Loader=yaml.Loader)


lookup = {"get_current_conda_env": get_current_conda_env}
