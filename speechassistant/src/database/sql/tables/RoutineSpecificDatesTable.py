from src.database.sql.tables.AbstractTable import AbstractTable


class RoutineSpecificDatesTable(AbstractTable):
    table_name = "RoutineSpecificDates"
    col_id = "Id"
    col_routine_days_id = "RoutineDays"
    all_columns = [
        col_id,
        col_routine_days_id
    ]

    @staticmethod
    def create_table():
        pass
