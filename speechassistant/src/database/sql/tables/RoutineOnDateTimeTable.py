from database.sql.tables import AbstractTable
from database.sql.tables.AbstractTable import Schema


class RoutineActivationTable(AbstractTable):
    table_name = "RoutineOnDateTime"
    col_id = "Id"
    col_month = "Month"
    col_day = "Day"
    col_time = "Time"
    all_columns = [col_id, col_month, col_day, col_time]

    @staticmethod
    def create_table():
        pass

    def result_to_schema(self) -> Schema:
        pass
