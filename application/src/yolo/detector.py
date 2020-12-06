import torch

from src.config import yolo_config
from src.yolo.util import write_results, load_classes
from .draw import (rectangle, get_boxes)

classes = load_classes(yolo_config.names_file)
height = yolo_config.resolution


def detection(image_loader, model, draw=True):
    image_processed = image_loader[0].cuda() if yolo_config.cuda else image_loader[0]
    # Original images from batches
    image_original = image_loader[1]
    # Get predictions
    predictions = predict(model, image_processed)
    if type(predictions) == int:
        return []
    if yolo_config.cuda:
        torch.cuda.synchronize(device=0)
    # Predictions rescaled to the original image
    print(predictions)
    # TODO needs some observations
    scaled_predictions = rescale_prediction(image_loader, predictions)
    # Save image in output folder
    if draw:
        rectangle(scaled_predictions, image_original, classes)
    # Get boxes from detected objects
    boxes = get_boxes(predictions)

    return boxes


def handle_dimensions(image_loader, predictions, cuda):
    """
    Repeat image dimensions along axis=1, twice and get cuda version
        if cuda is available
    :param image_loader: loader of an image
    :param cuda: cuda.is_avaible()
    :return: image dimensions of class torch FloatTensor or cuda version of it
    """
    image_dimensions = image_loader[2]
    image_dimensions = torch.FloatTensor(image_dimensions).repeat(1, 2)
    image_dimensions = image_dimensions.cuda() if cuda else image_dimensions
    image_dimensions = torch.index_select(image_dimensions, 0, predictions[:, 0].long())
    return image_dimensions


def predict(model, image_processed):
    """
    Get predictions from model
    """
    num_classes = len(classes)
    with torch.no_grad():
        predictions = model(image_processed, yolo_config.cuda)

    predictions = write_results(predictions, yolo_config.confidence, num_classes, nms=True,
                                nms_conf=yolo_config.nms_thresh)
    return predictions


def rescale_prediction(image_loader, predictions):
    """
    Rescale predictions to get boxes according to original size of image
    """
    image_dimensions = handle_dimensions(image_loader, predictions, yolo_config.cuda)
    scaling_factor = torch.min(height / image_dimensions, 1)[0].view(-1, 1)
    predictions[:, [1, 3]] -= (height - scaling_factor * image_dimensions[:, 0].view(-1, 1)) / 2
    predictions[:, [2, 4]] -= (height - scaling_factor * image_dimensions[:, 1].view(-1, 1)) / 2

    predictions[:, 1:5] /= scaling_factor

    for i in range(predictions.shape[0]):
        predictions[i, [1, 3]] = torch.clamp(predictions[i, [1, 3]], 0.0, image_dimensions[i, 0])
        predictions[i, [2, 4]] = torch.clamp(predictions[i, [2, 4]], 0.0, image_dimensions[i, 1])

    return predictions
