"""Configuration class for applications"""

import configparser
import os
from dataclasses import dataclass

import torch

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
    ENABLE_REGISTRATION = config['APPLICATION']['ENABLE_REGISTRATION'] == 'true'

    @staticmethod
    def init_app(app):
        pass


@dataclass()
class Media:
    media_path = os.path.join(base_dir, config["MEDIA"]["MEDIA_PATH"])
    result_files_path = os.path.join(media_path, 'results')

    def __init__(self):
        os.makedirs(self.media_path, exist_ok=True)
        os.makedirs(self.result_files_path, exist_ok=True)


class FaissConfiguration:
    dimension = int(config["FAISS_DATABASE"]["INDEX_DIMENSION"])
    index_path = config["FAISS_DATABASE"]["FAISS_INDEX_PATH"]


@dataclass(init=False)
class YoloConfiguration:
    output_folder = os.path.join(base_dir, config['YOLO']['OUTPUT_FOLDER'])
    batch_size = int(config['YOLO']['BATCH_SIZE'])
    confidence = float(config['YOLO']['CONFIDENCE'])
    nms_thresh = float(config['YOLO']['NMS_THRESH'])
    config_file = config['YOLO']['CONFIG']
    weights_file = config['YOLO']['WEIGHTS']
    names_file = config['YOLO']['NAMES']
    resolution = int(config['YOLO']['RESOLUTION'])
    scales = config['YOLO']['SCALES']
    cuda = torch.cuda.is_available()


@dataclass(init=False)
class Resnet:
    weights_file = config['RESNET']['WEIGHTS']
    cuda = torch.cuda.is_available()
    batch_size = int(config['RESNET']['BATCH_SIZE'])
    top_k = int(config['RESNET']['TOP_K'])
