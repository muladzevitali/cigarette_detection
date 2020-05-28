"""Search endpoints for applications"""

from flask_restful import Resource


class Search(Resource):
    """
    Search vectors in faiss database
    """

    def post(self):
        print('searching')

        return {'data': True}
