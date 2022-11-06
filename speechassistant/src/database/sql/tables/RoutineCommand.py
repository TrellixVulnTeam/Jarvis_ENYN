from src.database.sql.tables.AbstractTable import AbstractTable


class RoutineCommand(AbstractTable):
    table_name = "RoutineCommand"
    col_id = "Id"
    col_module_name = "ModuleName"
    col_routine_name = "RoutineName"
    all_columns = [
        col_id,
        col_module_name,
        col_routine_name
    ]

    @staticmethod
    def create_table():
        pass
