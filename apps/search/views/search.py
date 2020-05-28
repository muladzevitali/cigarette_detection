"""Search endpoints for applications"""

from flask_restful import Resource

from apps.auth import login_required


class Search(Resource):
    """
    Search vectors in faiss database
    """
    method_decorators = [login_required]

    def post(self):
        print('searching')

        return {'data': True}
