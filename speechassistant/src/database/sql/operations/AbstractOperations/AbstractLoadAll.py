from abc import ABCMeta
from typing import Generic

from pydantic.dataclasses import TypeVar

from src.database.sql.connection import DbConnection

AbstractTable = TypeVar("AbstractTable")
Schema = TypeVar("Schema")

Driver = DbConnection.get_instance().driver


class AbstractLoadAll(metaclass=ABCMeta, Generic[AbstractTable, Schema]):
    @staticmethod
    def load_all() -> list[Schema]:
        cursor: Driver.Cursor = Driver.get_connection().cursor()
        result: Driver.Result = cursor.execute("SELECT * FROM ?;", AbstractTable.table_name)
        return [Schema.from_result(x) for x in result.fetchall()]
