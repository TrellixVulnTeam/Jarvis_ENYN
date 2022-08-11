from sqlite3 import OperationalError

from fastapi import HTTPException, status

from src.database.database_connection import DataBase
from src.exceptions.SQLException import NoMatchingEntry
from src.models.alarm import Alarm

alarm_interface: any = DataBase().alarm_interface


class AlarmLogic:
    @staticmethod
    def create_alarm(alarm: Alarm) -> Alarm:
        return alarm_interface.add_alarm(alarm)

    @staticmethod
    def read_all_alarms() -> list[Alarm]:
        return alarm_interface.get_all_alarms()

    @staticmethod
    def read_alarm_by_id(alarm_id: int) -> Alarm:
        try:
            return alarm_interface.get_alarm_by_id(alarm_id)
        except (OperationalError, NoMatchingEntry):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There is no Alarm with the ID {alarm_id} in the database!",
            )

    @staticmethod
    def update_alarm(alarm: Alarm) -> Alarm:
        try:
            return alarm_interface.update_alarm(alarm)
        except (OperationalError, NoMatchingEntry):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There is no Alarm with the ID {alarm.alarm_id} in the database!",
            )

    @staticmethod
    def delete_alarm(alarm_id: int) -> None:
        if alarm_interface.delete_alarm(alarm_id) < 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There is no Alarm with the ID {alarm_id} in the database!",
            )
