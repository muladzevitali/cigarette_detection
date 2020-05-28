"""Configuration class for applications"""

import configparser
import os
from dataclasses import dataclass

config = configparser.ConfigParser()
config.read("config.ini")
base_dir = os.path.abspath('.')

os.environ["NLS_LANG"] = "AMERICAN_AMERICA.AL32UTF8"


@dataclass(init=False)
class SqLite:
    uri = f'sqlite:///{base_dir}/media/database/development.db'


@dataclass(init=False)
class ApplicationDatabase:
    """Class for database handling"""
    # If another database required create its class and change the uri as needed
    uri = SqLite.uri if config['DATABASE']['DATABASE'] == 'SQLITE' else ''
    table_prefix = config['DATABASE']['TABLE_PREFIX']


@dataclass(init=False)
class Application:
    SECRET_KEY = config["APPLICATION"]["SECRET_KEY"]
    SQLALCHEMY_ECHO = config["APPLICATION"]["SQLALCHEMY_ECHO"] == "true"
    SQLALCHEMY_TRACK_MODIFICATIONS = config["APPLICATION"]["SQLALCHEMY_TRACK_MODIFICATIONS"] == "true"
    SQLALCHEMY_DATABASE_URI = ApplicationDatabase.uri

    @staticmethod
    def init_app(app):
        pass


@dataclass()
class Media:
    media_path = config["MEDIA"]["MEDIA_PATH"]
    log_file_info = config["LOGGER"]["LOG_FILE_INFO"]
    log_file_error = config["LOGGER"]["LOG_FILE_ERROR"]
    index_path = config["MEDIA"]["FAISS_INDEX_PATH"]

    def __init__(self):
        os.makedirs(self.media_path, exist_ok=True)


class FaissConfiguration:
    dimension = int(config["FAISS_DATABASE"]["INDEX_DIMENSION"])
