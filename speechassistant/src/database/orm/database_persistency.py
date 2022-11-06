import pathlib

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool

from src import log


class OrmPersistency:
    _INSTANCE = None

    @staticmethod
    def get_instance():
        if not OrmPersistency._INSTANCE:
            OrmPersistency._INSTANCE = OrmPersistency()
        return OrmPersistency._INSTANCE

    def __init__(self):
        if OrmPersistency._INSTANCE:
            raise RuntimeError

        self.FOLDER_PATH = pathlib.Path(__file__).parent.resolve()
        log.info(f"Using Database-File {self.FOLDER_PATH.joinpath('db.sqlite')}")
        self.DATABASE_URL = f"sqlite:///{self.FOLDER_PATH.joinpath('db.sqlite')}"
        self.USER_NAME = ""
        self.PASSWORD = ""
        self.Base = declarative_base()
        self.engine = create_engine(
            self.DATABASE_URL,
            echo=False,
            future=True,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self.meta = MetaData(self.engine)
