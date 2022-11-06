from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar, Type

from src.database.orm.database_persistency import OrmPersistency
from src.database.sql.tables import *

DriverType = TypeVar("DriverType")


class AbstractDriver(metaclass=ABCMeta, Generic[DriverType]):

    def __init__(self):
        self.db_persistency = OrmPersistency.get_instance()
        self.connection: DriverType = self.connect()
        self.connection_pool = None

    @property
    @abstractmethod
    def Cursor(self):
        ...

    @property
    @abstractmethod
    def Result(self):
        ...

    @abstractmethod
    def execute(self, sql: str, *args):
        ...

    @abstractmethod
    def query(self, sql: str, *args):
        ...

    @abstractmethod
    def create_table(self, table: Type[AbstractTable]):
        ...

    @abstractmethod
    def commit(self):
        ...

    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def get_connection(self):
        ...

    @abstractmethod
    def create_connection_pool(self, size: int):
        ...

    def stop(self):
        self.connection.close()

    def create_all_tables(self):
        self.create_table(AlarmRepeatingTable)
        self.create_table(AlarmsTable)
        self.create_table(AudioFilesTable)
        self.create_table(BirthdayTable)
        self.create_table(ReminderTable)
        self.create_table(RoutineCallingCommandTable)
        self.create_table(RoutineSpecificDatesTable)
        self.create_table(RoutineClockTimeTable)
        self.create_table(RoutineCommandTextTable)
        self.create_table(RoutineCommand)
        self.create_table(RoutineTable)
