from __future__ import annotations  # compatibility for < 3.10

import base64
import io
import os
import sqlite3
from datetime import datetime, time
from sqlite3 import Connection, Cursor

from src.speechassistant.exceptions.CriticalExceptions import UnsolvableException
from src.speechassistant.exceptions.SQLException import *
from src.speechassistant.models.alarm import Alarm, AlarmRepeating
from src.speechassistant.models.audio_file import AudioFile
from src.speechassistant.models.reminder import Reminder
from src.speechassistant.models.routine import (
    Routine,
    SpecificDate,
    RoutineDays,
    RoutineCommand,
    RoutineRetakes,
    RoutineTimes,
    RoutineClockTime,
)
from src.speechassistant.models.shopping_list import ShoppingListItem
from src.speechassistant.models.timer import Timer
from src.speechassistant.models.user import User
from src.speechassistant.resources.module_skills import Skills


# toDo: as_tuple -> output_type: OutputTypes
# toDo: close cursor before raise


class DataBase:
    __instance = None

    @staticmethod
    def get_instance():
        if DataBase.__instance is None:
            DataBase()
        return DataBase.__instance

    def __init__(self) -> None:
        if DataBase.__instance is not None:
            raise Exception("Singleton cannot be instantiated more than once!")

        logging.basicConfig(level=logging.DEBUG)
        logging.info("[ACTION] Initialize DataBase...\n")
        logging.info(os.path.dirname(os.path.realpath(__file__)).join("db.sqlite"))

        self.db: Connection = sqlite3.connect(
            "C:\\Users\\Jakob\\PycharmProjects\\Jarvis\\db.sqlite",
            # os.path.dirname(os.path.realpath(__file__)).join("db.sqlite"),
            check_same_thread=False,
        )
        self.error_counter: int = 0

        self.user_interface = self._UserInterface(self.db)
        self.alarm_interface = self._AlarmInterface(self.db)
        self.timer_interface = self._TimerInterface(self.db, self.user_interface)
        self.reminder_interface = self._ReminderInterface(self.db, self.user_interface)
        self.quiz_interface = self._QuizInterface(self.db)
        self.shoppinglist_interface = self._ShoppingListInterface(self.db)
        self.routine_interface = self._RoutineInterface(self.db)
        self.audio_interface = self._AudioInterface(self.db)
        self.messenger_interface = self._MessangerInterface()
        self.birthday_interface = self._BirthdayInterface(self.db)
        self.__audio_path: str = ""

        self.create_tables()

        DataBase.__instance = self

        logging.info("[INFO] DataBase successfully initialized.")

    def close(self):
        self.db.close()
        DataBase.__instance = None
        logging.info("[ACTION] DataBase closed!")

    def create_tables(self) -> None:
        # toDo: CONSTRAINTS

        # CHECK (mycolumn IN (0, 1)) -> BOOL

        logging.info("[ACTION] Create tables...")
        self.__create_table(
            "CREATE TABLE IF NOT EXISTS audio ("
            "name VARCHAR(30) PRIMARY KEY UNIQUE,"
            "data BLOB)"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS user ("
            "uid INTEGER PRIMARY KEY,"
            "alias VARCHAR(10) UNIQUE,"
            "firstname VARCHAR(15),"
            "lastname VARCHAR(30),"
            "birthday VARCHAR(10),"
            "mid INTEGER,"
            "sname VARCHAR(30),"
            "FOREIGN KEY(sname) REFERENCES audio(name))"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS alarm ("
            "aid INTEGER PRIMARY KEY, "
            "sname VARCHAR(30), "
            "uid INTEGER, "
            "time Time, "
            "text VARCHAR(255), "
            "active INTEGER, "
            "initiated INTEGER, "
            "last_executed VARCHAR(10), "
            "FOREIGN KEY(sname) REFERENCES audio(name), "
            "FOREIGN KEY(uid) REFERENCES user(uid))"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS alarmrepeat ("
            "aid INTEGER PRIMARY KEY UNIQUE,"
            "monday INTEGER,"
            "tuesday INTEGER,"
            "wednesday INTEGER,"
            "thursday INTEGER,"
            "friday INTEGER ,"
            "saturday INTEGER,"
            "sunday INTEGER, "
            "regular INTEGER, "
            "FOREIGN KEY(aid) REFERENCES alarm(aid))"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS timer ("
            "id INTEGER PRIMARY KEY,"
            "duration VARCHAR(50), "
            "time VARCHAR(25),"
            "text VARCHAR(255),"
            "uid INTEGER,"
            "FOREIGN KEY(uid) REFERENCES user(uid))"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS shoppinglist ("
            "id INTEGER PRIMARY KEY,"
            "name varchar(50) UNIQUE,"
            "measure varchar(4),"
            "quantity FLOAT)"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS reminder ("
            "id INTEGER PRIMARY KEY,"
            "time VARCHAR(19),"
            "text VARCHAR(255),"
            "uid INTEGER,"
            "FOREIGN KEY(uid) REFERENCES user(uid))"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS routine ("
            "name VARCHAR(50) PRIMARY KEY, "
            "description VARCHAR(255), "
            "daily INTEGER, "
            "monday INTEGER, "
            "tuesday INTEGER, "
            "wednesday INTEGER, "
            "thursday INTEGER, "
            "friday INTEGER, "
            "saturday INTEGER, "
            "sunday INTEGER, "
            "afteralarm INTEGER, "
            "aftersunrise INTEGER, "
            "aftersunset INTEGER, "
            "aftercall INTEGER)"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS oncommand ( "
            "ocid INTEGER PRIMARY KEY, "
            "rname VARCHAR(50), "
            "command VARCHAR(255), "
            "FOREIGN KEY(rname) REFERENCES routine(rname)"
            "UNIQUE (rname, command))"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS routineactivationtime ("
            "ratid INTEGER PRIMARY KEY, "
            "rname VARCHAR(50), "
            "hour INTEGER, "
            "minute INTEGER, "
            "FOREIGN KEY(rname) REFERENCES routine(rname), "
            "UNIQUE (rname, hour, minute))"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS routinedates ("
            "rdid INTEGER PRIMARY KEY, "
            "rname VARCHAR(50), "
            "day INTEGER, "
            "month INTEGER, "
            "UNIQUE (rname, day, month), "
            "FOREIGN KEY(rname) REFERENCES routine(rname))"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS routinecommands ("
            "rcid INTEGER PRIMARY KEY, "
            "rname VARCHAR(50), "
            "modulename VARCHAR(50), "
            "FOREIGN KEY(rname) REFERENCES routine(rname))"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS commandtext ("
            "cid INTEGER,"
            "text VARCHAR(255) NOT NULL,"
            "PRIMARY KEY(cid, text),"
            "FOREIGN KEY(cid) REFERENCES routinecommands(rcid), "
            "UNIQUE(cid, text))"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS quiz (" "category VARCHAR(50) PRIMARY KEY)"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS questions ("
            "qid INTEGER PRIMARY KEY,"
            "category REFERENCES quiz(category),"
            "starting INTEGER,"
            "question VARCHAR(255),"
            "audio VARCHAR(30),"
            "answer VARCHAR(255),"
            "FOREIGN KEY(audio) REFERENCES audio(name))"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS answeroptions ("
            "category REFERENCES quiz(category),"
            "text VARCHAR(255),"
            "PRIMARY KEY(category, text))"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS notification ("
            "uid INTEGER,"
            "text VARCHAR(255),"
            "PRIMARY KEY(uid, text),"
            "FOREIGN KEY(uid) REFERENCES user(uid))"
        )

        # self.__create_table('CREATE TABLE IF NOT EXISTS messenger notifications')
        self.__create_table(
            "CREATE TABLE IF NOT EXISTS birthdays ("
            "firstname VARCHAR(15), "
            "lastname VARCHAR(30), "
            "day INTEGER, "
            "month INTEGER, "
            "year INTEGER, "
            "PRIMARY KEY(firstname, lastname), "
            "UNIQUE (firstname, lastname))"
        )

        # #self.db.commit()

        if self.error_counter == 0:
            logging.info("[INFO] Tables successfully created!")
        else:
            msg: str = (
                f"During the creation of {self.error_counter} tables there were problems. Manual intervention "
                f"mandatory. "
            )
            raise UnsolvableException(msg)

    def __create_table(self, command: str) -> None:
        cursor: Cursor = self.db.cursor()
        try:
            cursor.execute(command)
            logging.info(f"[INFO] Successfully created table {command.split(' ')[5]}!")
        except Exception as e:
            self.error_counter += 1
            logging.warning(
                f"[ERROR] Couldn't create table {command.split(' ')[5]}:\n {e}"
            )
        cursor.close()
        self.db.commit()

    def __remove_tables(self):
        pass

    def stop(self):
        logging.info("[ACTION] Stopping database...")
        self.db.commit()
        self.db.close()

    class _UserInterface:
        def __init__(self, db: Connection) -> None:
            self.db: Connection = db
            logging.info("[INFO] UserInterface initialized.")

        def get_user_by_id(self, user_id: int) -> User:
            with self.db.cursor() as cursor:
                statement: str = f"SELECT * from user WHERE uid=? LIMIT 1"
                cursor.execute(statement, (user_id,))

                user: User = self.__tuple_to_user(cursor.fetchone())
                return user

        def get_user_by_messenger_id(self, messenger_id: int) -> User:
            with self.db.cursor() as cursor:
                statement: str = "SELECT * FROM user WHERE mid=? LIMIT 1"
                cursor.execute(statement, (messenger_id,))
                user: User = self.__tuple_to_user(cursor.fetchone())
                return user

        def get_user_by_alias(self, alias: str) -> User:
            with self.db.cursor() as cursor:
                statement: str = "SELECT * FROM user WHERE alias=? LIMIT 1"
                cursor.execute(statement, (alias,))
                user: User = self.__tuple_to_user(cursor.fetchone())
                return user

        def get_user_by_first_and_last_name(
            self, first_name: str, last_name: str
        ) -> User:
            with self.db.cursor() as cursor:
                statement: str = (
                    "SELECT * FROM user WHERE firstname=? AND lastname=? LIMIT 1"
                )
                cursor.execute(statement, (first_name, last_name))
                user: User = self.__tuple_to_user(cursor.fetchone())
                return user

        def get_users(self) -> list[User]:
            with self.db.cursor() as cursor:
                statement: str = "SELECT * from user"
                cursor.execute(statement)
                result_set: list = cursor.fetchall()

                user_list: list[User] = [
                    self.__tuple_to_user(item) for item in result_set
                ]

                for user in user_list:
                    notification_statement: str = (
                        f"SELECT text FROM notification WHERE uid=?"
                    )
                    cursor.execute(notification_statement, (user.uid,))
                    user.waiting_notifications = [x[0] for x in cursor.fetchall()]
                return user_list

        def add_user(self, user: User) -> User:
            with self.db.cursor() as cursor:
                statement: str = (
                    f"INSERT INTO user (alias, firstname, lastname, birthday, mid, sname) "
                    f"VALUES (?, ?, ?, ?, ?, ?)"
                )
                cursor.execute(
                    statement,
                    (
                        user.alias,
                        user.first_name,
                        user.last_name,
                        user.birthday.isoformat(),
                        user.messenger_id,
                        user.song_name,
                    ),
                )
                user.uid = cursor.lastrowid
                self.db.commit()
                return user

        def add_user_notification_by_user_id(
            self, user_id: int, notification: str
        ) -> None:
            with self.db.cursor() as cursor:
                statement: str = f"INSERT INTO notification (uid, text) VALUES (?, ?)"
                cursor.execute(statement, (user_id, notification))
                self.db.commit()

        def add_use_notification_by_user_alias(
            self, user_alias: str, notification: str
        ) -> None:
            user_id: int = self.__get_user_id_by_alias(user_alias)
            self.add_user_notification_by_user_id(user_id, notification)

        def update_user(self, user: User) -> User:
            with self.db.cursor() as cursor:
                statement: str = """UPDATE user 
                                    SET alias=?, firstname=?, lastname=?, 
                                    birthday=?, mid=?, sname=? 
                                    WHERE uid=?"""
                cursor.execute(
                    statement,
                    (
                        user.alias,
                        user.first_name,
                        user.last_name,
                        user.birthday,
                        user.messenger_id,
                        user.song_name,
                        user.uid,
                    ),
                )
                self.db.commit()
                return user

        def delete_user_notification_by_id(self, user: int, text: str) -> None:
            with self.db.cursor() as cursor:
                statement: str = "DELETE FROM notification WHERE uid=? AND text=?"
                cursor.execute(statement, (user, text))
                self.db.commit()

        def delete_user_notification_by_alias(self, alias: str, text: str) -> None:
            user_id: int = self.__get_user_id_by_alias(alias)
            self.delete_user_notification_by_id(user_id, text)

        def delete_user_by_id(self, user_id: int) -> None:
            with self.db.cursor() as cursor:
                statement: str = "DELETE FROM user WHERE uid=?"
                cursor.execute(statement, (user_id,))
                self.db.commit()

        def delete_user_by_alias(self, alias: str) -> None:
            user_id: int = self.__get_user_id_by_alias(alias)
            self.delete_user_by_id(user_id)

        @staticmethod
        def __birthday_to_string(birthday: datetime) -> str:
            return birthday.isoformat()

        def __get_user_id_by_alias(self, alias: str) -> int:
            with self.db.cursor() as cursor:
                statement: str = "SELECT uid FROM user WHERE alias=? LIMIT 1"
                cursor.execute(statement, (alias,))
                uid: int = cursor.fetchone()
                if uid:
                    return uid
                else:
                    raise UserNotFountException()

        def __get_user_id_by_first_and_last_name(
            self, first_name: str, last_name: str
        ) -> int:
            with self.db.cursor() as cursor:
                statement: str = (
                    "SELECT uid FROM user WHERE firstname=? AND lastname=? LIMIT 1"
                )
                cursor.execute(statement, (first_name, last_name))
                uid: int = cursor.fetchone()
                if uid:
                    return uid
                else:
                    raise UserNotFountException()

        def __create_table(self):
            pass

        @staticmethod
        def __tuple_to_user(result_set: tuple) -> User:
            (
                uid,
                alias,
                first_name,
                last_name,
                birthday,
                messenger_id,
                song_name,
            ) = result_set
            return User(
                uid, alias, first_name, last_name, birthday, messenger_id, song_name
            )

    class _AlarmInterface:
        def __init__(self, _db: Connection) -> None:
            self.db: Connection = _db
            self.skills = Skills()
            logging.info("[INFO] AlarmInterface initialized.")

        def get_alarm_by_id(self, aid: int) -> Alarm:
            with self.db.cursor() as cursor:
                statement: str = "SELECT * FROM alarm as a JOIN alarmrepeat as ar ON a.aid=ar.aid WHERE a.aid=? LIMIT 1"
                cursor.execute(statement, (aid,))
                return self.__tuple_to_alarm(cursor.fetchone())

        def get_active_and_init_alarms(self) -> tuple[list[Alarm], list[Alarm]]:
            now: datetime = datetime.now()
            weekday: str = self.skills.statics.numb_to_day[str(now.weekday())]
            now_seconds = now.hour * 3600 + now.minute * 60 + now.second
            active_alarms = self.get_active_and_passed_alarms(now, weekday)
            init_alarms = self.get_initiated_alarms(now_seconds, weekday)

            return active_alarms, init_alarms

        def get_active_and_passed_alarms(self, now, weekday) -> list[Alarm]:
            with self.db.cursor() as cursor:
                active_alarms_statement: str = (
                    f"SELECT * FROM alarm as a "
                    f"JOIN alarmrepeat as ar ON a.aid = ar.aid "
                    f"WHERE ar.{weekday}=1 "
                    f"AND a.hour >= ? "
                    f"AND a.minute >= ? "
                    f"AND a.active = 1 "
                    f"AND a.last_executed != ?"
                )
                cursor.execute(
                    active_alarms_statement,
                    (now.hour, now.minute, f"{now.day}.{now.month}.{now.year}"),
                )
                active_alarms: list[Alarm] = [
                    self.__tuple_to_alarm(alarm) for alarm in cursor.fetchall()
                ]
                return active_alarms

        def get_initiated_alarms(self, now_seconds, weekday) -> list[Alarm]:
            with self.db.cursor() as cursor:
                init_alarms_statement: str = (
                    f"SELECT * FROM alarm as a "
                    f"JOIN alarmrepeat as ar ON a.aid = ar.aid "
                    f"WHERE ar.{weekday} = 1 "
                    f"AND a.total_seconds <= {now_seconds + 1800}"
                )
                cursor.execute(init_alarms_statement)
                init_alarms: list[Alarm] = [
                    self.__tuple_to_alarm(alarm) for alarm in cursor.fetchall()
                ]
                return init_alarms

        def get_all_alarms(self) -> list[Alarm]:
            with self.db.cursor() as cursor:
                statement: str = (
                    "SELECT * FROM alarm as a "
                    "JOIN alarmrepeat as ar ON a.aid = ar.aid"
                )
                cursor.execute(statement)
                return [self.__tuple_to_alarm(alarm) for alarm in cursor.fetchall()]

        def get_alarms_unfiltered(self, active: bool) -> list[Alarm]:
            with self.db.cursor() as cursor:
                statement: str = (
                    "SELECT * FROM alarm as a JOIN alarmrepeat as ar ON a.aid=ar.aid"
                )
                if active:
                    statement = f"{statement} WHERE a.active=True"
                cursor.execute(statement)
                return [self.__tuple_to_alarm(alarm) for alarm in cursor.fetchall()]

        def add_alarm(self, alarm: Alarm) -> Alarm:
            alarm_id = self.__add_alarm_into_db(
                alarm.active,
                alarm.alarm_time.isoformat(),
                alarm.initiated,
                alarm.song_name,
                alarm.text,
                alarm.user_id,
            )
            self.__add_alarm_repeating_into_db(alarm_id, alarm.repeating)
            self.db.commit()
            alarm.aid = alarm_id

            return alarm

        def __add_alarm_repeating_into_db(
            self, alarm_id: int, repeating: AlarmRepeating
        ) -> None:
            with self.db.cursor() as cursor:
                statement: str = (
                    f"INSERT INTO alarmrepeat VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                )
                cursor.execute(
                    statement,
                    (
                        alarm_id,
                        repeating.monday,
                        repeating.tuesday,
                        repeating.wednesday,
                        repeating.thursday,
                        repeating.friday,
                        repeating.saturday,
                        repeating.sunday,
                        repeating.regular,
                    ),
                )

        def __add_alarm_into_db(
            self, active, alarm_time, initiated, song, text, user
        ) -> int:
            with self.db.cursor() as cursor:
                statement: str = """INSERT INTO alarm (sname, uid, hour, minute, total_seconds, text, active, 
                                    initiated, last_executed) 
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, "")"""
                cursor.execute(
                    statement,
                    (
                        song,
                        user,
                        alarm_time["hour"],
                        alarm_time["minute"],
                        alarm_time["total_seconds"],
                        text,
                        int(active),
                        int(initiated),
                    ),
                )
                return cursor.lastrowid

        def delete_alarm(self, aid: int) -> int:
            with self.db.cursor() as cursor:
                statement: str = "DELETE FROM alarm WHERE aid=?"
                cursor.execute(statement, (aid,))
                anz_removed_alarm: int = cursor.rowcount
                statement = "DELETE FROM alarmrepeat WHERE aid=?"
                cursor.execute(statement, (aid,))
                anz_removed_repeat: int = cursor.rowcount

                if anz_removed_alarm != anz_removed_repeat:
                    self.db.rollback()
                    raise UnsolvableException(
                        "Removed more alarm repeating´s than alarms!"
                    )
                self.db.commit()
                return anz_removed_alarm

        def update_alarm(self, alarm: Alarm):
            with self.db.cursor() as cursor:
                statement: str = (
                    f"UPDATE alarm SET sname=?, uid=?, time=?, text=?, active=?, "
                    f"initiated=?, last_executed=? WHERE aid=?"
                )
                cursor.execute(
                    statement,
                    (
                        alarm.song_name,
                        alarm.user_id,
                        alarm.alarm_time,
                        alarm.text,
                        alarm.active,
                        alarm.initiated,
                        alarm.last_executed,
                        alarm.aid,
                    ),
                )
                alarm_repeat: AlarmRepeating = alarm.repeating
                statement: str = (
                    f"UPDATE alarmrepeat "
                    f"SET monday=?, tuesday=?, wednesday=?, thursday=?, friday=?, saturday=?, sunday=? "
                    f"WHERE aid=?"
                )
                cursor.execute(
                    statement,
                    (
                        alarm_repeat.monday,
                        alarm_repeat.tuesday,
                        alarm_repeat.wednesday,
                        alarm_repeat.thursday,
                        alarm_repeat.friday,
                        alarm_repeat.saturday,
                        alarm_repeat.sunday,
                        alarm_repeat.regular,
                        alarm.aid,
                    ),
                )

            self.db.commit()
            return alarm

        @staticmethod
        def __tuple_to_alarm(alarm: tuple) -> Alarm:
            (
                alarm_id,
                song_name,
                user_id,
                alarm_time,
                text,
                active,
                initiated,
                last_executed,
                _,
                monday,
                tuesday,
                wednesday,
                thursday,
                friday,
                saturday,
                sunday,
                regular,
            ) = alarm
            repeating: AlarmRepeating = AlarmRepeating(
                monday, tuesday, wednesday, thursday, friday, saturday, sunday, regular
            )
            return Alarm(
                alarm_id,
                repeating,
                song_name,
                time.fromisoformat(alarm_time),
                text,
                active,
                initiated,
                last_executed,
                user_id,
            )

        def __create_table(self):
            pass

    class _AudioInterface:
        def __init__(self, _db: Connection) -> None:
            self.db: Connection = _db
            self.audio_path: str = "C:\\Users\\Jakob\\PycharmProjects\\Jarvis"
            logging.info("[INFO] AudioInterface initialized.")

        def add_audio(self, name: str, audio_file: io.BytesIO = None) -> str:
            with self.db.cursor() as cursor:
                statement: str = "INSERT INTO audio (name, path) VALUES (?, ?)"
                encoded_data = base64.b64decode(audio_file.read())
                cursor.execute(statement, (name, encoded_data))
                self.db.commit()
                return name

        def update_audio_file(self, old_name: str, audio_file: AudioFile) -> None:
            with self.db.cursor() as cursor:
                statement: str = "UPDATE audio SET name=?, data=? WHERE name=?"
                cursor.execute(statement, (audio_file.name, audio_file.data, old_name))
                self.db.commit()

        def get_audio_file_by_name(self, audio_name: str) -> AudioFile:
            with self.db.cursor() as cursor:
                statement: str = "SELECT * FROM audio WHERE name=?"
                cursor.execute(statement, (audio_name,))
                return self.__tuple_to_audio_file(cursor.fetchone())

        def get_file_names(self) -> list[str]:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT name FROM audio"
            cursor.execute(statement)
            result_set: list[tuple] = cursor.fetchall()
            cursor.close()
            # return only filenames
            return [x[0] for x in result_set]

        def delete_audio(self, audio_name: str) -> int:
            with self.db.cursor() as cursor:
                statement: str = "SELECT path FROM audio WHERE name=?"
                cursor.execute(statement, (audio_name,))
                statement = "DELETE FROM audio WHERE name=?"
                cursor.execute(statement, (audio_name,))
                return cursor.rowcount

        @staticmethod
        def __tuple_to_audio_file(result_set: tuple) -> AudioFile:
            name, data = result_set
            return AudioFile(name, data)

    class _TimerInterface:
        def __init__(self, _db: Connection, user_interface) -> None:
            self.db: Connection = _db
            self.user_interface = user_interface
            logging.info("[INFO] TimerInterface initialized.")

        def get_all_timer(self) -> list[Timer]:
            with self.db.cursor() as cursor:
                statement: str = f"SELECT * FROM timer"
                cursor.execute(statement)
                result_set: list = cursor.fetchall()
                return [self.__tuple_to_timer(timer) for timer in result_set]

        def get_timer_of_user_by_user_id(self, user: int) -> list[Timer]:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM timer WHERE uid=?"
            cursor.execute(statement, (user,))
            return [self.__tuple_to_timer(alarm) for alarm in cursor.fetchall()]

        def get_timer_of_user_by_user_alias(self, user_alias: str) -> list[Timer]:
            user_id: int = self.user_interface.__get_user_id(user_alias)
            return self.get_timer_of_user_by_user_id(user_id)

        def get_timer_by_id(self, timer_id: int) -> Timer:
            with self.db.cursor() as cursor:
                statement: str = f"SELECT * FROM timer WHERE id=? LIMIT 1"
                cursor.execute(statement, (timer_id,))
                return self.__tuple_to_timer(cursor.fetchone())

        def add_timer(self, timer: Timer) -> int:
            with self.db.cursor() as cursor:
                statement: str = (
                    f"INSERT INTO timer (duration, time, text, uid) "
                    f"VALUES(?, ?, ?, ?)"
                )
                cursor.execute(
                    statement,
                    (timer.duration, timer.start_time, timer.text, timer.user.uid),
                )
                result_set: int = cursor.rowcount
                statement = "SELECT id FROM timer LIMIT 1"
                cursor.execute(statement)
                self.db.commit()
                # id from inserted timer - id from the first timer in the current database +1
                return result_set - cursor.rowcount + 1

        def update_timer(self, timer: Timer) -> Timer:
            with self.db.cursor() as cursor:
                statement: str = """UPDATE timer 
                                    SET duration=?, time=?, text=?, uid=? 
                                    WHERE id=?"""
                cursor.execute(
                    statement,
                    (
                        timer.duration,
                        timer.start_time,
                        timer.text,
                        timer.user.uid,
                        timer.tid,
                    ),
                )
                self.db.commit()
                return timer

        def delete_timer(self, timer_id: int) -> None:
            with self.db.cursor() as cursor:
                statement: str = "DELETE FROM timer WHERE id=?"
                cursor.execute(statement, (timer_id,))

        def delete_passed_timer(self) -> int:
            with self.db.cursor() as cursor:
                statement: str = "DELETE FROM timer WHERE time < ?"
                now: datetime = datetime.now()
                cursor.execute(
                    statement, time(now.hour, now.minute, now.second).isoformat()
                )
                return cursor.rowcount

        @staticmethod
        def __tuple_to_timer(result_set: tuple) -> Timer:
            timer_id, duration, start_time, text, user = result_set
            return Timer(timer_id, duration, start_time, text, user)

        def __create_table(self):
            pass

    class _ReminderInterface:
        def __init__(self, _db: Connection, user_interface) -> None:
            self.db: Connection = _db
            self.user_interface = (
                user_interface  # connection is necessary for get_user_by_id()
            )
            logging.info("[INFO] ReminderInterface initialized.")

        def get_passed_reminder(self) -> list[Reminder]:
            with self.db.cursor() as cursor:
                now: datetime = datetime.now()
                date_string: str = now.strftime("%Y.%d.%m:%H:%M:%S")
                statement: str = "SELECT * FROM reminder as r JOIN user as u ON r.id = u.id WHERE time<?"
                cursor.execute(statement, (date_string,))
                return [
                    self.__tuple_to_reminder(reminder) for reminder in cursor.fetchall()
                ]

        def get_all_reminder(self) -> list[Reminder]:
            with self.db.cursor() as cursor:
                statement: str = "SELECT * FROM reminder"
                cursor.execute(statement)
                return [
                    self.__tuple_to_reminder(reminder) for reminder in cursor.fetchall()
                ]

        def add_reminder(self, reminder: Reminder) -> int:
            with self.db.cursor() as cursor:
                statement: str = (
                    f"INSERT INTO reminder (time, text, uid) VALUES (?, ?, ?)"
                )
                cursor.execute(
                    statement, (reminder.time, reminder.text, reminder.user.uid)
                )
                rid: int = cursor.lastrowid
                self.db.commit()
                return rid

        def delete_reminder_by_id(self, _id: int) -> int:
            statement: str = "DELETE FROM reminder WHERE id=?"
            return self.__delete_reminder_by_statement(statement, (_id,))

        def delete_reminder_by_time(self, _time: str) -> int:
            statement: str = "DELTE FROM reminder WHERE time=?"
            return self.__delete_reminder_by_statement(statement, (_time,))

        def __delete_reminder_by_statement(self, statement: str, values: tuple) -> int:
            with self.db.cursor() as cursor:
                cursor.execute(statement, values)
                counter: int = cursor.rowcount
                self.db.commit()
                return counter

        def __tuple_to_reminder(self, result_set: tuple) -> Reminder:
            (reminder_id, reminder_time, text, user_id) = result_set
            user: User = self.user_interface.get_user_by_id(user_id)
            return Reminder(reminder_id, reminder_time, text, user)

        def __create_table(self):
            pass

    class _ShoppingListInterface:
        def __init__(self, _db: Connection) -> None:
            self.db: Connection = _db
            logging.info("[INFO] ShoppingListInterface initialized.")

        def get_list(self) -> list[ShoppingListItem]:
            with self.db.cursor() as cursor:
                statement: str = "SELECT * FROM shoppinglist"
                cursor.execute(statement)
                return self.__tuple_to_shopping_list(cursor.fetchall())

        def get_item(self, name: str) -> ShoppingListItem:
            with self.db.cursor() as cursor:
                statement: str = "SELECT * FROM shoppinglist WHERE name=?"
                cursor.execute(statement, (name,))
                return self.__tuple_to_shopping_list_item(cursor.fetchone())

        def add_item(self, item: ShoppingListItem) -> int:
            with self.db.cursor() as cursor:
                statement: str = f"INSERT INTO shoppinglist (name, measure, quantity) VALUES (?, ?, ?)"
                cursor.execute(statement, (item.name, item.measure, item.quantity))
                self.db.commit()
                return cursor.lastrowid

        def update_item(self, item: ShoppingListItem) -> ShoppingListItem:
            with self.db.cursor() as cursor:
                statement: str = """UPDATE shoppinglist 
                                    SET name=?, measure=?, quantity=?  
                                    WHERE name=?"""
                cursor.execute(statement, (item.name, item.measure, item.quantity))
                self.db.commit()
                return item

        def remove_item_by_id(self, item_id: int) -> None:
            statement: str = "DELETE FROM shoppinglist WHERE id=?"
            self.__remove_item_by_statement(statement, (item_id,))

        def remove_item_by_name(self, name: str) -> None:
            statement: str = "DELETE FROM shoppinglist WHERE name=?"
            self.__remove_item_by_statement(statement, (name,))

        def __remove_item_by_statement(self, statement: str, values: tuple) -> None:
            with self.db.cursor() as cursor:
                cursor.execute(statement, values)
                self.db.commit()

        def clear_list(self) -> None:
            with self.db.cursor() as cursor:
                statement: str = "DELETE FROM shoppinglist"
                cursor.execute(statement)
                self.db.commit()

        def is_item_in_list(self, name: str) -> bool:
            with self.db.cursor() as cursor:
                statement: str = f"SELECT 1 FROM shoppinglist WHERE name=? LIMIT 1"
                cursor.execute(statement, (name,))
                return cursor.rowcount == 1

        def __create_table(self):
            pass

        def __tuple_to_shopping_list(
            self, result_set: list[tuple]
        ) -> list[ShoppingListItem]:
            return [self.__tuple_to_shopping_list_item(item) for item in result_set]

        @staticmethod
        def __tuple_to_shopping_list_item(item: tuple) -> ShoppingListItem:
            name, measure, quantity = item
            return ShoppingListItem(name=name, measure=measure, quantity=quantity)

    class _RoutineInterface:
        def __init__(self, _db: Connection) -> None:
            self.db: Connection = _db
            logging.info("[INFO] RoutineInterface initialized.")

        def get_routine(self, name: str) -> Routine:
            with self.db.cursor() as cursor:
                statement: str = "SELECT * FROM routine WHERE name=? LIMIT 1"
                cursor.execute(statement)
                return self.__tuple_to_routine(cursor.fetchone())

        def get_routines(self, on_command: str = None, on_time: dict = None) -> list:
            cursor: Cursor = self.db.cursor()
            routine_list: list[dict] = []
            if on_command is not None:
                statement: str = """SELECT * FROM routine 
                                    JOIN oncommand ON routine.name=oncommand.rname 
                                    WHERE instr(?, oncommand.command) > 0"""

                cursor.execute(statement, (on_command,))
                routine_set: list[tuple] = cursor.fetchall()
            elif on_time is not None:
                statement: str = """SELECT * FROM routine"""
                cursor.execute(statement)
                routine_set: list[tuple] = cursor.fetchall()
            else:
                statement: str = """SELECT * FROM routine"""
                cursor.execute(statement)
                routine_set: list[tuple] = cursor.fetchall()

            for rout in routine_set:
                statement: str = "SELECT * FROM routinecommands WHERE rname=?"
                cursor.execute(statement, (rout[0],))
                command_set: list[tuple] = cursor.fetchall()
                text_set: list[tuple] = []
                for command in command_set:
                    statement = "SELECT * FROM commandtext WHERE cid=?"
                    cursor.execute(statement, (command[0],))
                    for item in cursor.fetchall():
                        text_set.append(item)

                statement = "SELECT * FROM routinedates WHERE rname=?"
                cursor.execute(statement, (rout[0],))
                data_set: list[tuple] = cursor.fetchall()

                statement = "SELECT * FROM routineactivationtime WHERE rname=?"
                cursor.execute(statement, (rout[0],))
                activation_set: list[tuple] = cursor.fetchall()

                statement = "SELECT command FROM oncommand WHERE rname=?"
                cursor.execute(statement, (rout[0],))
                on_command_set: list[tuple] = cursor.fetchall()

                # print(f'rout: {rout}, command_set: {command_set}, text_set: {text_set}, date_set: {data_set}, activation_set: {activation_set}, on_command_set: {on_command_set}')
                routine_list.append(
                    self.__build_json(
                        rout,
                        command_set,
                        text_set,
                        data_set,
                        activation_set,
                        on_command_set,
                    )
                )

            cursor.close()
            return routine_list

        def get_routine_command(self, rcid: int) -> dict:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM routinecommand WHERE rcid=? LIMIT 1"
            cursor.execute(statement, (rcid,))
            rcid, rname, modulename = cursor.fetchone()
            statement = "SELECT * FROM commandtext WHERE rcid=?"
            commands: list[tuple] = cursor.fetchall()
            cursor.execute(statement, (rcid,))
            cursor.close()
            return {
                "id": rcid,
                "rname": rname,
                "modulename": modulename,
                "text": [text for _, text in commands],
            }

        def get_routine_dates(self, rdid: int) -> dict:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM routinedates WHERE rdid=? LIMIT 1"
            cursor.execute(statement, (rdid,))
            rdid, rname, day, month = cursor.fetchone()
            cursor.close()
            return {"id": rdid, "rname": rname, "day": day, "month": month}

        def get_on_command(self, ocid: int) -> dict:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM oncommand WHERE ocid=?"
            cursor.execute(statement, (ocid,))
            ocid, rname, command = cursor.fetchone()
            cursor.close()
            return {"id": ocid, "rname": rname, "command": command}

        def get_routine_activation_time(self, ratid: int) -> dict:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM routineactivationtime WHERE ratid=?"
            cursor.execute(statement, (ratid,))
            ratid, rname, command = cursor.fetchone()
            cursor.close()
            return {"id": ratid, "rname": rname, "command": command}

        def add_routine(self, routine: dict) -> None:
            days: dict = routine["retakes"]["days"]
            if (
                days["monday"]
                and days["tuesday"]
                and days["wednesday"]
                and days["friday"]
                and days["saturday"]
                and days["sunday"]
            ):
                routine["retakes"]["days"]["daily"] = True
            else:
                routine["retakes"]["days"]["daily"] = False
            cursor: Cursor = self.db.cursor()
            statement: str = """INSERT INTO routine (name, description, daily, monday, tuesday, wednesday, thursday, 
                                friday, saturday, sunday, afteralarm, aftersunrise, aftersunset, aftercall) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """
            values: list = [routine.get("name"), routine.get("description")]
            for key in [
                "daily",
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
            ]:
                values.append(str(int(routine["retakes"]["days"][key] is True)))
            for key in ["after_alarm", "after_sunrise", "after_sunset", "after_call"]:
                values.append(str(int(routine["retakes"]["activation"][key] is True)))
            cursor.execute(statement, tuple(values))

            statement = "SELECT last_insert_rowid()"
            cursor.execute(statement)

            self.__add_commands(routine["actions"]["commands"], routine.get("name"))

            statement = "INSERT INTO routinedates (rname, day, month) VALUES (?, ?, ?)"
            for item in routine["retakes"]["days"]["date_of_day"]:
                cursor.execute(
                    statement, (routine["name"], item.get("day"), item.get("month"))
                )

            statement = "INSERT INTO routineactivationtime (rname, hour, minute) VALUES (?, ?, ?)"
            for item in routine["retakes"]["activation"]["clock_time"]:
                cursor.execute(
                    statement, (routine["name"], item["hour"], item["minute"])
                )

            statement = "INSERT INTO oncommand (rname, command) VALUES(?, ?)"
            for item in routine["on_commands"]:
                cursor.execute(statement, (routine["name"], item))

            cursor.close()
            self.db.commit()

        def add_routine_by_values(
            self,
            name,
            description,
            daily,
            monday,
            tuesday,
            wednesday,
            thursday,
            friday,
            saturday,
            sunday,
            afteralarm,
            aftersunrise,
            aftersunset,
            aftercall,
        ):
            cursor: Cursor = self.db.cursor()
            statement: str = """INSERT INTO routine (name, description, daily, monday, tuesday, wednesday, thursday, 
                                            friday, saturday, sunday, afteralarm, aftersunrise, aftersunset, aftercall) 
                                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """
            cursor.execute(
                statement,
                (
                    name,
                    description,
                    daily,
                    monday,
                    tuesday,
                    wednesday,
                    thursday,
                    friday,
                    saturday,
                    sunday,
                    afteralarm,
                    aftersunrise,
                    aftersunset,
                    aftercall,
                ),
            )
            cursor.close()
            self.db.commit()

        def create_routine_commands(
            self, rname: str, modulename: str, text: list[str]
        ) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = (
                "INSERT INTO routinecommands (rname, modulename) VALUES (?, ?)"
            )
            cursor.execute(statement, (rname, modulename))
            rcid: int = cursor.lastrowid

            if text is not None:
                statement = "INSERT INTO commandtext VALUES (?, ?)"
                cursor.executemany(statement, text)

            cursor.close()
            self.db.commit()
            return rcid

        def create_on_command(self, rname: str, command: str) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = "INSERT INTO oncommand (rname, command) VALUES (?, ?)"
            cursor.execute(statement, (rname, command))
            ocid: int = cursor.lastrowid
            cursor.close()
            self.db.commit()
            return ocid

        def create_routine_dates(self, rname: str, day: int, month: int):
            cursor: Cursor = self.db.cursor()
            statement: str = (
                "INSERT INTO routinedates (rname, day, month) VALUES (?, ?, ?)"
            )
            cursor.execute(statement, (rname, day, month))
            rdid: int = cursor.lastrowid
            cursor.close()
            self.db.commit()
            return rdid

        def create_routine_activation_time(
            self, rname: str, hour: int, minute: int
        ) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = "INSERT INTO routineactivationtime (rname, hour, minute) VALUES (?, ?, ?)"
            cursor.execute(statement, (rname, hour, minute))
            ratid: int = cursor.lastrowid
            cursor.close()
            self.db.commit()
            return ratid

        def update_routine(
            self,
            old_name: str,
            new_routine_dict: dict = None,
            _name: str = None,
            _description: str = None,
            _daily: bool = None,
            _monday: bool = None,
            _tuesday: bool = None,
            _wednesday: bool = None,
            _thursday: bool = None,
            _friday: bool = None,
            _saturday: bool = None,
            _sunday: bool = None,
            _after_alarm: bool = None,
            _after_sunrise: bool = None,
            _after_sunset: bool = None,
            _after_call: bool = None,
            _dates: list = None,
            _clock_time: list = None,
            _commands: list = None,
        ):
            cursor: Cursor = self.db.cursor()

            if new_routine_dict is not None:
                _name = new_routine_dict["name"]
                _description = new_routine_dict["description"]

                _retakes: dict = new_routine_dict["retakes"]["days"]
                _daily = _retakes["daily"]
                _monday = _retakes["monday"]
                _tuesday = _retakes["tuesday"]
                _wednesday = _retakes["wednesday"]
                _thursday = _retakes["thursday"]
                _friday = _retakes["friday"]
                _saturday = _retakes["saturday"]
                _sunday = _retakes["sunday"]

                _activation: dict = new_routine_dict["retakes"]["activation"]
                _after_alarm = _activation["after_alarm"]
                _after_sunrise = _activation["after_sunrise"]
                _after_sunset = _activation["after_sunset"]
                _after_call = _activation["after_call"]

                _dates = _retakes["date_of_day"]
                _clock_time = _activation["clock_time"]
                _commands = new_routine_dict["actions"]["commands"]

            statement: str = "SELECT * FROM routine WHERE name=? LIMIT 1"
            cursor.execute(statement, (old_name,))
            result_set: tuple = cursor.fetchone()
            if cursor.rowcount < 1:
                cursor.close()
                raise NoMatchingEntry(
                    f"No matching routine with the name {old_name} was found in the database."
                )

            (
                name,
                description,
                daily,
                monday,
                tuesday,
                wednesday,
                thursday,
                friday,
                saturday,
                sunday,
                after_alarm,
                after_sunrise,
                after_sunset,
                after_call,
            ) = result_set

            if _name is not None:
                if len(_name) > 50:
                    cursor.close()
                    raise ValueError("Given name is too long!")
                name = _name
                # toDo: update names of other tables

            if _description is not None:
                if len(_description) > 255:
                    cursor.close()
                    raise ValueError("Given text is too long!")
                description = _description
            # maybe (y is True) is y
            if _daily is not None:
                daily = int(_daily is True)
            if _monday is not None:
                monday = int(_monday is True)
            if _tuesday is not None:
                tuesday = int(_tuesday is True)
            if _wednesday is not None:
                wednesday = int(_wednesday is True)
            if _thursday is not None:
                thursday = int(_thursday is True)
            if _friday is not None:
                friday = int(_friday is True)
            if _saturday is not None:
                saturday = int(_saturday is True)
            if _sunday is not None:
                sunday = int(_sunday is True)
            if _after_alarm is not None:
                after_alarm = int(_after_alarm is True)
            if _after_sunrise is not None:
                after_sunrise = int(_after_sunrise is True)
            if _after_sunset is not None:
                after_sunset = int(_after_sunset is True)
            if _after_call is not None:
                after_call = int(_after_call is True)

            statement: str = (
                f"UPDATE routine "
                f"SET name=?, description=?, daily=?, monday=?, tuesday=?, wednesday=?, thursday=?, "
                f"friday=?, saturday=?, sunday=?, afteralarm=?, aftersunrise=?, aftersunset=?, aftercall=? "
                f"WHERE name=?"
            )
            cursor.execute(
                statement,
                (
                    name,
                    description,
                    daily,
                    monday,
                    tuesday,
                    wednesday,
                    thursday,
                    friday,
                    saturday,
                    sunday,
                    after_alarm,
                    after_sunrise,
                    after_sunset,
                    after_call,
                    old_name,
                ),
            )

            if _dates is not None:
                statement: str = "UPDATE routinedates SET day=?, month=? WHERE rdid=?"
                values: list[tuple] = [
                    (item["day"], item["month"], item["id"]) for item in _dates
                ]
                cursor.executemany(statement, values)

            if _clock_time is not None:
                statement: str = (
                    "UPDATE routineactivationtime SET hour=?, minute=? WHERE ratid=?"
                )
                values: list[tuple] = [
                    (item["hour"], item["minute"], item["id"]) for item in _clock_time
                ]
                cursor.executemany(statement, values)

            if _commands is not None:
                statement: str = "UPDATE routinecommands SET modulename=? WHERE rcid=?"
                values: list[tuple] = [
                    (item["module_name"], (item["id"])) for item in _commands
                ]
                cursor.executemany(statement, values)

                statement: str = "UPDATE commandtext SET text=? WHERE rcid=?"
                values: list[tuple] = [(item["text"], item["id"]) for item in _commands]
                cursor.executemany(statement, values)
            cursor.close()
            self.db.commit()

        def update_date_of_day(self, rdid: int, day: int, month: int):
            cursor: Cursor = self.db.cursor()
            statement: str = "UPDATE routinedates SET day=?, month=? WHERE rdid=?"
            cursor.execute(statement, (day, month, rdid))
            cursor.close()
            self.db.commit()

        def update_activation_time(self, ratid: int, hour: int, minute: int):
            cursor: Cursor = self.db.cursor()
            statement: str = (
                "UPDATE routineactivationtime SET hour=?, minute=? WHERE ratid=?"
            )
            cursor.execute(statement, (hour, minute, ratid))
            cursor.close()
            self.db.commit()

        def update_routine_commands(self, rcid: int, modulename: str, text: list[str]):
            cursor: Cursor = self.db.cursor()
            statement: str = "UPDATE routinecommands SET modulename=? WHERE rcid=?"
            cursor.execute(statement, (modulename, rcid))
            cursor.close()
            self.db.commit()

        def update_command_text(self, rcid: int, module_name: str, text: list[str]):
            cursor: Cursor = self.db.cursor()
            statement: str = "DELETE FROM commandtext WHERE rcid=?"
            cursor.execute(statement, (rcid,))
            statement = "INSERT INTO commandtext VALUES (?, ?)"
            values: list[tuple] = [(rcid, item) for item in text]
            cursor.executemany(statement, values)
            cursor.close()
            self.db.commit()

        def update_on_command(self, ocid: int, command: str) -> None:
            cursor: Cursor = self.db.cursor()
            statement: str = "UPDATE FROM oncommand SET command=? WHERE ocid=?"
            cursor.execute(statement, (command, ocid))
            cursor.close()
            self.db.commit()

        def update_on_commands(self, rname: str, commands: list[str]):
            cursor: Cursor = self.db.cursor()
            try:
                statement: str = "DELETE FROM oncommand WHERE rname=?"
                cursor.execute(statement, (rname,))
                statement = "INSERT INTO oncommand (rname, command) VALUES (?, ?)"
                values: list[tuple] = [(rname, item) for item in commands]
                cursor.executemany(statement, values)
            except Exception as e:
                # there could be an SQLException because len(command) has to be < 255
                cursor.close()
                raise e

            cursor.close()
            self.db.commit()

        def update_attribute(self, routine_name: str, values: list[tuple[str, any]]):
            cursor: Cursor = self.db.cursor()

            for item in values:
                attribute, value = item
                # change after_alarm to afteralarm, ...
                attribute.replace("_", "")
                if attribute == "name":
                    self.update_routine(routine_name, _name=value)
                if attribute in [
                    "description",
                    "daily",
                    "monday",
                    "tuesday",
                    "wednesday",
                    "thursday",
                    "friday",
                    "saturday",
                    "sunday",
                    "afteralarm",
                    "aftersunrise",
                    "aftersunset",
                    "aftercall",
                ]:
                    statement: str = "UPDATE routine SET " + "?=?"
                    cursor.execute(statement, (attribute, value))
                elif attribute == "commands":
                    self.update_routine(routine_name, _commands=value)
            cursor.close()
            self.db.commit()

        def delete_routine(self, routine_name: str) -> int:
            cursor: Cursor = self.db.cursor()
            cursor.execute(
                "DELETE FROM routineactivationtime WHERE rname=?", (routine_name,)
            )
            cursor.execute("DELETE FROM routinedates WHERE rname=?", (routine_name,))
            cursor.execute("DELETE FROM commandtext WHERE rname=?", (routine_name,))
            cursor.execute("DELETE FROM routinecommands WHERE rname=?", (routine_name,))
            cursor.execute("DELETE FROM routine WHERE rname=?", (routine_name,))
            counter: int = cursor.rowcount
            cursor.close()
            self.db.commit()
            return counter

        def delete_routine_command(self, rcid: int):
            cursor: Cursor = self.db.cursor()
            statement: str = "DELETE FROM commandtext WHERE rcid=?"
            cursor.execute(statement, (rcid,))
            statement: str = "DELETE FROM routinecommands WHERE rcid=?"
            cursor.execute(statement, (rcid,))
            cursor.close()
            self.db.commit()

        def delete_on_command(self, ocid: int):
            cursor: Cursor = self.db.cursor()
            statement: str = "DELETE FROM oncommand WHERE ocid=?"
            cursor.execute(statement, (ocid,))
            cursor.close()
            self.db.commit()

        def delete_routine_dates(self, rdid: int):
            cursor: Cursor = self.db.cursor()
            statement: str = "DELETE FROM routinedates WHERE rdid=?"
            cursor.execute(statement, (rdid,))
            cursor.close()
            self.db.commit()

        def delete_routine_activation_time(self, ratid: int):
            cursor: Cursor = self.db.cursor()
            statement: str = "DELETE FROM routineactivationtime WHERE ratid=?"
            cursor.execute(statement, (ratid,))
            cursor.close()
            self.db.commit()

        def __add_commands(self, commands: list[dict], name: str):
            cursor: Cursor = self.db.cursor()
            statement: str = (
                "INSERT INTO routinecommands (rname, modulename) VALUES (?, ?)"
            )
            for module in commands:
                cursor.execute(statement, (name, module.get("module_name")))
                cursor.execute("SELECT last_insert_rowid()")
                (module_id,) = cursor.fetchone()

                for text in module.get("text"):
                    cursor.execute(
                        f"INSERT INTO commandtext (cid, text) VALUES (?, ?)",
                        (module_id, text),
                    )
            cursor.close()

        @staticmethod
        def __build_json(
            routine: tuple,
            commands: list[tuple],
            commandtext: list[tuple],
            dates: list[tuple],
            activation: list[tuple],
            on_commands: list[tuple],
        ) -> dict:
            """
            rout: ('Morgenroutine', 'Routine, wenn Sonne Untergeht. Z.B. geht dann das Licht an', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
            command_set: [(1, 'Morgenroutine', 'phillips_hue')],
            text_set: [(1, 'Mach das Bett grün'), (1, 'Mach den Schreibtisch blau')],
            date_set: [(1, 'Morgenroutine', 5, 12)],
            activation_set: [(2, 'Morgenroutine', 10, 30), (1, 'Morgenroutine', 12, 0)],
            on_command_set: []

            """
            if routine == ():
                return {}

            print(routine)
            (
                name,
                description,
                daily,
                monday,
                tuesday,
                wednesday,
                thursday,
                friday,
                saturday,
                sunday,
                afteralarm,
                aftersunrise,
                aftersunset,
                aftercall,
            ) = routine
            result_dict = {
                "name": name,
                "descriptions": description,
                "on_commands": [],
                "retakes": {
                    "days": {
                        "daily": (daily == 1),
                        "monday": (monday == 1),
                        "tuesday": (tuesday == 1),
                        "wednesday": (wednesday == 1),
                        "thursday": (thursday == 1),
                        "friday": (friday == 1),
                        "saturday": (saturday == 1),
                        "sunday": (sunday == 1),
                        "date_of_day": [],
                    },
                    "activation": {
                        "clock_time": [],
                        "after_alarm": (afteralarm == 1),
                        "after_sunrise": (aftersunrise == 1),
                        "after_sunset": (aftersunset == 1),
                        "after_call": (aftercall == 1),
                    },
                },
                "actions": {"commands": []},
            }

            for rdid, rid, day, month in dates:
                result_dict["retakes"]["days"]["date_of_day"].append(
                    {"id": rdid, "day": day, "month": month}
                )

            for ratid, rid, _hour, _min in activation:
                result_dict["retakes"]["activation"]["clock_time"].append(
                    {"id": ratid, "hour": _hour, "min": _min}
                )

            for _id, rid, module_name in commands:
                text_list: list = []

                for cid, text in commandtext:
                    if cid == _id:
                        text_list.append(text)

                result_dict["actions"]["commands"].append(
                    {"id": _id, "module_name": module_name, "text": text_list}
                )

            for (command,) in on_commands:
                result_dict["on_commands"].append(command)

            return result_dict

        def __create_table(self):
            pass

        def __tuple_to_routine(
            self,
            routine: tuple,
        ) -> Routine:
            with self.db.cursor() as cursor:
                (
                    name,
                    description,
                    daily,
                    monday,
                    tuesday,
                    wednesday,
                    thursday,
                    friday,
                    saturday,
                    sunday,
                    after_alarm,
                    after_sunrise,
                    after_sunset,
                    after_call,
                ) = routine

                routine_dates_statement: str = (
                    "SELECT * FROM routinedates WHERE rname=?"
                )
                cursor.execute(routine_dates_statement, (name,))

                routine_dates: list[SpecificDate] = [
                    SpecificDate(sid, day, month)
                    for sid, _, day, month in cursor.fetchall()
                ]

                on_command_statement: str = "SELECT * FROM oncommand WHERE rname=?"
                cursor.execute(on_command_statement, (name,))

                on_commands: list[str] = [command for command, in cursor.fetchall()]

                routine_days: RoutineDays = RoutineDays(
                    monday,
                    tuesday,
                    wednesday,
                    thursday,
                    friday,
                    saturday,
                    sunday,
                    routine_dates,
                )

                routine_activation_times_statement: str = (
                    "SELECT * FROM routineactivationtime WHERE rname=?"
                )
                cursor.execute(routine_activation_times_statement, (name,))

                clock_times: list[RoutineClockTime] = [
                    RoutineClockTime(rctid, time(hour, minute))
                    for rctid, _, hour, minute in cursor.fetchall()
                ]

                routine_times: RoutineTimes = RoutineTimes(
                    clock_times, after_alarm, after_sunrise, after_sunset, after_call
                )

                retakes: RoutineRetakes = RoutineRetakes(routine_days, routine_times)

                actions: list[RoutineCommand] = self.__get_routine_commands(name)

                return Routine(name, description, on_commands, retakes, actions)

        def __get_routine_commands(self, routine_name: str) -> list[RoutineCommand]:
            with self.db.cursor() as cursor:
                statement: str = "SELECT * FROM routinecommands WHERE rname=?"
                cursor.execute(statement, (routine_name,))
                return [
                    RoutineCommand(rcid, module_name, self.__get_texts_of_command(rcid))
                    for rcid, _, module_name in cursor.fetchall()
                ]

        def __get_texts_of_command(self, routine_id: int) -> list[str]:
            with self.db.cursor() as cursor:
                statement: str = "SELECT * FROM commandtext WHERE cid=?"
                cursor.execute(statement, (routine_id,))
                return [text for _, text in cursor.fetchall()]

    class _QuizInterface:
        def __init__(self, db: Connection) -> None:
            self.db: Connection = db
            logging.info("[INFO] QuizInterface initialized.")

        def add_question(
            self, theme: str, question: str, audio: str | io.BytesIO, answer: str
        ):
            pass

        def load_stack(self, theme: str):
            pass

        def update_stack(self, theme: str):
            pass

        def __create_table(self):
            pass

    class _MessangerInterface:
        def __init__(self) -> None:
            pass

        def add_rejected_message(self, msg):
            if msg["content_type"] == "text":
                pass

    class _BirthdayInterface:
        def __init__(self, db: Connection) -> None:
            self.db: Connection = db

        def add_birthday(
            self, first_name: str, last_name: str, day: int, month: int, year: int
        ) -> None:
            cursor: Cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO birthdays VALUES (?, ?, ?, ?, ?)",
                (first_name, last_name, day, month, year),
            )
            cursor.close()
            self.db.commit()

        def get_birthday(self, first_name: str, last_name: str) -> dict:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM birthdays WHERE firstname=? AND lastname=?"
            cursor.execute(statement, (first_name, last_name))
            result_set: tuple = cursor.fetchone()
            cursor.close()
            return self.__build_json(result_set)

        def get_all_birthdays(self) -> list[dict]:
            cursor: Cursor = self.db.cursor()
            result_list: list[dict] = []

            cursor.execute(f"SELECT * FROM birthdays")
            result_set: list[tuple] = cursor.fetchall()
            cursor.close()
            for item in result_set:
                result_list.append(self.__build_json(item))

            return result_list

        def update_birthday(
            self,
            _old_first_name: str,
            _old_last_name: str,
            _new_first_name: str = None,
            _new_last_name: str = None,
            _day: int = None,
            _month: int = None,
            _year: int = None,
        ) -> None:

            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM birthdays WHERE firstname=? AND lastname=?"
            cursor.execute(statement, (_old_first_name, _old_last_name))
            first_name, last_name, day, month, year = cursor.fetchone()

            if _new_first_name is not None:
                first_name = _new_first_name
            if _new_last_name is not None:
                last_name = _new_last_name
            if _day is not None:
                day = day
            if _month is not None:
                month = _month
            if _year is not None:
                year = _year

            statement: str = """UPDATE birthdays 
                                SET firstname=?, lastname=?, day=?, month=?, year=? 
                                WHERE firstname=? 
                                AND lastname=?"""
            cursor.execute(
                statement,
                (
                    first_name,
                    last_name,
                    day,
                    month,
                    year,
                    _old_first_name,
                    _old_last_name,
                ),
            )
            cursor.close()
            self.db.commit()

        def delete_birthday(self, first_name: str, last_name: str) -> None:
            cursor: Cursor = self.db.cursor()
            cursor.execute(
                "DELETE FROM birthdays WHERE firstname=? AND lastname=?",
                (first_name, last_name),
            )
            cursor.close()
            self.db.commit()

        @staticmethod
        def __build_json(result_set: tuple) -> dict:
            return {
                "first_name": result_set[0],
                "last_name": result_set[1],
                "day": result_set[2],
                "month": result_set[3],
                "year": result_set[4],
            }

    """def __execute(self, command: str, values: tuple = ()) -> list | int:
        # cursor: Cursor = self.db.cursor()
        cursor: Cursor = self.db.cursor()
        try:
            result_set: list = cursor.execute(command, values).fetchall()
            if 'insert into' in command.lower():
                return cursor.lastrowid
            elif 'delete' in command.lower():
                return cursor.rowcount
            return result_set
        except Exception as e:
            self.error_counter += 1
            logging.warning(f"[ERROR] Could not execute SQL command: {command}:\n {e}")
            self.db.rollback()
            raise SQLException(f"Couldn't execute SQL Statement: {command} with Values {str(values)}\n{e}")
        finally:
            cursor.close()"""


if __name__ == "__main__":
    db = DataBase()
    print(db.routine_interface.get_routines())
    db.routine_interface.add_routine(
        {
            "name": "Morgenroutine",
            "descriptions": "Routine, wenn Sonne Untergeht. Z.B. geht dann das Licht an",
            "on_commands": [],
            "retakes": {
                "days": {
                    "daily": True,
                    "monday": False,
                    "tuesday": False,
                    "wednesday": False,
                    "thursday": False,
                    "friday": False,
                    "saturday": False,
                    "sunday": False,
                    "date_of_day": [{"id": 1, "day": 5, "month": 12}],
                },
                "activation": {
                    "clock_time": [
                        {"id": 2, "hour": 10, "minute": 30},
                        {"id": 1, "hour": 12, "minute": 0},
                    ],
                    "after_alarm": False,
                    "after_sunrise": False,
                    "after_sunset": True,
                    "after_call": False,
                },
            },
            "actions": {
                "commands": [
                    {
                        "id": 1,
                        "module_name": "phillips_hue",
                        "text": [
                            "Mach das Bett gr\u00fcn",
                            "Mach den Schreibtisch blau",
                        ],
                    }
                ]
            },
        }
    )
    # print(db.alarm_interface.get_alarms())
