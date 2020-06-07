import os

import cv2
import imutils

images_folder_path = '/home/muladzevitali/media/cigarettes/data'
output_folder_path = '/home/muladzevitali/media/cigarettes/rotated_data'

for image_name in os.listdir(images_folder_path):
    image_path = os.path.join(images_folder_path, image_name)
    image = cv2.imread(image_path)
    rotated = imutils.rotate(image, -90)
    image_new_path = os.path.join(output_folder_path, image_name)
    cv2.imwrite(image_new_path, rotated)
