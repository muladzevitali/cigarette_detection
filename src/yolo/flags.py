import argparse

import torch


def _add_detection_config(arg_parser):
    """Adds default configuration parameters to argument parser
        Args:
           arg_parser - argument parser to add parameters
    """
    arg_parser.add_argument("--image", dest='image',
                            help="Image to perform detection upon",
                            default="images", type=str)
    arg_parser.add_argument("--video", dest='video',
                            help="video to perform detection upon",
                            default="data/video/test.mp4", type=str)
    arg_parser.add_argument("--out_folder", dest='out_folder',
                            help="Image / Directory to store detections to", default="results", type=str)
    arg_parser.add_argument("--batch_size", dest="batch_size", help="Batch size", default=1)
    arg_parser.add_argument("--confidence", dest="confidence", type=float,
                            help="Object Confidence to filter predictions", default=0.3)
    arg_parser.add_argument("--nms_thresh", dest="nms_thresh", help="NMS Threshhold", default=0.3, type=float)
    arg_parser.add_argument("--cfg", dest='cfg',
                            help="Config file", default="media/models/cigarette/cigarette.cfg", type=str)
    arg_parser.add_argument("--weights", dest='weights', help="weightsfile",
                            default="media/models/cigarette/cigarette.weights", type=str)
    arg_parser.add_argument("--names", dest='names', help="classes file",
                            default="media/models/cigarette/cigarette.names", type=str)
    arg_parser.add_argument("--resolution", dest='resolution',
                            help="Input resolution of the network. Increase to increase accuracy. "
                                 "Decrease to increase speed",
                            default="416", type=str)
    arg_parser.add_argument("--scales", dest="scales", help="Scales to use for detection",
                            default="0,1,2", type=str)
    cuda = int(torch.cuda.is_available())
    arg_parser.add_argument("--gpu", dest="cuda", default=cuda, help="If cuda available", type=int)


def init_detection_config():
    """Initializes default configuration for features vector search
        Returns:
            flags - configuration parameters
    """
    arg_parser = argparse.ArgumentParser('Image search service')
    _add_detection_config(arg_parser)
    flags, _ = arg_parser.parse_known_args()

    return flags


def init_config():
    """Initializes configuration parameters container
        Returns:
            flags - training and evaluation configuration parameters
    """
    # Network architecture
    arg_parser = argparse.ArgumentParser('Image search standalone')
    _add_detection_config(arg_parser)
    flags, _ = arg_parser.parse_known_args()

    return flags
