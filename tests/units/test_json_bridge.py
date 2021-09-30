from fetools.config import Config
from fetools.bridge import FetoolsLibrary


def test_json_library():
    library = FetoolsLibrary(Config.FETOOLS_JSON_ROOT_PATH)
    library.search()

    assert len(library.json_file_paths) > 0
    assert 'class' in library.modules


def test_json_file():
    library = FetoolsLibrary(Config.FETOOLS_JSON_ROOT_PATH)
    library.search()

    items = library['items']
    assert len(items.name) > 0 and items.name == 'items.json'

    item_found = False
    assert items.json_root_key == 'item'
    item_kvs = items[items.json_root_key]
    item_names = (v for k, v in item_kvs if k == 'name')
    for name in item_names:
        assert len(name) > 0
        item_found = True
    assert item_found
