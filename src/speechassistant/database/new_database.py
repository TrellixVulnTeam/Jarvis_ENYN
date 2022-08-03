import datetime
from datetime import time
from typing import Type

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src.speechassistant.database.connections.AbstractDataBaseConnection import (
    AbstractDataBaseConnection, Model, Schema,
)
from src.speechassistant.database.schemas.alarmSchema import (
    AlarmSchema,
    alarm_to_schema,
    schema_to_alarm,
)
from src.speechassistant.database.schemas.audioFileSchema import audio_file_to_schema, schema_to_audio_file, \
    AudioFileSchema
from src.speechassistant.database.schemas.birthdaySchema import BirthdaySchema, schema_to_birthday, birthday_to_schema
from src.speechassistant.database.schemas.reminderSchema import ReminderSchema, schema_to_reminder, reminder_to_schema
from src.speechassistant.database.schemas.routineSchema import RoutineSchema, schema_to_routine, routine_to_schema
from src.speechassistant.database.schemas.shoppingListSchema import ShoppingListSchema, schema_to_shopping_list, \
    shopping_list_to_schema
from src.speechassistant.database.schemas.timerSchema import TimerSchema, schema_to_timer, timer_to_schema
from src.speechassistant.database.schemas.userSchema import UserSchema, schema_to_user, user_to_schema
from src.speechassistant.models.alarm import Alarm, AlarmRepeating
from src.speechassistant.models.audio_file import AudioFile
# class DataBase:
#    def __int__(self) -> None:
#      self.engine: Engine = create_engine(
#        DBPersistency.DATABASE_URL, echo=True, future=True, connect_args={"check_same_thread": False}
#   )
from src.speechassistant.models.birthday import Birthday
from src.speechassistant.models.reminder import Reminder
from src.speechassistant.models.routine import Routine
from src.speechassistant.models.shopping_list import ShoppingListItem
from src.speechassistant.models.timer import Timer
# toDo: add cascade in schemas where it has to
from src.speechassistant.models.user import User


class _AlarmInterface(AbstractDataBaseConnection[Alarm, AlarmSchema]):

    def get_schema_type(self) -> Type[Schema]:
        return AlarmSchema

    def get_model_type(self) -> Type[Model]:
        return Alarm

    def schema_to_model(self, model_schema: AlarmSchema) -> Alarm:
        return schema_to_alarm(model_schema)

    def model_to_schema(self, model: Alarm) -> AlarmSchema:
        return alarm_to_schema(model)

    def get_model_id(self, model: Alarm) -> int:
        return model.alarm_id

    def __init__(self):
        super().__init__()

        from src.speechassistant.database.tables.alarmTables import create_tables
        create_tables(self.engine)


class _AudioFileInterface(AbstractDataBaseConnection[AudioFile, AudioFileSchema]):
    def get_model_type(self) -> Type[Model]:
        return AudioFile

    def get_schema_type(self) -> Type[Schema]:
        return AudioFileSchema

    def schema_to_model(self, model_schema: AudioFileSchema) -> AudioFile:
        return schema_to_audio_file(model_schema)

    def model_to_schema(self, model: AudioFile) -> AudioFileSchema:
        return audio_file_to_schema(model)

    def get_model_id(self, model: AudioFile) -> int:
        return model.id

    def __int__(self) -> None:
        super().__init__()
        from src.speechassistant.database.tables.audiofileTable import create_tables
        create_tables(self.engine)


class _BirthdayInterface(AbstractDataBaseConnection[Birthday, BirthdaySchema]):
    def schema_to_model(self, model_schema: Schema) -> Model:
        return schema_to_birthday(model_schema)

    def model_to_schema(self, model: Model) -> Schema:
        return birthday_to_schema(model)

    def get_model_id(self, model: Birthday) -> int:
        return -1

    def get_model_type(self) -> Type[Model]:
        return Birthday

    def get_schema_type(self) -> Type[Schema]:
        return BirthdaySchema

    def __int__(self) -> None:
        super().__init__()
        from src.speechassistant.database.tables.birthdayTable import create_tables
        create_tables(self.engine)


class _ReminderInterface(AbstractDataBaseConnection[Reminder, ReminderSchema]):
    def schema_to_model(self, model_schema: Schema) -> Model:
        return schema_to_reminder(model_schema)

    def model_to_schema(self, model: Model) -> Schema:
        return reminder_to_schema(model)

    def get_model_id(self, model: Reminder) -> int:
        return model.reminder_id

    def get_model_type(self) -> Type[Model]:
        return Reminder

    def get_schema_type(self) -> Type[Schema]:
        return ReminderSchema

    def __int__(self) -> None:
        super().__init__()
        from src.speechassistant.database.tables.reminderTable import create_tables
        create_tables(self.engine)


class _RoutineInterface(AbstractDataBaseConnection[Routine, RoutineSchema]):
    def schema_to_model(self, model_schema: Schema) -> Model:
        return schema_to_routine(model_schema)

    def model_to_schema(self, model: Model) -> Schema:
        return routine_to_schema(model)

    def get_by_id(self, model_id: int) -> Model:
        raise NotImplemented

    def get_by_name(self, model_name: str) -> Routine:
        model_schema: Schema
        with Session(self.engine) as session:
            stmt = select(self.get_schema_type()).where(self.get_schema_type().name == model_name)
            model_schema = session.execute(stmt).scalars().first()
            return self.schema_to_model(model_schema)

    def get_model_id(self, model: Model) -> int:
        return -1

    def get_model_type(self) -> Type[Model]:
        return Routine

    def get_schema_type(self) -> Type[Schema]:
        return RoutineSchema

    def __int__(self) -> None:
        super().__init__()
        from src.speechassistant.database.tables.routineTable import create_tables
        create_tables(self.engine)


class _ShoppingListInterface(AbstractDataBaseConnection[ShoppingListItem, ShoppingListSchema]):
    def schema_to_model(self, model_schema: Schema) -> Model:
        return schema_to_shopping_list(model_schema)

    def model_to_schema(self, model: Model) -> Schema:
        return shopping_list_to_schema(model)

    def get_model_id(self, model: ShoppingListItem) -> int:
        return model.id

    def get_model_type(self) -> Type[Model]:
        return ShoppingListItem

    def get_schema_type(self) -> Type[Schema]:
        return ShoppingListSchema

    def __int__(self) -> None:
        super().__init__()
        from src.speechassistant.database.tables.shoppinglistTable import create_tables
        create_tables(self.engine)


class _TimerInterface(AbstractDataBaseConnection[Timer, TimerSchema]):
    def schema_to_model(self, model_schema: Schema) -> Model:
        return schema_to_timer(model_schema)

    def model_to_schema(self, model: Model) -> Schema:
        return timer_to_schema(model)

    def get_model_id(self, model: Timer) -> int:
        return Timer.tid

    def get_model_type(self) -> Type[Model]:
        return Timer

    def get_schema_type(self) -> Type[Schema]:
        return TimerSchema

    def __int__(self) -> None:
        super().__init__()
        from src.speechassistant.database.tables.timerTable import create_tables
        create_tables(self.engine)


class _UserInterface(AbstractDataBaseConnection[User, UserSchema]):
    def schema_to_model(self, model_schema: Schema) -> Model:
        return schema_to_user(model_schema)

    def model_to_schema(self, model: Model) -> Schema:
        return user_to_schema(model)

    def get_model_id(self, model: User) -> int:
        return model.uid

    def get_model_type(self) -> Type[Model]:
        return User

    def get_schema_type(self) -> Type[Schema]:
        return UserSchema

    def __int__(self) -> None:
        super().__init__()
        from src.speechassistant.database.tables.userTable import create_tables
        create_tables(self.engine)


if __name__ == "__main__":
    interface = _AlarmInterface()

    alarm: Alarm = Alarm(
        text="Guten Morgen",
        alarm_time=time(12, 12, 12),
        repeating=AlarmRepeating(
            monday=False,
            tuesday=False,
            wednesday=False,
            thursday=True,
            friday=False,
            saturday=False,
            sunday=False,
            regular=False,
        ),
        song_name="standard",
    )
    result: Alarm = interface.create(alarm)
    print(
        "-------------------------------------------" + result.__repr__() + "-------------------------------------------")
    print("-------------------------------------------" + interface.get_by_id(
        result.alarm_id).__repr__() + "-------------------------------------------")
    result.last_executed = datetime.datetime.now()
    print("-------------------------------------------" + interface.update(
        result).__repr__() + "-------------------------------------------")
    interface.delete_by_id(result.alarm_id)
    print("-------------------------------------------" + interface.get_by_id(
        result.alarm_id).__repr__() + "-------------------------------------------")
