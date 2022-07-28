from abc import ABC

from database.DataBasePersistency import DBPersistency
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker


class AbstractDataBaseConnection(ABC):
    def __init__(self):
        self.meta = MetaData()

        self.engine = create_engine(
            DBPersistency.DATABASE_URL,
            echo=True,
            future=True,
            connect_args={"check_same_thread": False},
        )

        with self.engine.connect() as conn:
            self.meta.create_all(conn)

        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.Base = DBPersistency.Base
