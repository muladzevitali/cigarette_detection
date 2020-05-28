import json
from typing import (List, Optional, Tuple)

import cv2


def form_rectangle(points: List[List]) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Form a rectangle out of points on the plane.
    :return main diagonal coordinates"""

    # Diagonal bottom coordinates
    x1, y1 = min([int(point[0]) for point in points]), min([int(point[1]) for point in points])
    # Diagonal top coordinates
    x2, y2 = max([int(point[0]) for point in points]), max([int(point[1]) for point in points])

    return (x1, y1), (x2, y2)


def convert_labels_to_yolo(width, height, box):
    """Convert rectangle and image parameters to yolo format"""

    dw = 1 / width
    dh = 1 / height
    # Get center coordinates of rectangle
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    if y > 1:
        return False

    return x, y, w, h


image_path = '/home/muladzevitali/media/cigarettes/images/20.03.13 288957 Gorgiladze Tariel 0 adlia -  District - Unknown - Batumi Gulf  id=91281.jpeg'
json_path = '/home/muladzevitali/media/cigarettes/labels/20.03.13 288957 Gorgiladze Tariel 0 adlia -  District - Unknown - Batumi Gulf  id=91281.json'
image = cv2.imread(image_path)

with open(json_path) as input_stream:
    image_metadata = json.load(input_stream)

# Parse image meta
points: List[List[list]] = [shape['points'] for shape in image_metadata['shapes']]
# Form rectangles
rectangles = [form_rectangle(points_group) for points_group in points]

height, width = image.shape[:2]

for rectangle in rectangles:
    box = (rectangle[0][0], rectangle[1][0], rectangle[0][1], rectangle[1][1])
    yolo_bounding_box = convert_labels_to_yolo(width, height, box)
    if not yolo_bounding_box:
        image = cv2.rectangle(image, rectangle[0], rectangle[1], (0, 255, 0), 4)
        print(height, width, rectangle[0], rectangle[1])
    else:
        image = cv2.rectangle(image, rectangle[0], rectangle[1], (255, 0, 0), 4)
        print(yolo_bounding_box, box)
print(height, width)
cv2.imshow('image', image)
cv2.waitKey(0)
