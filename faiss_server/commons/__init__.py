"""Common functions and objects for application different parts"""

import atexit

from models.faiss_database import FaissIndex
from source.configuration import (files, faiss_configuration)

faiss_index = FaissIndex(files.index_path, faiss_configuration.dimension)


def exit_handler(index: FaissIndex) -> None:
    """
    Write faiss in the disk on process termination
    :param index: faiss index
    """
    index.to_disk(files.backup_index_path)


# Register the function at exit
atexit.register(exit_handler, faiss_index)
