from abc import ABCMeta
from typing import TYPE_CHECKING

from src.database.sql.connection import DbConnection

if TYPE_CHECKING:
    Driver = DbConnection.get_instance().driver


class AbstractInterface(metaclass=ABCMeta):
    def __init__(self):
        self.connection = DbConnection.get_instance()
        self.driver = self.connection.driver
