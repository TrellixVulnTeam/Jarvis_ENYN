from src.database.sql.tables.AbstractTable import AbstractTable


class RoutineClockTimeTable(AbstractTable):
    table_name = "RoutineClockTime"
    col_id = "Id"
    col_clock_time = "ClockTime"
    col_time_id = "TimeId"
    all_columns = [
        col_id,
        col_clock_time,
        col_time_id
    ]

    @staticmethod
    def create_table():
        pass
