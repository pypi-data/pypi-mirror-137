import json
from abc import ABC
from pathlib import Path

import hub
from hub.store.store import get_fs_and_path

from ...utils.convenience import git_commit_hash


class ActiveLoopHub(ABC):
    def __init__(self, activeloop_dataset):
        self.activeloop_dataset = activeloop_dataset
        self.additional_meta_info = self._load_additional_meta_info()

    @property
    def commit_id(self):
        return self.activeloop_dataset._commit_id

    @property
    def previous_commit_id(self):
        try:
            return self.all_previous_commit_ids[-1]
        except IndexError:
            print("Error when returning previous commit as there this is the first commit")
            return {}

    @property
    def current_node(self):
        return (
            self.activeloop_dataset._version_node.parent
            if not self.activeloop_dataset._version_node.children
            else self.activeloop_dataset._version_node
        )

    @property
    def all_previous_commit_ids(self):
        previous_commit_ids = []
        _current_node = self.current_node
        while _current_node:
            previous_commit_ids.append(_current_node.commit_id)
            _current_node = _current_node.parent
        return previous_commit_ids[::-1]

    @property
    def previous_commit_additional_meta_info(self):
        return self.all_additional_meta_info.get(self.previous_commit_id)

    @property
    def all_additional_meta_info(self):
        _, path = get_fs_and_path(self.activeloop_dataset.url)
        try:
            with open(str(Path(path) / "additional_meta.json"), "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("error loading additional info")
            return dict()

    def _store_additional_meta_info_for_commit_id(self, commit_id):
        _, path = get_fs_and_path(self.activeloop_dataset.url)
        all_additional_meta_info = self.all_additional_meta_info
        all_additional_meta_info[commit_id] = self.additional_meta_info
        with open(str(Path(path) / "additional_meta.json"), "w") as f:
            json.dump(all_additional_meta_info, f)

    def _load_additional_meta_info(self):
        self.additional_meta_info = self.all_additional_meta_info.get(self.commit_id, {})
        return self.additional_meta_info

    def __len__(self):
        return len(self.activeloop_dataset)

    def __getitem__(self, index):
        return self.activeloop_dataset.__getitem__(index)

    def commit(self, message):
        previous_commit_id = self.activeloop_dataset.commit(message)
        self._store_additional_meta_info_for_commit_id(previous_commit_id)
        return previous_commit_id

    def save(self):
        self._store_additional_meta_info_for_commit_id(self.commit_id)
        self.activeloop_dataset.save()

    def store(self, url):
        self.activeloop_dataset = self.activeloop_dataset.store(url=url)
        return self

    def filter(self, filter_fn):
        return self.activeloop_dataset.filter(filter_fn)

    def get_index_of_id(self, id):
        return self.filter(lambda sample: sample.compute()["id"] == id).indexes[0]

    def checkout(self, address, create=False):
        self.activeloop_dataset.checkout(address, create=create)
        self._load_additional_meta_info()

    def checkout_for_training_run(self):
        self.checkout(git_commit_hash(), create=True)

    def resize_shape(self, shape):
        self.activeloop_dataset.resize_shape(shape)

    def log(self):
        return self.activeloop_dataset.log()

    def debug_logs(self):
        print("All additional meta info")
        print(self.all_additional_meta_info)

        print()
        print("Additional meta info")
        print(self.additional_meta_info)

        print()
        print("Commit id to be used")
        print(self.commit_id)

        print()
        print("Logs")
        self.log()

        print()
        print("Previous commits")
        print(self.all_previous_commit_ids)

    @property
    def branches(self):
        return self.activeloop_dataset.branches
