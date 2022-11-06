from src.database.sql.tables.AbstractTable import AbstractTable


class AlarmRepeatingTable(AbstractTable):
    table_name = "AlarmRepeating"
    col_id = "AlarmId"
    col_monday = "Monday"
    col_tuesday = "Tuesday"
    col_wednesday = "Wednesday"
    col_thursday = "Thursday"
    col_friday = "Friday"
    col_saturday = "Saturday"
    col_sunday = "Sunday"
    col_regular = "Regular"
    all_columns = [
        col_id,
        col_monday,
        col_tuesday,
        col_wednesday,
        col_thursday,
        col_friday,
        col_saturday,
        col_sunday,
        col_regular
    ]

    @staticmethod
    def create_table():
        pass
