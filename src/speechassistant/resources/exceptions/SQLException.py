import logging


class SQLException(Exception):
    """Problem executing a SQL command. After this exception must still come an error handling!

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str = "Problem executing a SQL command.") -> None:
        self.message: str = message
        super().__init__(self.message)


class FileNameAlreadyExists(Exception):
    """Problem executing a SQL command, because the filename already exists in the database. After this exception must still
    come an error handling!

         Attributes:
             message -- explanation of the error
    """

    def __init__(self, message: str = "Filename already exists.") -> None:
        self.message: str = message
        super().__init__(self.message)


class UserNotFountException(Exception):
    """Problem executing a SQL command, because no matching user was found. After this exception must still come
    an error handling!

            Attributes:
                message -- explanation of the error
    """

    def __init__(self, message: str = "User not found in database.") -> None:
        self.message: str = message
        super().__init__(self.message)


class NoMatchingEntry(Exception):
    """Problem executing a SQL command. After this exception must still come an error handling!

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str = "No entry found with specified values.") -> None:
        self.message: str = message
        super().__init__(self.message)
