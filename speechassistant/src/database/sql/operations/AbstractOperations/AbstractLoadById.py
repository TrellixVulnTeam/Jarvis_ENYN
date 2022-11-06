from abc import ABCMeta
from typing import Generic, TypeVar

from src.database.sql.connection import DbConnection

IdType = TypeVar("IdType")
Schema = TypeVar("Schema")
AbstractTable = TypeVar("AbstractTable")

Driver = DbConnection.get_instance().driver


class AbstractLoadById(metaclass=ABCMeta, Generic[AbstractTable, IdType, Schema]):
    @staticmethod
    def load_by_id(id_value: "IdType") -> Schema:
        cursor: Driver.Cursor = Driver.get_connection().cursor()
        result: Driver.Result = cursor.execute("SELECT * FROM ? WHERE ? = ?;", AbstractTable.table_name,
                                               AbstractTable.col_id, id_value)
        return Schema.from_result(result.fetchone())
