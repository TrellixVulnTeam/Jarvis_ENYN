from src.database.sql.tables.AbstractTable import AbstractTable


class UserTable(AbstractTable):
    table_name = "Users"
    col_id = "Id"
    col_alias = "Alias"
    col_first_name = "FirstName"
    col_last_name = "LastName"
    col_birthday = "Birthday"
    col_messenger_id = "MessengerId"
    col_default_song_name = "DefaultSongName"
    all_columns = [
        col_id,
        col_alias,
        col_first_name,
        col_last_name,
        col_birthday,
        col_messenger_id,
        col_default_song_name
    ]

    @staticmethod
    def create_table():
        pass
