import sqlite3
from typing import Type

from src.database.orm.database_persistency import OrmPersistency
from src.database.sql.driver.AbstractDriver import AbstractDriver
from src.database.sql.tables import AbstractTable


class SQLite(AbstractDriver, sqlite3.Connection):
    Cursor = sqlite3.Cursor

    def connect(self):
        return sqlite3.connect(OrmPersistency.get_instance().DATABASE_URL)

    def commit(self):
        self.connection.commit()

    def create_connection_pool(self, **kwargs):
        pass

    def get_connection(self):
        return self.connection

    def execute(self, sql: str, *args):
        return self.connection.execute(sql, args)

    def execute_many(self, sqls: list[str], args: list[tuple]):
        pass

    def query(self, sql: str, *args):
        pass

    def create_table(self, table: Type[AbstractTable]):
        self.execute(f"CREATE TABLE IF NOT EXISTS ? (?)", table.table_name, table.create_table())
