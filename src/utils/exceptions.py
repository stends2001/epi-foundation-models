class DataSetsMissingError(Exception):
    def __init__(self):
        msg = 'Could not find the data!'
        super().__init__(msg)