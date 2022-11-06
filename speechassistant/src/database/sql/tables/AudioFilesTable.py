from src.database.sql.tables.AbstractTable import AbstractTable


class AudioFilesTable(AbstractTable):
    table_name = "AudioFiles"
    col_id = "Name"
    col_data = "Data"
    all_columns = [
        col_id,
        col_data
    ]

    @staticmethod
    def create_table():
        pass
