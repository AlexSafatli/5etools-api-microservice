import ijson
import typing
import os


IGNORED_SUBDIRS = ['roll20-module', 'generated']
IGNORED_PREFIXES = ['roll20', 'foundry', 'changelog', 'renderdemo']


class FetoolsLibrary(object):

    def __init__(self, json_path: str):
        self.json_root_path: str = json_path
        self.json_file_paths: typing.Dict[str,
                                          typing.List[FetoolsJsonFile]] = {}

    def _search(self, root_path):
        found_files: typing.List[FetoolsJsonFile] = []
        for _, dirs, files in os.walk(root_path):
            for f in files:
                ignored = False
                for prefix in IGNORED_PREFIXES:
                    if f.startswith(prefix):
                        ignored = True
                        break
                if ignored:
                    continue
                if f.endswith('json'):
                    _f: str = os.path.join(root_path, f)
                    found_files.append(FetoolsJsonFile(f, _f))
            for d in dirs:
                if os.path.basename(d) in IGNORED_SUBDIRS:
                    continue
                self._search(d)
        self.json_file_paths[root_path] = found_files

    def search(self):
        self._search(self.json_root_path)


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
