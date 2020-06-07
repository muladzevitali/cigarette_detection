"""Search endpoints for application"""

import os
from typing import (Dict, Optional, Tuple)

import cv2
import numpy
import werkzeug
from flask_cors import cross_origin
from flask_restful import (Resource, reqparse, abort)
from flask_restful.inputs import boolean

from src.utils import temporary
from src.yolo import cigarette_detector
from src.resnet import cigarette_classifier


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
        # Load image stream as numpy array
        image: numpy.array = self.load_image(image=args.get('image'))
        # Get coordinates from yolo model
        coordinates = cigarette_detector.detect(image, save_output=False)
        # Classify detections
        classification_results: dict = self.classify_cigarettes(coordinates, image, args)

        return {'data': classification_results}

    @staticmethod
    def load_image(image: werkzeug.datastructures.FileStorage) -> numpy.array:
        """Load werkzeug file storage to numpy. Returns only RGB layers"""
        image = cv2.imdecode(numpy.frombuffer(image.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

        return image[:, :, :3]

    def save_yolo_results(self, coordinates: list, image: numpy.array, args) -> Optional[Tuple[Dict[str, dict], dict]]:
        """Save yolo coordinates to disk and get paths of the images for showing on front"""
        # Get image metadata
        image_name, image_extension = os.path.splitext(args.get('image').filename)
        # Create a temporary directory for saving cropped images
        base_directory = temporary.get_temporary_directory()
        # Save original image
        image_path = f'{base_directory}/{image_name}{image_extension}'
        # Try to save image and return not allowed message if format not supported
        save_status: bool = self.save_image(image_path, image)
        if not save_status:
            return abort(http_status_code=404, message='Image format not allowed')

        # Results dict for sending to client
        results: dict = dict(image=dict(), detections=list())
        results['image']['found_objects'] = 0
        results['image']['image_path'] = image_path
        # Cropped images mapper for classifier
        cropped_images: Dict[str, numpy.array] = dict()

        for index_, coordinate in enumerate(coordinates):
            cropped_image = image[coordinate[0][1]: coordinate[1][1], coordinate[0][0]: coordinate[1][0]]
            cropped_image_path = f"{base_directory}/{index_}{image_extension}"
            # Catch if result is not image like array
            save_status: bool = self.save_image(cropped_image_path, cropped_image)
            # Save to results
            if save_status:
                results['detections'].append(
                    {'image_path': cropped_image_path})
                results['image']['found_objects'] += 1
                cropped_images[cropped_image_path] = cropped_image

        return results, cropped_images

    def classify_cigarettes(self, coordinates, image, args):
        # Save images to disk
        detector_results, cropped_images = self.save_yolo_results(coordinates, image, args)

        images_paths, cropped_images = list(cropped_images.keys()), list(cropped_images.values())

        predictions = cigarette_classifier.predict_classes(cropped_images)
        classifier_results = {image_path: prediction for image_path, prediction in zip(images_paths, predictions)}

        for detection in detector_results['detections']:
            image_path = detection['image_path']
            detection.update(classifier_results[image_path])

        return detector_results

    @staticmethod
    def save_image(image_path: str, image: numpy.array) -> bool:
        """Save image on disk"""
        try:
            cv2.imwrite(image_path, image)
            return True
        except cv2.error:
            return False
