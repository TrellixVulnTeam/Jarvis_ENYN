from database.sql.tables.AbstractTable import Schema
from src.database.sql.tables.AbstractTable import AbstractTable


class RoutineCommandTextTable(AbstractTable):
    def result_to_schema(self) -> Schema:
        pass

    table_name = "RoutineCommandTextTable"
    col_id = "Id"
    col_text = "Text"
    col_routine_command_id = "RoutineCommandId"
    all_columns = [col_id, col_text, col_routine_command_id]

    @staticmethod
    def create_table():
        pass
