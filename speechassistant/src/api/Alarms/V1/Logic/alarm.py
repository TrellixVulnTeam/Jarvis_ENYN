from sqlite3 import OperationalError

from fastapi import HTTPException, status

from src.database.connection import AlarmInterface
from src.exceptions.sql_exception import NoMatchingEntry
from src.models.alarm import Alarm

alarm_interface: AlarmInterface = AlarmInterface()


class AlarmLogic:
    @staticmethod
    def create_alarm(alarm: Alarm) -> Alarm:
        return alarm_interface.create(alarm)

    @staticmethod
    def read_all_alarms() -> list[Alarm]:
        return alarm_interface.get_all()

    @staticmethod
    def read_alarm_by_id(alarm_id: int) -> Alarm:
        try:
            return alarm_interface.get_by_id(alarm_id)
        except (OperationalError, NoMatchingEntry):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There is no Alarm with the ID {alarm_id} in the database!",
            )

    @staticmethod
    def update_alarm(alarm: Alarm) -> Alarm:
        try:
            return alarm_interface.update(alarm)
        except (OperationalError, NoMatchingEntry):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There is no Alarm with the ID {alarm.alarm_id} in the database!",
            )

    @staticmethod
    def update_satus_of_alarm(alarm_id: int, alarm_status: bool) -> Alarm:
        try:
            return alarm_interface.update_satus_of_alarm(alarm_id, alarm_status)
        except (OperationalError, NoMatchingEntry):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There is no Alarm with the ID {alarm_id} in the database!",
            )

    @staticmethod
    def delete_alarm(alarm_id: int) -> None:
        try:
            alarm_interface.delete_by_id(alarm_id)
        except NoMatchingEntry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There is no Alarm with the ID {alarm_id} in the database!",
            )
