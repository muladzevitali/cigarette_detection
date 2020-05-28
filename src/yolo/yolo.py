from typing import (Union, List)

import numpy

from .detector import detection
from .loader import load_model
from .preprocess import prepare_image


class YoloDetector:
    def __init__(self):
        self.model = load_model()

    def detect(self, image: Union[str, numpy.array], save_output: bool = False) -> List[list]:
        """Detect objects on image"""
        if isinstance(image, str):
            image = prepare_image(image, path=True)
        else:
            image = prepare_image(image, path=False)

        return detection(image, self.model, draw=save_output)
