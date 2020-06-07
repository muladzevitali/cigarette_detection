from typing import List

import numpy
import torch
from PIL import Image
from torchvision import transforms

from src.config import resnet_config

# Transformations composition object
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor()
])


def pre_process_image(image_array: numpy.array, unsqueeze=False):
    """Pre process image including casting for numpy to PIL image and apply transformations"""
    # Cast from numpy to PIL
    image = Image.fromarray(image_array)
    # Apply transformations
    image = transform(image)
    # Apply cuda if available
    if resnet_config.cuda:
        image = image.cuda()

    return image.unsqueeze(0) if unsqueeze else image


def transform_images(images: List[numpy.array]) -> torch.tensor:
    """
    Transform list of images to tensor with transformations
    """
    images = torch.stack([pre_process_image(image, unsqueeze=False) for image in images])

    if resnet_config.cuda:
        images = images.cuda()

    return images
