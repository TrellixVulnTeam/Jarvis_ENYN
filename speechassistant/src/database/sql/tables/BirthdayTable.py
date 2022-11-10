from database.sql.tables.AbstractTable import Schema
from src.database.sql.tables.AbstractTable import AbstractTable


class BirthdayTable(AbstractTable):
    def result_to_schema(self) -> Schema:
        pass

    table_name = "Birthdays"
    col_id = "Id"
    col_first_name = "FirstName"
    col_last_name = "LastName"
    col_date = "Date"
    all_columns = [col_id, col_first_name, col_last_name, col_date]

    @staticmethod
    def create_table():
        pass
