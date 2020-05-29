"""Flask initialization"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from src.config.log import Logger

application = Flask(__name__)
# Database for connection
database = SQLAlchemy()


def create_app(config) -> Flask:
    # Create a flask application
    application.config.from_object(config)
    # Initialize the database connection within an application
    database.init_app(application)
    application.logger = Logger().get_logger()

    from .auth import (Register, Login)
    from .search import Search
    from .update import Update
    from .insert import Insert

    # Make an restful endpoints
    api = Api(application)
    # Add register endpoint
    api.add_resource(Register, "/register")
    # Add login endpoint
    api.add_resource(Login, "/login")
    # Add searching endpoint
    api.add_resource(Search, "/search")
    # Add insertion endpoint
    api.add_resource(Insert, "/insert")
    # Add update endpoint
    api.add_resource(Update, "/update")

    return application
