from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic

Schema = TypeVar("Schema")


class AbstractTable(metaclass=ABCMeta, Generic[Schema]):
    def __init__(self):
        pass

    @property
    @abstractmethod
    def col_id(self):
        ...

    @property
    @abstractmethod
    def table_name(self):
        ...

    @property
    @abstractmethod
    def all_columns(self):
        ...

    @abstractmethod
    @staticmethod
    def create_table():
        ...

    @abstractmethod
    def result_to_schema(self) -> Schema:
        ...
