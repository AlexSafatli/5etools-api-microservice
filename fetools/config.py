from os import environ


class Config(object):
    FETOOLS_JSON_ROOT_PATH = environ.get('FETOOLS_JSON_ROOT_PATH', './jsons')


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    ENABLE_CACHE = False
    CELERY_TASK_ALWAYS_EAGER = True
