from datetime import time

from sqlalchemy import create_engine
from sqlalchemy.future import Engine, select
from sqlalchemy.orm import Session, sessionmaker

from src.speechassistant.database.DataBasePersistency import DBPersistency

# toDo: add cascade in schemas where it has to
from src.speechassistant.database.schemas.alarmSchema import (
    AlarmSchema,
    alarm_to_schema,
    schema_to_alarm,
)
from src.speechassistant.models.alarm import Alarm, AlarmRepeating
from src.speechassistant.models.audio_file import AudioFile

# class DataBase:
#    def __int__(self) -> None:
#      self.engine: Engine = create_engine(
#        DBPersistency.DATABASE_URL, echo=True, future=True, connect_args={"check_same_thread": False}
#   )


engine = create_engine(
    DBPersistency.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = DBPersistency.Base


class _AlarmInterface:
    def __int__(self) -> None:
        self.engine: Engine = create_engine(
            DBPersistency.DATABASE_URL,
            echo=True,
            future=True,
            connect_args={"check_same_thread": False},
        )

    def create_alarm(self, new_alarm: Alarm) -> Alarm:
        alarm_schema: AlarmSchema = alarm_to_schema(new_alarm)
        with Session(self.engine, future=True) as session:
            session.add(alarm_schema)
            session.commit()
            return alarm_schema

    def get_alarm_by_id(self, alarm_id: int) -> Alarm:
        with Session(self.engine) as session:
            stmt = select(AlarmSchema).where(AlarmSchema.id == alarm_id)
            return session.scalars(stmt).one()

    def get_all_alarms(self) -> list[Alarm]:
        with Session(self.engine) as session:
            stmt = select(AlarmSchema)
            return [schema_to_alarm(a) for a in session.scalars(stmt)]

    def update_alarm_by_id(self, alarm_id: int, alarm: Alarm) -> Alarm:
        alarm_schema: AlarmSchema = alarm_to_schema(alarm)
        with Session(self.engine) as session:
            stmt = select(AlarmSchema).where(AlarmSchema.id == alarm_id)
            alarm_in_db: AlarmSchema = session.scalars(stmt).one()
            alarm_in_db = alarm_schema
            session.commit()
        return schema_to_alarm(alarm_in_db)

    def delete_alarm_by_id(self, alarm_id: int) -> None:
        pass


class _AudioFileInterface:
    def __int__(self) -> None:
        self.engine: Engine = create_engine(
            DBPersistency.DATABASE_URL,
            echo=True,
            future=True,
            connect_args={"check_same_thread": False},
        )

    def create_audio_file(self) -> AudioFile:
        pass

    def get_audio_file_by_id(self, audio_file_id: int) -> AudioFile:
        pass

    def get_audio_file_by_name(self, audio_file_name: str) -> AudioFile:
        pass

    def get_all_audio_files(self) -> list[AudioFile]:
        pass

    def update_audio_file_by_id(
        self, audio_file_id: int, audio_file: AudioFile
    ) -> AudioFile:
        pass

    def delete_audio_file_by_id(self, audio_file_id: int) -> None:
        pass

    def delete_audio_file_by_name(self, audio_file_name: str) -> None:
        pass


class _BirthdayInterface:
    def __int__(self) -> None:
        self.engine: Engine = create_engine(
            DBPersistency.DATABASE_URL,
            echo=True,
            future=True,
            connect_args={"check_same_thread": False},
        )

    def create_birthday(self) -> AudioFile:
        pass

    def get_birthday_by_id(self, audio_file_id: int) -> AudioFile:
        pass

    def get_birthday_by_first_and_last_name(self, audio_file_name: str) -> AudioFile:
        pass

    def get_all_birthdays(self) -> list[AudioFile]:
        pass

    def update_birthday_by_id(
        self, audio_file_id: int, audio_file: AudioFile
    ) -> AudioFile:
        pass

    def delete_birthday_by_id(self, audio_file_id: int) -> None:
        pass

    def delete_birthday_by_first_and_last_name(self, audio_file_name: str) -> None:
        pass


class _ReminderInterface:
    def __int__(self) -> None:
        self.engine: Engine = create_engine(
            DBPersistency.DATABASE_URL,
            echo=True,
            future=True,
            connect_args={"check_same_thread": False},
        )

    def create_reminder(self) -> AudioFile:
        pass

    def get_reminder_by_id(self, audio_file_id: int) -> AudioFile:
        pass

    def get_all_reminder(self) -> list[AudioFile]:
        pass

    def update_reminder_by_id(
        self, audio_file_id: int, audio_file: AudioFile
    ) -> AudioFile:
        pass

    def delete_reminder_by_id(self, audio_file_id: int) -> None:
        pass


class _RoutineInterface:
    def __int__(self) -> None:
        self.engine: Engine = create_engine(
            DBPersistency.DATABASE_URL,
            echo=True,
            future=True,
            connect_args={"check_same_thread": False},
        )

    def create_routine(self) -> AudioFile:
        pass

    def get_routine_by_id(self, audio_file_id: int) -> AudioFile:
        pass

    def get_routine_by_name(self, audio_file_name: str) -> AudioFile:
        pass

    def get_all_routine(self) -> list[AudioFile]:
        pass

    def update_routine_by_id(
        self, audio_file_id: int, audio_file: AudioFile
    ) -> AudioFile:
        pass

    def delete_routine_by_id(self, audio_file_id: int) -> None:
        pass


class _ShoppingListInterface:
    def __int__(self) -> None:
        self.engine: Engine = create_engine(
            DBPersistency.DATABASE_URL,
            echo=True,
            future=True,
            connect_args={"check_same_thread": False},
        )

    def create_shopping_list(self) -> AudioFile:
        pass

    def get_shopping_list_by_id(self, audio_file_id: int) -> AudioFile:
        pass

    def get_shopping_list_by_name(self, audio_file_name: str) -> AudioFile:
        pass

    def update_shopping_list_by_id(
        self, audio_file_id: int, audio_file: AudioFile
    ) -> AudioFile:
        pass

    def delete_shopping_list_by_id(self, audio_file_id: int) -> None:
        pass

    def delete_shopping_list_by_name(self, audio_file_name: str) -> None:
        pass


class _TimerInterface:
    def __int__(self) -> None:
        self.engine: Engine = create_engine(
            DBPersistency.DATABASE_URL,
            echo=True,
            future=True,
            connect_args={"check_same_thread": False},
        )

    def create_timer(self) -> AudioFile:
        pass

    def get_timer_by_id(self, audio_file_id: int) -> AudioFile:
        pass

    def get_all_timer(self) -> list[AudioFile]:
        pass

    def update_timer_by_id(
        self, audio_file_id: int, audio_file: AudioFile
    ) -> AudioFile:
        pass

    def delete_timer_by_id(self, audio_file_id: int) -> None:
        pass


class _UserInterface:
    def __int__(self) -> None:
        self.engine: Engine = create_engine(
            DBPersistency.DATABASE_URL,
            echo=True,
            future=True,
            connect_args={"check_same_thread": False},
        )

    def create_user(self) -> AudioFile:
        pass

    def get_user_by_id(self, audio_file_id: int) -> AudioFile:
        pass

    def get_user_by_alias(self, audio_file_name: str) -> AudioFile:
        pass

    def get_all_user(self) -> list[AudioFile]:
        pass

    def update_user_by_id(self, audio_file_id: int, audio_file: AudioFile) -> AudioFile:
        pass

    def delete_user_by_id(self, audio_file_id: int) -> None:
        pass

    def delete_user_by_alias(self, audio_file_name: str) -> None:
        pass


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

    print(interface.create_alarm(alarm))
