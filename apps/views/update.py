"""Update endpoints for applications"""

from flask import current_app
from flask_restful import Resource
from werkzeug.local import LocalProxy

logger = LocalProxy(lambda: current_app.logger)


class Update(Resource):
    """
    Update vectors in faiss database
    """

    def post(self):
        pass
