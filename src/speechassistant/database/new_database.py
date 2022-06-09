import logging
import os

import sqlalchemy
from sqlalchemy import databases

from src.speechassistant.database.DataBasePersistency import DBPersistency


class DataBase:
    def __int__(self) -> None:
        logging.info("[ACTION] Initialize DataBase...\n")
        database = databases.Database(DBPersistency.DATABASE_URL)
        metadata = sqlalchemy.MetaData()

        engine = sqlalchemy.create_engine(
            DBPersistency.DATABASE_URL, connect_args={"check_same_thread": False}
        )
        metadata.create_all(engine)
