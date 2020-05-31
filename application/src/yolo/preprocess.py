import cv2
import numpy as np
import torch
from PIL import Image

from src.config import yolo_config


def letterbox_image(img, inp_dim):
    img_w, img_h = img.shape[1], img.shape[0]
    w, h = inp_dim
    new_w = int(img_w * min(w / img_w, h / img_h))
    new_h = int(img_h * min(w / img_w, h / img_h))
    resized_image = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

    canvas = np.full((inp_dim[1], inp_dim[0], 3), 128)

    canvas[(h - new_h) // 2:(h - new_h) // 2 + new_h, (w - new_w) // 2:(w - new_w) // 2 + new_w, :] = resized_image

    return canvas


def prepare_image(img, path=True):
    """
    Prepare image for inputting to the neural network.
    Returns a Variable 
    """
    orig_im = cv2.imread(img) if path else img
    dim = orig_im.shape[1], orig_im.shape[0]
    # If image is png like with more than 3 layers
    if orig_im.shape[2] > 3:
        orig_im = orig_im[:, :, :3]

    img = (letterbox_image(orig_im, (yolo_config.resolution, yolo_config.resolution)))
    img_ = img[:, :, ::-1].transpose((2, 0, 1)).copy()
    img_ = torch.from_numpy(img_).float().div(255.0).unsqueeze(0)

    return img_, orig_im, dim


def prep_image_pil(img, network_dim):
    orig_im = Image.open(img)
    img = orig_im.convert('RGB')
    dim = img.size
    img = img.resize(network_dim)
    img = torch.ByteTensor(torch.ByteStorage.from_buffer(img.tobytes()))
    img = img.view(*network_dim, 3).transpose(0, 1).transpose(0, 2).contiguous()
    img = img.view(1, 3, *network_dim)
    img = img.float().div(255.0)

    return img, orig_im, dim


def inp_to_image(inp):
    inp = inp.cpu().squeeze()
    inp = inp * 255
    try:
        inp = inp.data.numpy()
    except RuntimeError:
        inp = inp.numpy()
    inp = inp.transpose(1, 2, 0)

    inp = inp[:, :, ::-1]
    return inp
