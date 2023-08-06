import subprocess
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
from urllib.parse import unquote

import boto3
from tqdm import tqdm

# https://stackoverflow.com/questions/43458001/can-we-copy-the-files-and-folders-recursively-between-aws-s3-buckets-using-boto3/43478147


class S3Client:
    def __init__(self, profile_name=None, endpoint_url=None):
        session_kwargs = {}
        client_kwargs = {}
        if profile_name is not None:
            session_kwargs["profile_name"] = profile_name
        if endpoint_url is not None:
            client_kwargs["endpoint_url"] = endpoint_url
        self.client = boto3.session.Session(**session_kwargs).client("s3", **client_kwargs)

    @contextmanager
    def download_to_temporary_file(self, bucket, key, show_progress=False):
        try:
            temp_file = NamedTemporaryFile()
            self.download(bucket, key, temp_file.name, show_progress)
            yield temp_file.name
        finally:
            pass

    def download(self, bucket, key, save_path, show_progress=False):
        save_path = str(save_path)

        if show_progress:

            def hook(t):
                def inner(bytes_amount):
                    t.update(bytes_amount)

                return inner

            file_size = float(self.client.head_object(Bucket=bucket, Key=unquote(key))["ContentLength"])
            with tqdm(total=file_size, unit="B", unit_scale=True, desc=save_path) as t:
                self.client.download_file(bucket, unquote(key), save_path, Callback=hook(t))
        else:
            self.client.download_file(bucket, unquote(key), save_path)

    def upload_file(self, path, bucket, key):
        self.client.upload_file(path, bucket, key)

    def upload_fileobj(self, fileobj, bucket, key):
        self.client.upload_fileobj(fileobj, bucket, key)

    def copy(self, source_bucket, source_key, dst_bucket, dst_key):
        self.client.copy({"Bucket": source_bucket, "Key": source_key}, dst_bucket, dst_key)

    def sync(self, from_path, to_path):
        cmd = ["aws"]

        if self.endpoint_url is not None:
            cmd.append(f"--endpoint-url {self.endpoint_url}")

        if self.profile_name is not None:
            cmd.append(f"=--profile {self.profile_name}")

        cmd.append(from_path)
        cmd.append(to_path)
        return subprocess.Popen(cmd).wait()

    def check_if_exists_in_s3(self, bucket, key):
        try:
            self.client.head_object(Bucket=bucket, Key=key)
            return True
        except Exception:
            return False

    def get_s3_keys(self, bucket, prefix=None, delimiter=None):
        keys = []
        try:
            for resp in self._construct_s3_paginator(bucket, prefix, delimiter):
                keys.extend([c["Key"] for c in resp["Contents"]])
        except KeyError:
            pass
        return keys

    def get_top_level_bucket_keys(self, bucket):
        keys = []
        for prefix in self._construct_s3_paginator(bucket, delimiter="/").search("CommonPrefixes"):
            keys.append(prefix.get("Prefix"))
        return keys

    def _construct_s3_paginator(self, bucket, prefix=None, delimiter=None):
        kwargs = {"Bucket": bucket}
        s3_paginator = self.client.get_paginator("list_objects_v2")

        if prefix is not None:
            kwargs.update({"Prefix": prefix})

        if delimiter is not None:
            kwargs.update({"Delimiter": delimiter})
        return s3_paginator.paginate(**kwargs)
