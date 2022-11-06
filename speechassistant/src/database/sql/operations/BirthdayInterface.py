from src.database.sql.operations.AbstractInterface import AbstractInterface
from src.database.sql.operations.AbstractOperations.AbstractLoadAll import AbstractLoadAll
from src.database.sql.operations.AbstractOperations.AbstractLoadById import AbstractLoadById
from src.database.sql.tables import BirthdayTable


class BirthdayInterface(AbstractInterface, AbstractLoadById[BirthdayTable, int, BirthdaySchema],
                        AbstractLoadAll[BirthdayTable, BirthdaySchema]):
    pass
