import logging


class SQLException(Exception):
    """Problem executing a SQL command. After this exception must still come an error handling!

        Attributes:
            message -- explanation of the error
    """
    def __init__(self, message: str = "Problem executing a SQL command.") -> None:
        self.message: str = message
        super().__init__(self.message)

class UserNotFountException(Exception):
    """Problem executing a SQL command. After this exception must still come an error handling!

            Attributes:
                message -- explanation of the error
        """

    def __init__(self, message: str = "User not found in database.") -> None:
        self.message: str = message
        super().__init__(self.message)