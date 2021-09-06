class Config(object):
    pass


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    ENABLE_CACHE = False
    CELERY_TASK_ALWAYS_EAGER = True
