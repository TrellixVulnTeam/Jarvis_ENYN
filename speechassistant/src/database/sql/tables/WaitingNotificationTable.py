from database.sql.tables import AbstractTable
from database.sql.tables.AbstractTable import Schema


class WaitingNotificationTable(AbstractTable):
    table_name = "WaitingNotifications"
    col_id = "Id"
    col_text = "Text"
    all_columns = [col_id, col_text]

    @staticmethod
    def create_table():
        pass

    def result_to_schema(self) -> Schema:
        pass
