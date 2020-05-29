"""Configuration class for applications"""

import configparser
import os

# Read the config file
config = configparser.ConfigParser()
config.read("config.ini")


class Application:
    """Configuration class for an application"""
    SECRET_KEY = config["APPLICATION"]["SECRET_KEY"]
    WTF_CSRF_SECRET_KEY = "SecretBogGe"

    @staticmethod
    def init_app(app):
        pass


class Files:
    """Configuration class for files"""
    media_path = config["MEDIA"]["MEDIA_PATH"]
    log_file_info = config["LOGGER"]["LOG_FILE_INFO"]
    log_file_error = config["LOGGER"]["LOG_FILE_ERROR"]
    index_path = config["FAISS_DATABASE"]["FAISS_INDEX_PATH"]
    backup_index_path = config["FAISS_DATABASE"]["BACKUP_INDEX_PATH"]

    def __init__(self):
        os.makedirs(Files.media_path, exist_ok=True)
        os.makedirs("media/logs", exist_ok=True)


class FaissConfiguration:
    dimension = int(config["FAISS_DATABASE"]["INDEX_DIMENSION"])
