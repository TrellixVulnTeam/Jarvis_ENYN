from src.database.sql.tables.AbstractTable import AbstractTable


class ReminderTable(AbstractTable):
    table_name = "Reminder"
    col_id = "Id",
    col_time = "Time"
    col_text = "Text"
    col_user_id = "UserId"
    all_columns = [
        col_id,
        col_time,
        col_text,
        col_user_id
    ]

    @staticmethod
    def create_table():
        pass
