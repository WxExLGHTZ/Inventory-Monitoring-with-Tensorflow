class Error(Exception):
    """Base class for other exceptions"""
    pass


class RecognitonError(Error):
    """Raised when there is no Image do recognize"""
    pass


class SaveError(Error):
    """Raised when there is no Directory names 'ResultOfRecognition'"""
    pass


class ValueOfBoxesTooLow(Error):
    """Raised when the count of the boxes which are recognized is not nine"""
    pass

class DatabaseError(Error):
    """Raised when database connection failed"""
    pass

