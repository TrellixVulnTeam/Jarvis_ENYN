from typing import Callable

from src.database.sql.connection import DbConnection

Driver = DbConnection.get_instance().driver


class OperationHelper:
    @staticmethod
    def load_multiple_from_table_with_one_where_statement(
        table_name: str, column: str, value: any, convert_to_object: Callable
    ) -> list["Driver.Result"]:
        statement: str = f"SELECT * FROM ? WHERE ? = ?;"
        cursor: "Driver.Cursor" = Driver.cursor()
        return convert_to_object(cursor.execute(statement, table_name, column, value))
