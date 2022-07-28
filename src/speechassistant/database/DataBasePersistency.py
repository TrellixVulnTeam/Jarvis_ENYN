from sqlalchemy.orm import declarative_base


class DBPersistency:
    DATABASE_URL = "sqlite:///C:\\Users\\Jakob\\PycharmProjects\\Jarvis\\src\\speechassistant\\database\\db.sqlite"
    USER_NAME = ""
    PASSWORD = ""
    Base = declarative_base()
