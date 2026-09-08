from pathlib import Path

class DataSetsMissingError(Exception):
    def __init__(self):
        msg = 'Could not find the data!'
        super().__init__(msg)

class PathNotFound(Exception):
    def __init__(self, path: str | Path):
        super().__init__(f'Path was not found: {path}')