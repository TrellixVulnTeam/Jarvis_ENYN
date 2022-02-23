import logging


class UnsolvableException(Exception):
    """Exception raised for errors that cannot be fixed automatically, but are too serious for the system to handle.

        Attributes:
            message -- explanation of the error
    """
    def __init__(self, message: str = "Extremely serious error occurred. Manual intervention necessary!") -> None:
        self.message: str = message
        super().__init__(self.message)
        logging.warning('[ERROR] ' + message)
