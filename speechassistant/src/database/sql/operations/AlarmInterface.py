from database.orm.schemas.alarms import AlarmSchema
from src.database.sql.operations.AbstractInterface import AbstractInterface
from src.database.sql.operations.AbstractOperations.AbstractLoadAll import (
    AbstractLoadAll,
)
from src.database.sql.operations.AbstractOperations.AbstractLoadById import (
    AbstractLoadById,
)
from src.database.sql.tables import AlarmTable


class AlarmInterface(
    AbstractInterface,
    AbstractLoadById[AlarmTable, int, AlarmSchema],
    AbstractLoadAll[AlarmTable, AlarmSchema],
):
    pass
