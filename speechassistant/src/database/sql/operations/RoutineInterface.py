from typing import TYPE_CHECKING

from database.orm.schemas.routines import RoutineSchema
from database.sql.operations.AbstractOperations.AbstractLoadById import AbstractLoadById
from database.sql.operations.OperationHelper import OperationHelper
from database.sql.schemas import RoutineCommandSchema
from database.sql.tables import (
    RoutineTable,
    RoutineCommandTable,
    RoutineCommandTextTable,
)
from models import Routine
from src.database.sql.connection import DbConnection
from src.database.sql.operations.AbstractInterface import AbstractInterface

if TYPE_CHECKING:
    Driver = DbConnection.get_instance().driver


class RoutineInterface(AbstractInterface):
    def load_by_id(self, _id: int) -> Routine:
        