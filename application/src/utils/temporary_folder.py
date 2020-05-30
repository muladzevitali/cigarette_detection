import tempfile
import threading
import time


class TemporaryDirectoryFactory:
    def __init__(self, timeout: int):
        self.set = set()
        self.timeout = timeout

    def get_temporary_directory(self):
        """Get temporary directory"""
        # Create directory
        directory = tempfile.TemporaryDirectory(dir='media/results')
        # Add to auto removable items set
        self.add(directory)

        return directory.name

    def add(self, directory: tempfile.TemporaryDirectory):
        # Add directory to static set
        self.set.add(directory)
        # Create thread
        t = threading.Thread(target=self.timeout_set_remove, args=(directory,))
        # Run the job
        t.start()

    def timeout_set_remove(self, item: tempfile.TemporaryDirectory):
        """Remove an object after time elapsed"""
        # Wait for time
        time.sleep(self.timeout)
        # Remove entire directory
        item.cleanup()
        # Delete the folder from set
        self.set.remove(item)
