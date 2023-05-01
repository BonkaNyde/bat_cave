# from 

class Config:
    """
    """
    SECRET_KEY = ''
    CELERY=dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,
    )


class DevConfig(Config):
    """
    """
    DEBUG = True


class ProdConfig(Config):
    """
    """
    DEBUG = False


class TestConfig(Config):
    """
    """


config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'testing': TestConfig
}
