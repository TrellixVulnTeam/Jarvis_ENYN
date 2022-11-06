from src.database.sql.tables.AbstractTable import AbstractTable


class RoutineTable(AbstractTable):
    table_name = "Routines"
    col_id = "Name"
    col_description = "Description"
    col_monday = "Monday"
    col_tuesday = "Tuesday"
    col_wednesday = "Wednesday"
    col_thursday = "Thursday"
    col_friday = "Friday"
    col_saturday = "Saturday"
    col_sunday = "Sunday"
    col_after_alarm = "AfterAlarm"
    col_after_sunrise = "AfterSunrise"
    col_after_sunset = "AfterSunset"
    col_after_call = "AfterCall"
    all_columns = [
        col_id,
        col_description,
        col_monday,
        col_tuesday,
        col_wednesday,
        col_thursday,
        col_friday,
        col_saturday,
        col_sunday,
        col_after_alarm,
        col_after_sunrise,
        col_after_sunset,
        col_after_call
    ]

    @staticmethod
    def create_table():
        pass
