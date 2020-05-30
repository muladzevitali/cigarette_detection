"""Search endpoints for application"""

import os

from flask import send_file
from flask_cors import cross_origin
from flask_restful import (Resource)

from src.config import media_config


class Media(Resource):
    """
    Search vectors in faiss database
    """

    @cross_origin()
    def get(self, folder, sub_folder, file_name):
        # Send file to front
        file_path = os.path.join(media_config.media_path, folder, sub_folder, file_name)
        # If file does not exist any more
        if not os.path.isfile(file_path):
            return ''

        return send_file(file_path, mimetype='image/gif')
