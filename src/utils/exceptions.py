from pathlib import Path

class DataSetsMissingError(Exception):
    def __init__(self):
        msg = 'Could not find the data!'
        super().__init__(msg)

class PathNotFound(Exception):
    def __init__(self, path: str | Path):
        super().__init__(f'Path was not found: {path}')

class TiRexInstallationError(Exception):
    def __init__(self):
        super().__init__('model.cpkt could not be found in expected directory ``src/models/NX-AI/TiRex``.\nPlease check the installation of tirex-ts.\nFor more information please see https://github.com/NX-AI/tirex.')