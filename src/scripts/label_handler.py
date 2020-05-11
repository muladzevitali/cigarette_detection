import json
import os
from math import (floor, ceil)
from shutil import copyfile
from typing import (List, Tuple, Optional)
from secrets import token_hex
from PIL import Image


def form_rectangle(points: List[List]) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Form a rectangle out of points on the plane.
    :return main diagonal coordinates"""

    # Diagonal bottom coordinates
    x1, y1 = min([point[0] for point in points]), min([point[1] for point in points])
    # Diagonal top coordinates
    x2, y2 = max([point[0] for point in points]), max([point[1] for point in points])

    return (x1, y1), (x2, y2)


def parse_data_folder(images_dir_path: str, labels_dir_path: str) -> List[tuple]:
    """Parses directory and returns image, json tuples list"""

    parsed_files: List[tuple] = list()
    for file in os.listdir(images_dir_path):
        image_file = os.path.join(images_dir_path, file)
        file_name = f'{os.path.splitext(file)[0]}.json'
        json_file = os.path.join(labels_dir_path, file_name)

        parsed_files.append((image_file, json_file))

    return parsed_files


def get_rectangles(image_meta: dict):
    """Get labeled points from json and form a rectangle from each point group"""
    # Parse image meta
    points: List[List[list]] = [shape['points'] for shape in image_meta['shapes']]
    # Form rectangles
    rectangle_points = [form_rectangle(points_group) for points_group in points]

    return rectangle_points


def convert_labels_to_yolo(width, height, box):
    """Convert rectangle and image parameters to yolo format"""

    dw = 1. / width
    dh = 1. / height
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    if y > 1:
        print(width, height, box)
    return x, y, w, h


def create_yolo_label_file(file_: tuple, current_class_id: str, yolo_dataset_dir: str):
    """Create yolo format txt file from json label"""
    image_path, json_path = file_
    file_name, file_extension = os.path.splitext(os.path.basename(image_path))
    new_file_name = token_hex(10)
    image_new_path = os.path.join(yolo_dataset_folder, f'{new_file_name}{file_extension}')
    # Output file path
    output_file_name = f'{new_file_name}.txt'
    output_file_path = os.path.join(yolo_dataset_dir, output_file_name)
    output_file = open(output_file_path, 'w')
    # Get rectangles
    with open(json_path) as input_stream:
        image_metadata = json.load(input_stream)
    # Form rectangles from labeled points
    rectangles = get_rectangles(image_metadata)
    # Get image sizes
    image = Image.open(image_path)
    width = int(image.size[0])
    height = int(image.size[1])
    # Iterate throw rectangles and write each of them on a separate line
    for rectangle in rectangles:
        box = (rectangle[0][0], rectangle[1][0], rectangle[0][1], rectangle[1][1])
        yolo_bounding_box = convert_labels_to_yolo(width, height, box)
        output_file.write(f'{current_class_id} ' + " ".join([str(a) for a in yolo_bounding_box]) + '\n')
    if not os.path.isfile(image_new_path):
        copyfile(image_path, image_new_path)

    output_file.close()


if __name__ == '__main__':
    media_dir: str = '/home/muladzevitali/media/cigarettes'
    # Folder paths for images and labels
    images_folder = os.path.join(media_dir, 'images')
    labels_folder = os.path.join(media_dir, 'labels')
    yolo_dataset_folder = os.path.join(media_dir, 'yolo_dataset')

    files: List[tuple] = parse_data_folder(images_folder, labels_folder)
    for file in files:
        create_yolo_label_file(file, 0, yolo_dataset_folder)
