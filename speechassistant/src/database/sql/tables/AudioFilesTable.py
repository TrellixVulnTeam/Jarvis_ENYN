from database.sql.tables.AbstractTable import Schema
from src.database.sql.tables.AbstractTable import AbstractTable


class AudioFilesTable(AbstractTable):
    def result_to_schema(self) -> Schema:
        pass

    table_name = "AudioFiles"
    col_id = "Id"
    col_name = "Name"
    col_data = "Data"
    all_columns = [col_id, col_name, col_data]

    @staticmethod
    def create_table():
        pass
