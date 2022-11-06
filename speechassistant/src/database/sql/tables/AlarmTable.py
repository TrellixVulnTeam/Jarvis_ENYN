from src.database.sql.tables.AbstractTable import AbstractTable


class AlarmsTable(AbstractTable):
    table_name = "Alarms"
    col_id = "Id"
    col_text = "Text"
    col_alarm_time = "AlarmTime"
    col_song_name = "SongName"
    col_active = "Active"
    col_initiated = "Initiated"
    col_user_id = "UserId"
    col_last_executed = "LastExecuted"
    all_columns = [
        col_id,
        col_text,
        col_alarm_time,
        col_song_name,
        col_active,
        col_initiated,
        col_user_id,
        col_last_executed
    ]

    @staticmethod
    def create_table():
        pass
