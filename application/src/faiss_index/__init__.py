"""Common functions and objects for application different parts"""

import atexit

from .faiss_index import FaissIndex
from src.config import (media_config, faiss_config)

faiss_index = FaissIndex(media_config.index_path, faiss_config.dimension)


def exit_handler(index: FaissIndex) -> None:
    """
    Write faiss in the disk on process termination
    :param index: faiss index
    """
    # index.to_disk(media_config.backup_index_path)


# Register the function at exit
atexit.register(exit_handler, faiss_index)
