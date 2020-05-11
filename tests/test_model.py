from src.yolo.flags import init_detection_config
from src.yolo.utils.loader import load_model
from src.yolo.utils.detector import detection
from src.yolo.yolo.preprocess import prep_image

import cv2


LABELS = ['Cigarette']
flags = init_detection_config()
label_detector = load_model(flags)
height = label_detector.net_info['height']
image_path = r'C:\Users\vmuladze\Projects\cigarette_detection\media\images\1.jpg'
preped_image = prep_image(image_path, height)
results = detection(preped_image, label_detector, flags, draw=True)
