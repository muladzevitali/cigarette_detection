import os
from secrets import token_hex
import cv2

from src.yolo import cigarette_detector

images_folder_path = '/home/muladzevitali/media/cigarettes/images'
output_folder_path = '/home/muladzevitali/media/cigarettes/cropped_packs'

for image_name in os.listdir(images_folder_path):
    image_path = os.path.join(images_folder_path, image_name)
    image = cv2.imread(image_path)
    coordinates = cigarette_detector.detect(image_path)
    for index_, coordinate in enumerate(coordinates):
        # Take image from half and above
        y_start_coordinate = coordinate[1][1] - int((coordinate[1][1] - coordinate[0][1]) * 0.5)
        cropped_image = image[coordinate[0][1]:y_start_coordinate, coordinate[0][0]: coordinate[1][0]]
        cropped_image_path = os.path.join(output_folder_path, f'{token_hex(9)}.jpg')

        cv2.imwrite(cropped_image_path, cropped_image)
