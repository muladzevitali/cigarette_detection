"""Flask initialization"""

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
# Database for connection
database = SQLAlchemy()
# Initialize cors
cors = CORS(application)


def create_app(config) -> Flask:
    # Create a flask application
    application.config.from_object(config)
    # Initialize the database connection within an application
    database.init_app(application)

    from .views import (Detect, Insert, Update, Media)

    # Make an restful endpoints
    api = Api(application, prefix='/rest/v1')
    # Add detection endpoint
    api.add_resource(Detect, "/detect")
    # Add insertion endpoint
    api.add_resource(Insert, "/insert")
    # Add update endpoint
    api.add_resource(Update, "/update")
    # Add media endpoint
    api.add_resource(Media, '/media/<folder>/<sub_folder>/<file_name>')

    return application
