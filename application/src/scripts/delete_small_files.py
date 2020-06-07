import os

output_folder_path = '/home/muladzevitali/media/cigarettes/cropped_packs'

for image_name in os.listdir(output_folder_path):
    image_path = os.path.join(output_folder_path, image_name)
    if os.path.getsize(image_path) < 1300:
        os.remove(image_path)
