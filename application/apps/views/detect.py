"""Search endpoints for application"""

import cv2
import numpy
import werkzeug
from flask_restful import (Resource, reqparse)

from src.yolo import cigarette_detector


class Detect(Resource):
    """
    Search vectors in faiss database
    """
    parser = reqparse.RequestParser()
    parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files', required=True)

    def post(self):
        # Parse arguments
        args = self.parser.parse_args()
        # Load image stream as numpy array
        image = self.load_image(image=args.get('image'))
        # Get coordinates from yolo model
        coordinates = cigarette_detector.detect(image, save_output=False)

        return {'data': coordinates}

    @staticmethod
    def load_image(image: werkzeug.datastructures.FileStorage):
        """Load werkzeug file storage to numpy"""
        image = cv2.imdecode(numpy.frombuffer(image.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

        return image
