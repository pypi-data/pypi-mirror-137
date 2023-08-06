import os
from djask import Djask
from .settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")
    app = Djask("{{cookiecutter.app_name}}", config=config[config_name])
    return app
