"""Flask initialization"""

from flask import Flask

from models.log import Logger


# Database variable for connection


def create_app(config) -> Flask:
    # Create a flask application
    application = Flask(__name__)
    application.config.from_object(config)
    # Initialize the database connection within an application
    application.logger = Logger().get_logger()

    return application
