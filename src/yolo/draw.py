import os

import cv2

from src.config import yolo_config


def rectangle(predictions, image, classes, path=None):
    """
    Draw rectangle over objects in image
    """
    for each in predictions:
        c1 = tuple(each[1:3].int())
        c2 = tuple(each[3:5].int())
        cls = int(each[-1])
        label = classes[cls]
        image = cv2.rectangle(image, c1, c2, (255, 0, 0), 1)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1, 1)[0]
        c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
        image = cv2.rectangle(image, c1, c2, (255, 0, 0), -1)
        image = cv2.putText(image, label, (c1[0], c1[1] + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1, [225, 255, 255], 1)

    image_name = path.split('/')[-1] if path else 'output.jpg'
    image_path = os.path.join(yolo_config.output_folder, image_name)

    a = cv2.imwrite(image_path, image)
    print(a)


def get_boxes(predictions):
    """
    Get boxes from predictions
    :param predictions: prediction
    :return: upper left point, bottom right point, label
    """
    boxes = list()
    for each in predictions:
        upper_left = (int(each[1]), int(each[2]))
        bottom_right = (int(each[3]), int(each[4]))
        label = int(each[-1])
        boxes.append([upper_left, bottom_right, label])
    return boxes
