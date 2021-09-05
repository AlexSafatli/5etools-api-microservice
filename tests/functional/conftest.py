import pytest


@pytest.fixture(scope='module')
def testapp(app):
    return app.test_client()
