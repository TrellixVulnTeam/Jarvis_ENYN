from sqlalchemy.orm import declarative_base
import pathlib


class DBPersistency:
    FOLDER_PATH = pathlib.Path(__file__).parent.resolve()
    DATABASE_URL = f"sqlite:///{FOLDER_PATH.joinpath('db.sqlite')}"
    USER_NAME = ""
    PASSWORD = ""
    Base = declarative_base()
