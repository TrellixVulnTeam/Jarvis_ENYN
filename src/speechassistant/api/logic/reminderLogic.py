from sqlite3 import OperationalError
from fastapi import status, HTTPException

from src.speechassistant.exceptions.SQLException import NoMatchingEntry
from src.speechassistant.models.reminder import Reminder
from src.speechassistant.database.database_connection import DataBase

reminder_interface = DataBase().reminder_interface


class ReminderLogic:
    @staticmethod
    def create_reminder(reminder: Reminder) -> Reminder:
        return reminder_interface.add_reminder(reminder)

    @staticmethod
    def read_all_reminder() -> list[Reminder]:
        return reminder_interface.get_all_reminder()

    @staticmethod
    def read_passed_reminder() -> list[Reminder]:
        return reminder_interface.get_passed_reminder()

    @staticmethod
    def read_reminder_by_id(reminder_id: int) -> list[Reminder]:
        try:
            return reminder_interface.get_reminder_by_id(reminder_id)
        except (OperationalError, NoMatchingEntry):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There is no reminder with the ID {reminder_id} in the database!",
            )

    @staticmethod
    def update_reminder(reminder: Reminder) -> Reminder:
        return None

    @staticmethod
    def delete_reminder(reminder_id: int) -> None:
        reminder_interface.delete_reminder_by_id(reminder_id)
