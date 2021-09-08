import ijson
import typing
import os


IGNORED_SUBDIRS = ['roll20-module', 'generated']
IGNORED_PREFIXES = ['roll20', 'foundry', 'changelog', 'renderdemo']


class FetoolsJsonFile(object):

    def __init__(self, name: str, json_path: str):
        self.name: str = name
        self.json_file_path: str = json_path
        self.json_file_handle = None

    def _read(self):
        if self.json_file_handle is not None:
            self.json_file_handle.close()
        self.json_file_handle = open(self.json_file_path)

    def __getitem__(self, item):
        if item is None:
            return None
        self._read()
        return ijson.kvitems(self.json_file_handle, item + '.item')


class FetoolsLibrary(object):

    def __init__(self, json_path: str):
        self.json_root_path: str = json_path
        self.json_file_paths: typing.Dict[str,
                                          typing.List[FetoolsJsonFile]] = {}
        self.json_file_names: typing.List[str] = []

    def _search(self, root_path):
        found_files: typing.List[FetoolsJsonFile] = []
        found_file_names: typing.List[str] = []
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
                    found_file_names.append(os.path.join(root_path,
                                                         os.path.basename(f)))
            for d in dirs:
                if not os.path.basename(d) in IGNORED_SUBDIRS:
                    self._search(d)
        if root_path == self.json_root_path:
            self.json_file_paths[''] = found_files
        else:
            self.json_file_paths[root_path] = found_files
        self.json_file_names.extend(found_file_names)

    def search(self) -> None:
        self._search(self.json_root_path)

    def modules(self) -> typing.List[str]:
        return list(self.json_file_paths.keys())

    def __getitem__(self, item) -> FetoolsJsonFile:
        if item is None:
            return FetoolsJsonFile('', '')
        path = os.path.split(item)
        if len(path) == 1:
            li = self.json_file_paths['']
        else:
            li = self.json_file_paths[path[0]]
        for fi in li:
            if fi.name == item + '.json':
                return fi
        return FetoolsJsonFile('', '')
