import ijson
import typing
import os


class FetoolsLibrary(object):

    def __init__(self, json_path):
        self.json_root_path: str = json_path
        self.json_file_paths: typing.List[FetoolsJsonFile] = []

    def search(self):
        found_files: typing.List[FetoolsJsonFile] = []
        for f in os.listdir(self.json_root_path):
            if f.endswith('.json'):
                f_path = os.path.join(self.json_root_path, f)
                found_files.append(FetoolsJsonFile(f, f_path))
        self.json_file_paths = found_files


class FetoolsJsonFile(object):

    def __init__(self, name: str, json_path: str):
        self.name: str = name
        self.json_file_path: str = json_path
        self.json_file_handle = None

    def _read(self):
        if self.json_file_handle is None:
            self.json_file_handle = open(self.json_file_path)

    def __getitem__(self, item):
        if item is None:
            return None
        self._read()
        return ijson.kvitems(self.json_file_handle, item)
