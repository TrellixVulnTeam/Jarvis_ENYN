from typing import Type

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src.database.connections.abstract_database_connection import AbstractDataBaseConnection, Model, Schema
from src.database.schemas.alarms import AlarmSchema, alarm_to_schema, schema_to_alarm
from src.database.schemas.audio_files import audio_file_to_schema, schema_to_audio_file, AudioFileSchema
from src.database.schemas.birthdays import BirthdaySchema, schema_to_birthday, birthday_to_schema
from src.database.schemas.reminder import ReminderSchema, schema_to_reminder, reminder_to_schema
from src.database.schemas.routines import RoutineSchema, schema_to_routine, routine_to_schema
from src.database.schemas.shopping_list import ShoppingListSchema, schema_to_shopping_list, shopping_list_to_schema
from src.database.schemas.timer import TimerSchema, schema_to_timer, timer_to_schema
from src.database.schemas.users import UserSchema, schema_to_user, user_to_schema
from src.models.alarm import Alarm
from src.models.audio_file import AudioFile
from src.models.birthday import Birthday
from src.models.reminder import Reminder
from src.models.routine import Routine
from src.models.shopping_list import ShoppingListItem
from src.models.timer import Timer
from src.models.user import User

# toDo: add cascade in schemas where it has to
# toDo: maybe split classes in own files


class AlarmInterface(AbstractDataBaseConnection[Alarm, AlarmSchema]):
    @staticmethod
    def get_schema_type() -> Type[Schema]:
        return AlarmSchema

    @staticmethod
    def get_model_type() -> Type[Model]:
        return Alarm

    @staticmethod
    def schema_to_model(model_schema: AlarmSchema) -> Alarm:
        return schema_to_alarm(model_schema)

    @staticmethod
    def model_to_schema(model: Alarm) -> AlarmSchema:
        return alarm_to_schema(model)

    @staticmethod
    def get_model_id(model: Alarm) -> int:
        return model.alarm_id

    def __init__(self):
        super().__init__()

        from src.database.tables.alarms import create_tables
        create_tables(self.engine)


class AudioFileInterface(AbstractDataBaseConnection[AudioFile, AudioFileSchema]):
    @staticmethod
    def get_model_type() -> Type[Model]:
        return AudioFile

    @staticmethod
    def get_schema_type() -> Type[Schema]:
        return AudioFileSchema

    @staticmethod
    def schema_to_model(model_schema: AudioFileSchema) -> AudioFile:
        return schema_to_audio_file(model_schema)

    @staticmethod
    def model_to_schema(model: AudioFile) -> AudioFileSchema:
        return audio_file_to_schema(model)

    @staticmethod
    def get_model_id(model: AudioFile) -> int:
        return model.id

    def __int__(self) -> None:
        super().__init__()
        from src.database.tables.audiofiles import create_tables
        create_tables(self.engine)


class BirthdayInterface(AbstractDataBaseConnection[Birthday, BirthdaySchema]):
    @staticmethod
    def schema_to_model(model_schema: Schema) -> Model:
        return schema_to_birthday(model_schema)

    @staticmethod
    def model_to_schema(model: Model) -> Schema:
        return birthday_to_schema(model)

    @staticmethod
    def get_model_id(model: Birthday) -> int:
        return -1

    @staticmethod
    def get_model_type() -> Type[Model]:
        return Birthday

    @staticmethod
    def get_schema_type() -> Type[Schema]:
        return BirthdaySchema

    def __int__(self) -> None:
        super().__init__()
        from src.database.tables.birthdays import create_tables
        create_tables(self.engine)


class ReminderInterface(AbstractDataBaseConnection[Reminder, ReminderSchema]):
    @staticmethod
    def schema_to_model(model_schema: Schema) -> Model:
        return schema_to_reminder(model_schema)

    @staticmethod
    def model_to_schema(model: Model) -> Schema:
        return reminder_to_schema(model)

    @staticmethod
    def get_model_id(model: Reminder) -> int:
        return model.reminder_id

    @staticmethod
    def get_model_type() -> Type[Model]:
        return Reminder

    @staticmethod
    def get_schema_type() -> Type[Schema]:
        return ReminderSchema

    def __int__(self) -> None:
        super().__init__()
        from src.database.tables.reminder import create_tables
        create_tables(self.engine)


class RoutineInterface(AbstractDataBaseConnection[Routine, RoutineSchema]):
    @staticmethod
    def schema_to_model(model_schema: Schema) -> Model:
        return schema_to_routine(model_schema)

    @staticmethod
    def model_to_schema(model: Model) -> Schema:
        return routine_to_schema(model)

    def get_by_id(self, model_id: int) -> Model:
        raise NotImplemented

    def get_by_name(self, model_name: str) -> Routine:
        model_schema: Schema
        with Session(self.engine) as session:
            stmt = select(self.get_schema_type()).where(self.get_schema_type().name == model_name)
            model_schema = session.execute(stmt).scalars().first()
            return self.schema_to_model(model_schema)

    @staticmethod
    def get_model_id(model: Model) -> int:
        return -1

    @staticmethod
    def get_model_type() -> Type[Model]:
        return Routine

    @staticmethod
    def get_schema_type() -> Type[Schema]:
        return RoutineSchema

    def __int__(self) -> None:
        super().__init__()
        from src.database.tables.routines import create_tables
        create_tables(self.engine)


class ShoppingListInterface(AbstractDataBaseConnection[ShoppingListItem, ShoppingListSchema]):
    @staticmethod
    def schema_to_model(model_schema: Schema) -> Model:
        return schema_to_shopping_list(model_schema)

    @staticmethod
    def model_to_schema(model: Model) -> Schema:
        return shopping_list_to_schema(model)

    @staticmethod
    def get_model_id(model: ShoppingListItem) -> int:
        return model.id

    @staticmethod
    def get_model_type() -> Type[Model]:
        return ShoppingListItem

    @staticmethod
    def get_schema_type() -> Type[Schema]:
        return ShoppingListSchema

    def __int__(self) -> None:
        super().__init__()
        from src.database.tables.shoppinglist import create_tables
        create_tables(self.engine)


class TimerInterface(AbstractDataBaseConnection[Timer, TimerSchema]):
    @staticmethod
    def schema_to_model(model_schema: Schema) -> Model:
        return schema_to_timer(model_schema)

    @staticmethod
    def model_to_schema(model: Model) -> Schema:
        return timer_to_schema(model)

    @staticmethod
    def get_model_id(model: Timer) -> int:
        return Timer.tid

    @staticmethod
    def get_model_type() -> Type[Model]:
        return Timer

    @staticmethod
    def get_schema_type() -> Type[Schema]:
        return TimerSchema

    def __int__(self) -> None:
        super().__init__()
        from src.database.tables.timer import create_tables
        create_tables(self.engine)


class UserInterface(AbstractDataBaseConnection[User, UserSchema]):
    @staticmethod
    def schema_to_model(model_schema: Schema) -> Model:
        return schema_to_user(model_schema)

    @staticmethod
    def model_to_schema(model: Model) -> Schema:
        return user_to_schema(model)

    @staticmethod
    def get_model_id(model: User) -> int:
        return model.uid

    @staticmethod
    def get_model_type() -> Type[Model]:
        return User

    @staticmethod
    def get_schema_type() -> Type[Schema]:
        return UserSchema

    def __int__(self) -> None:
        super().__init__()
        from src.database.tables.users import create_tables
        create_tables(self.engine)
