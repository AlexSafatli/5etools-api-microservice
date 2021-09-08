from fetools.config import Config
from fetools.bridge import FetoolsLibrary


def test_json_library():
    library = FetoolsLibrary(Config.FETOOLS_JSON_ROOT_PATH)
    library.search()

    assert len(library.json_file_paths) > 0
    assert 'class' in library.modules()
