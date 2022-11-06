from src.database.sql.driver.SQLite import SQLite


class DbConnection:
    __instance = None

    @staticmethod
    def get_instance() -> "DbConnection":
        if not DbConnection.__instance:
            DbConnection.__instance = DbConnection()
        return DbConnection.__instance

    def __init__(self):
        if DbConnection.__instance:
            raise RuntimeError
        self.driver = SQLite()
