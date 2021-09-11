import ijson
import typing
import os


IGNORED_SUBDIRS = ['roll20-module', 'generated']
IGNORED_PREFIXES = ['roll20', 'foundry', 'changelog', 'renderdemo']


class FetoolsJsonFile(object):

    def __init__(self, name: str, json_path: str):
        self.name: str = name
        self.base_name = name.strip('.json')
        self.json_file_path: str = json_path
        self.json_file_handle = None
        self._root_key: str = ''
        self.json_keys: typing.List[str] = []

    @property
    def json_root_key(self) -> str:
        self._scan()
        return self._root_key

    def _scan(self):
        if len(self._root_key) == 0:
            self.json_file_handle = open(self.json_file_path)
            j = ijson.kvitems(self.json_file_handle, '')
            for k, v in j:
                self.json_keys.append(k)
                if len(self._root_key) == 0:
                    self._root_key = k
                elif self.base_name == k or self.base_name == k + 's':
                    self._root_key = k

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

    def _search(self, root_path: str):
        found_file_names: typing.List[str] = []
        for root, dirs, files in os.walk(root_path):
            subdir_path = '' if root == root_path else root
            self.json_file_paths[os.path.basename(subdir_path)] = []
            for f in files:
                ignored = False
                for prefix in IGNORED_PREFIXES:
                    if f.startswith(prefix):
                        ignored = True
                        break
                if ignored:
                    continue
                if f.endswith('json') and not os.path.basename(
                        subdir_path) in IGNORED_SUBDIRS:
                    self.json_file_paths[os.path.basename(subdir_path)].append(
                        FetoolsJsonFile(f, os.path.join(root, f)))
                    found_file_names.append(os.path.join(root_path,
                                                         os.path.basename(f)))
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
