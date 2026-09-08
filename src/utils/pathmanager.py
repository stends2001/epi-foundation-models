from pathlib import Path

class PathManager:

    def __init__(self):
        self.root   = Path(__file__).resolve().parent.parent.parent 
        self.data           = self.root / 'data'
        self.src            = self.root / 'src'
        self.results        = self.root / 'results'