from sqlalchemy.orm import declarative_base


class DBPersistency:
    DATABASE_URL = "sqlite://"
    USER_NAME = ""
    PASSWORD = ""
    Base = declarative_base()
