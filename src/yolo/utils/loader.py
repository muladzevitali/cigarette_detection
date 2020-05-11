from ..yolo.darknet import Darknet
from ..yolo.preprocess import prep_image
import os


def load_model(args):
    """
    Load darknet network
    :param args: program parameters
    :return: network model
    """
    # Set up the neural network
    print("Loading network.....")
    model = Darknet(args.cfg)
    model.load_weights(args.weights)
    print("Network successfully loaded")

    # Set height for model input
    model.net_info["height"] = int(args.resolution)
    assert model.net_info["height"] % 32 == 0
    assert model.net_info["height"] > 32

    # If there's a GPU availible, put the model on GPU
    if args.cuda:
        model.cuda()

    # Set the model in evaluation mode
    model.eval()
    return model


def load_images(args, path=None):
    """
    Load images and create output folder
    :param args: program parameters
    :return: image
    """
    # Detection phase
    if path:
        image = path
    else:
        image = os.path.join(os.getcwd(), args.image)
    image_resolution = int(args.resolution)
    if not os.path.exists(args.out_folder):
        os.makedirs(args.out_folder)

    return prep_image(image, image_resolution)




