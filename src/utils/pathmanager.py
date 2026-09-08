from pathlib import Path

from .exceptions import PathNotFound

class PathManager:
    """ 
    Manages paths in this project.

    Attributes
    ----------
    ``root``
        Path to project root.
    ``data``
        Path in which data is saved.
    ``src``
        Path of source.
    """

    def __init__(self):
        self.root   = Path(__file__).resolve().parent.parent.parent 
        self.data           = self.root / 'data'
        self.src            = self.root / 'src'

        if not self.data.exists():
            self.data.mkdir()

        if not self.src.exists():
            raise PathNotFound(self.src)