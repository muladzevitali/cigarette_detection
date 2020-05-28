from src.yolo import cigarette_detector
from src.yolo.detector import detection

image_path = r'C:\Users\vmuladze\Projects\cigarette_detection\media\images\3.jpg'
results = cigarette_detector.detect(image_path, save_output=True)
