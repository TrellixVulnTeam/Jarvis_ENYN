from src.database.sql.tables.AbstractTable import AbstractTable


class BirthdayTable(AbstractTable):
    table_name = "Birthdays"
    col_id = "Id"
    col_first_name = "FirstName"
    col_last_name = "LastName"
    col_date = "Date"
    all_columns = [
        col_id,
        col_first_name,
        col_last_name,
        col_date
    ]

    @staticmethod
    def create_table():
        pass
