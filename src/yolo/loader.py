import os

from src.config import yolo_config
from .darknet import Darknet
from .preprocess import prepare_image


def load_model():
    """
    Load network
    """
    # Set up the neural network
    model = Darknet(yolo_config.config_file)
    model.load_weights(yolo_config.weights_file)

    # Set height for model input
    model.net_info["height"] = int(yolo_config.resolution)
    assert model.net_info["height"] % 32 == 0
    assert model.net_info["height"] > 32

    # If there's a GPU available, put the model on GPU
    if yolo_config.cuda:
        model.cuda()

    # Set the model in evaluation mode
    model.eval()

    return model


def load_images(path=None):
    """
    Load images and create output folder
    """
    # Detection phase
    image = path if path else os.path.join(os.getcwd(), 'image.jpg')
    if not os.path.exists(yolo_config.output_folder):
        os.makedirs(yolo_config.output_folder)

    return prepare_image(image, path=path)
