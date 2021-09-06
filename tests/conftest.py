import pytest

from fetools.app import create_app
from fetools.config import TestConfig


@pytest.fixture(scope='module')
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()
