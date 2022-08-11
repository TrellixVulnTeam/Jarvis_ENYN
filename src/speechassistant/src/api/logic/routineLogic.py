import traceback
from sqlite3 import OperationalError

from fastapi import HTTPException, status

from src.database.database_connection import DataBase
from src.exceptions.SQLException import NoMatchingEntry
from src.models.routine import Routine

routine_interface = DataBase().routine_interface


class RoutineLogic:
    @staticmethod
    def create_routine(routine: Routine) -> Routine:
        return routine_interface.add_routine(routine)

    @staticmethod
    def read_all_routines() -> list[Routine]:
        return routine_interface.get_routines()

    @staticmethod
    def read_routine_by_name(routine_name: str) -> Routine:
        try:
            return routine_interface.get_routine(routine_name)
        except (OperationalError, NoMatchingEntry):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There is no routine with the name {routine_name} in the database!",
            )

    @staticmethod
    def update_routine_by_name(routine_name: str, routine: Routine) -> Routine:
        try:
            return routine_interface.update_routine(routine_name, routine)
        except (OperationalError, NoMatchingEntry):
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There is no routine with the name {routine_name} in the database!",
            )

    @staticmethod
    def delete_routine_by_name(routine_name: str) -> None:
        routine_interface.delete_routine(routine_name)
