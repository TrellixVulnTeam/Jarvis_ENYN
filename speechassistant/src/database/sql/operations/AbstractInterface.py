from abc import ABCMeta

from src.database.sql.connection import DbConnection


class AbstractInterface(metaclass=ABCMeta):
    def __init__(self):
        self.connection = DbConnection.get_instance()
        self.driver = self.connection.driver
