from pathlib import Path

from ...utils.convenience import run_shell_command


class DVC:
    def __init__(self, dvc_run_path=None, silent=False, construct_only=False):
        self.default_dvc_run_path = dvc_run_path
        self.default_silent = silent
        self.construct_only = construct_only

    def _run_shell_command_with_log_status(self, cmd, silent):
        cmd = " ".join(cmd)
        if self.construct_only:
            print(cmd)
        else:
            run_shell_command(cmd, silent=self.default_silent if silent is None else silent, same_process=False)

    def _construct_dvc_command_with_run_path(self, dvc_run_path):
        cmd = ["dvc"]
        dvc_run_path = self.default_dvc_run_path if dvc_run_path is None else dvc_run_path
        if dvc_run_path:
            cmd.extend(["--cd", str(dvc_run_path)])
        return cmd

    def init(self, sub_dir=None, force=False, verbose=False, dvc_run_path=None, silent=False):
        cmd = self._construct_dvc_command_with_run_path(dvc_run_path)
        cmd.extend(["init"])

        if sub_dir:
            cmd.extend(["--subdir"])
        if force:
            cmd.extend(["--force"])
        if verbose:
            cmd.extend(["--verbose"])
        self._run_shell_command_with_log_status(cmd, silent)

    def install(self, dvc_run_path=None, silent=False):
        cmd = self._construct_dvc_command_with_run_path(dvc_run_path)
        cmd.extend(["install"])
        self._run_shell_command_with_log_status(cmd, silent)

    def add(self, add_path, dvc_output_path=None, dvc_run_path=None, silent=False):
        cmd = self._construct_dvc_command_with_run_path(dvc_run_path)
        cmd.extend(["add", str(add_path)])
        if dvc_output_path is not None:
            Path(dvc_output_path).parent.mkdir(exist_ok=True, parents=True)
            cmd.extend(["--file", str(dvc_output_path)])
            self._run_shell_command_with_log_status(cmd, silent)

    def add_remote(self, remote_name, remote_path, as_default=True, dvc_run_path=None, silent=False):
        cmd = self._construct_dvc_command_with_run_path(dvc_run_path)
        cmd.extend(["remote", "add"])

        if as_default:
            cmd.extend(["-d"])
        cmd.extend([remote_name, remote_path])
        self._run_shell_command_with_log_status(cmd, silent)

    def modify_remote_endpoint(self, remote_name, endpoint_url, dvc_run_path=None, silent=False):
        cmd = self._construct_dvc_command_with_run_path(dvc_run_path)
        cmd.extend(["remote", "modify", "--local", remote_name, "endpointurl", endpoint_url])
        self._run_shell_command_with_log_status(cmd, silent)

    def modify_remote_access_keys_id(self, remote_name, access_key_id, dvc_run_path=None, silent=False):
        cmd = self._construct_dvc_command_with_run_path(dvc_run_path)
        cmd.extend(["remote", "modify", "--local", remote_name, "access_key_id", access_key_id])
        self._run_shell_command_with_log_status(cmd, silent)

    def modify_remote_secret_access_key(self, remote_name, secret_access_key, dvc_run_path=None, silent=False):
        cmd = self._construct_dvc_command_with_run_path(dvc_run_path)
        cmd.extend(["remote", "modify", "--local", remote_name, "secret_access_key", secret_access_key])
        self._run_shell_command_with_log_status(cmd, silent)

    def run(self, name, run_command, dependency_paths=[], output_paths=[], dvc_run_path=None, force=False, no_run_cache=False, silent=False):
        cmd = self._construct_dvc_command_with_run_path(dvc_run_path)
        cmd.extend(["run"])
        cmd.extend(["-n", name])
        if force:
            cmd.extend(["--force"])
        if no_run_cache:
            cmd.extend(["--no-run-cache"])
        cmd.extend([f"-d {str(p)}" for p in dependency_paths])
        cmd.extend([f"-o {str(p)}" for p in output_paths])
        cmd.extend([run_command])
        self._run_shell_command_with_log_status(cmd, silent)

    def repro(self, target=None, dvc_run_path=None, silent=False):
        cmd = self._construct_dvc_command_with_run_path(dvc_run_path)
        if target is not None:
            cmd.extend([target])
        cmd.extend(["repro"])
        self._run_shell_command_with_log_status(cmd, silent)

    def pull(self, stage=None, dvc_run_path=None, silent=False):
        cmd = self._construct_dvc_command_with_run_path(dvc_run_path)
        cmd.extend(["pull"])
        if stage:
            cmd.extend([stage])
        self._run_shell_command_with_log_status(cmd, silent)

    def push(self, dvc_run_path=None, silent=False):
        cmd = self._construct_dvc_command_with_run_path(dvc_run_path)
        cmd.extend(["push"])
        self._run_shell_command_with_log_status(cmd, silent)
