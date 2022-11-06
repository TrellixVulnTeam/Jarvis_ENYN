from src.database.sql.operations.AbstractInterface import AbstractInterface
from src.database.sql.operations.AbstractOperations.AbstractLoadAll import AbstractLoadAll
from src.database.sql.operations.AbstractOperations.AbstractLoadById import AbstractLoadById
from src.database.sql.tables import ReminderTable


class ReminderInterface(AbstractInterface, AbstractLoadById[ReminderTable, int, ReminderSchema],
                        AbstractLoadAll[ReminderTable, ReminderSchema]):
    pass
