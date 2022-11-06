import pathlib


class DbPersistency:
    __instance = None

    @staticmethod
    def get_instance():
        if not DbPersistency.__instance:
            DbPersistency.__instance = DbPersistency()
        return DbPersistency.__instance

    def __init__(self):
        if DbPersistency.__instance:
            raise RuntimeError

        self.DATABASE_URL = f"sqlite:///{pathlib.Path(__file__).parent.resolve().joinpath('db.sqlite')}"
        self.USER_NAME = ""
        self.PASSWORD = ""
