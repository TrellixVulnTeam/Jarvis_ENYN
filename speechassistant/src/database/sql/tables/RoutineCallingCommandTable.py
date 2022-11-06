from src.database.sql.tables.AbstractTable import AbstractTable


class RoutineCallingCommandTable(AbstractTable):
    table_name = "RoutineCallingCommand"
    col_id = "Id"
    col_routine_name = "RoutineName"
    col_command = "Command"
    all_columns = [
        col_id,
        col_command,
        col_routine_name
    ]

    @staticmethod
    def create_table():
        pass
