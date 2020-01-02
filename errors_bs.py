class FileError(Exception):
    def __init__(self, message):
        super().__init__(message)
        
class NotImplementedError(Exception):
    def __init__(self):
        super().__init__("This method not implemented yet")