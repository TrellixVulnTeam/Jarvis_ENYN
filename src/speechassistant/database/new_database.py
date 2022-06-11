import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.future import Engine, select
from sqlalchemy.orm import Session

from src.speechassistant.database.DataBasePersistency import DBPersistency

# toDo: add cascade in schemas where it has to
from src.speechassistant.database.schemas import alarmSchema
from src.speechassistant.models.alarm import Alarm


class DataBase:
    def __int__(self) -> None:
        logging.info("[ACTION] Initialize DataBase...\n")
        self.engine: Engine = create_engine(
            DBPersistency.DATABASE_URL, echo=True, future=True, connect_args={"check_same_thread": False}
        )

    class _AlarmInterface:
        def __init__(self, engine: Engine):
            self.engine: Engine = engine

        def create_alarm(self, alarm: Alarm) -> Alarm:
            alarm_schema: alarmSchema.AlarmSchema = self.__alarm_to_schema(alarm)
            with Session(self.engine, future=True) as session:
                session.add(alarm_schema)
                session.commit()
                return alarm_schema

        def get_alarm_by_id(self, alarm_id: int) -> Alarm:
            with Session(self.engine) as session:
                stmt = select(Alarm).where(Alarm.alarm_id == alarm_id)
                return session.scalars(stmt).one()

        def get_all_alarms(self) -> list[Alarm]:
            with Session(self.engine) as session:
                stmt = select(Alarm)
                return session.scalars(stmt)

        def update_alarm_by_id(self, alarm_id: int, alarm: Alarm):
            pass
