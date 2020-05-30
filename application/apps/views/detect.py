"""Search endpoints for application"""

from typing import Dict

import cv2
import numpy
import werkzeug
from flask_cors import cross_origin
from flask_restful import (Resource, reqparse)
from flask_restful.inputs import boolean

from src.utils import temporary
from src.yolo import cigarette_detector


class Detect(Resource):
    """
    Search vectors in faiss database
    """
    parser = reqparse.RequestParser()
    parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files', required=True)
    parser.add_argument('localize', type=boolean, location='form', required=True)
    parser.add_argument('classify', type=boolean, location='form', required=True)

    @cross_origin()
    def post(self):
        # Parse arguments
        args = self.parser.parse_args()
        print(args)
        # Load image stream as numpy array
        image: numpy.array = self.load_image(image=args.get('image'))
        # Get coordinates from yolo model
        coordinates = cigarette_detector.detect(image, save_output=False)

        results: Dict[str, dict] = self.save_yolo_results(coordinates, image, args)

        return {'data': results}

    @staticmethod
    def load_image(image: werkzeug.datastructures.FileStorage) -> numpy.array:
        """Load werkzeug file storage to numpy"""
        image = cv2.imdecode(numpy.frombuffer(image.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

        return image

    @staticmethod
    def save_yolo_results(coordinates: list, image: numpy.array, args) -> Dict[str, dict]:
        """Save yolo coordinates to disk and get paths of the images for showing on front"""
        # Get image metadata
        image_name, image_extension = args.get('image').filename.split('.')
        # Create a temporary directory for saving cropped images
        base_directory = temporary.get_temporary_directory()
        # Save original image
        image_path = f'{base_directory}/{image_name}.{image_extension}'
        cv2.imwrite(image_path, image)
        # Results dict for sending to client
        results: dict = dict(image=dict(), detections=list())
        results['image']['found_objects'] = len(coordinates)
        results['image']['image_path'] = image_path

        for index_, coordinate in enumerate(coordinates):
            cropped_image = image[coordinate[0][1]: coordinate[1][1], coordinate[0][0]: coordinate[1][0]]
            cropped_image_path = f"{base_directory}/{index_}.{image_extension}"
            cv2.imwrite(cropped_image_path, cropped_image)
            results['detections'].append({'precision': 0.8, 'image_path': cropped_image_path})

        return results
