import logging
import os

import sqlalchemy
from sqlalchemy.engine import Connection, Engine


class DataBase:
    __instance = None

    @staticmethod
    def get_instance():
        if DataBase.__instance is None:
            DataBase()
        return DataBase.__instance

    def __int__(self) -> None:
        if DataBase.__instance is not None:
            raise Exception("Singleton cannot be instantiated more than once!")

        logging.info("[ACTION] Initialize DataBase...\n")
        logging.info(
            "sqlite://" + os.path.dirname(os.path.realpath(__file__)).join("db.sqlite")
        )

        self.engine: Engine = sqlalchemy.create_engine(
            "sqlite://" + os.path.dirname(os.path.realpath(__file__)).join("db.sqlite")
        )
        self.db: Connection = self.engine.connect()
