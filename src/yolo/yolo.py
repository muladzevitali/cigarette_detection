from typing import Union

import numpy

from .detector import detection
from .loader import load_model
from .preprocess import prepare_image


class YoloDetector:
    def __init__(self):
        self.model = load_model()

    def detect(self, image: Union[str, numpy.array], save_output: bool = False):
        """Detect objects on image"""
        if isinstance(image, str):
            image = prepare_image(image, path=True)

        results = detection(image, self.model, draw=save_output)

        return results
