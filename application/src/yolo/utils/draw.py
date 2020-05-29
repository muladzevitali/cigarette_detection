import pickle
import random

import cv2


def rectangle(predictions, image, classes, args, path=None):
    """
    Draw rectangle over objects in image
    :param predictions:  predicted objects
    :param image: original image
    :param classes: object classes
    :param args: program parameters
    :param path: path to the image
    """
    for each in predictions:
        colors = pickle.load(open("media/pallete", "rb"))
        c1 = tuple(each[1:3].int())
        c2 = tuple(each[3:5].int())
        cls = int(each[-1])
        label = f"{classes[cls]}"
        color = random.choice(colors)
        cv2.rectangle(image, c1, c2, color, 1)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1, 1)[0]
        c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
        cv2.rectangle(image, c1, c2, color, -1)
        cv2.putText(image, label, (c1[0], c1[1] + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1, [225, 255, 255], 1)

    output_folder = args.out_folder
    if path:
        image_name = path.split('/')[-1]
    else:
        image_name = args.image.split('/')[-1]
    result_path = f"output.jpg"
    cv2.imwrite(result_path, image)


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
