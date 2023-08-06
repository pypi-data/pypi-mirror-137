class PreprocessError(Exception):
    """
    Base class for all preprocessing exceptions
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class PreprocessFailed(PreprocessError):
    """
    Is raised when preprocessor in unable to process a file
    """

    pass


class HackDetected(PreprocessError):
    """
    Is raised when a suspicious content is detected in a file
    """

    pass
