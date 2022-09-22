from __future__ import annotations  # compatibility for < 3.10

import base64
import io
import os
import sqlite3
from datetime import datetime, time
from sqlite3 import Connection, Cursor
from typing import TYPE_CHECKING

import pathlib
from src.exceptions.critical_exception import UnsolvableException
from src.exceptions.sql_exception import *

if TYPE_CHECKING:
    from src.models.shopping_list import ShoppingListItem
    from src.models.timer import Timer
    from src.models.user import User

    from src.models.alarm import Alarm, AlarmRepeating
    from src.models.audio.audio_file import AudioFile
    from src.models.birthday import Birthday
    from src.models.reminder import Reminder
    from src.models.routine import (
        Routine,
        SpecificDate,
        RoutineDays,
        RoutineCommand,
        RoutineRetakes,
        RoutineTime,
        RoutineClockTime,
        CallingCommand,
    )


# toDo: __tuple_to raise value error when nothing fount (type-error)
# toDo: bugfix in returning boolean values of db


class DataBase:
    def __init__(self) -> None:
        log.basicConfig(level=log.DEBUG)
        log.action("Initialize DataBase...\n")

        path = "C:\\Users\\Jakob\\PycharmProjects\\Jarvis\\speechassistant\\src\\database\\db.sqlite"

        self.db: Connection = sqlite3.connect(
            path,
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

        log.info("DataBase successfully initialized.")

    def close(self):
        self.db.close()
        DataBase.__instance = None
        log.info("DataBase closed!")

    def create_tables(self) -> None:
        # toDo: CONSTRAINTS

        # CHECK (mycolumn IN (0, 1)) -> BOOL

        log.action("Create tables...")
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
            "time TIME, "
            "text VARCHAR(255), "
            "active INTEGER, "
            "initiated INTEGER, "
            "last_executed DATE, "
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
            "time DATE,"
            "text VARCHAR(255),"
            "uid INTEGER,"
            "FOREIGN KEY(uid) REFERENCES user(uid))"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS routine ("
            "name VARCHAR(50) PRIMARY KEY, "
            "description VARCHAR(255), "
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
            "time TIME, "
            "FOREIGN KEY(rname) REFERENCES routine(rname), "
            "UNIQUE (rname, time))"
        )

        self.__create_table(
            "CREATE TABLE IF NOT EXISTS routinedates ("
            "rdid INTEGER PRIMARY KEY, "
            "rname VARCHAR(50), "
            "date DATE, "
            "UNIQUE (rname, date), "
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
            "date DATE, "
            "PRIMARY KEY(firstname, lastname), "
            "UNIQUE (firstname, lastname))"
        )

        # #self.db.commit()

        if self.error_counter == 0:
            log.info("Tables successfully created!")
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
            log.info(f"Successfully created table {command.split(' ')[5]}!")
        except Exception as e:
            self.error_counter += 1
            log.fatal(
                f"Couldn't create table {command.split(' ')[5]}:\n {e}"
            )
        cursor.close()
        self.db.commit()

    def __remove_tables(self):
        pass

    def stop(self):
        log.action("Stopping database...")
        self.db.commit()
        self.db.close()

    class _UserInterface:
        def __init__(self, _db: Connection) -> None:
            self.db: Connection = _db
            log.info("UserInterface initialized.")

        def get_user_by_id(self, user_id: int) -> User:
            cursor: Cursor = self.db.cursor()
            statement: str = f"SELECT * from user WHERE uid=? LIMIT 1"
            cursor.execute(statement, (user_id,))

            user: User = self.__tuple_to_user(cursor.fetchone())
            cursor.close()
            return user

        def get_user_by_messenger_id(self, messenger_id: int) -> User:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM user WHERE mid=? LIMIT 1"
            cursor.execute(statement, (messenger_id,))
            user: User = self.__tuple_to_user(cursor.fetchone())
            cursor.close()
            return user

        def get_user_by_alias(self, alias: str) -> User:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM user WHERE alias=? LIMIT 1"
            cursor.execute(statement, (alias,))
            user: User = self.__tuple_to_user(cursor.fetchone())
            cursor.close()
            return user

        def get_user_by_first_and_last_name(
                self, first_name: str, last_name: str
        ) -> User:
            cursor: Cursor = self.db.cursor()
            statement: str = (
                "SELECT * FROM user WHERE firstname=? AND lastname=? LIMIT 1"
            )
            cursor.execute(statement, (first_name, last_name))
            user: User = self.__tuple_to_user(cursor.fetchone())
            cursor.close()
            return user

        def get_users(self) -> list[User]:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * from user"
            cursor.execute(statement)
            result_set: list = cursor.fetchall()

            user_list: list[User] = [self.__tuple_to_user(item) for item in result_set]

            for user in user_list:
                notification_statement: str = (
                    f"SELECT text FROM notification WHERE uid=?"
                )
                cursor.execute(notification_statement, (user.uid,))
                user.waiting_notifications = [x[0] for x in cursor.fetchall()]
            cursor.close()
            return user_list

        def add_user(self, user: User) -> User:
            cursor: Cursor = self.db.cursor()
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
            cursor.close()
            return user

        def add_user_notification_by_user_id(
                self, user_id: int, notification: str
        ) -> None:
            cursor: Cursor = self.db.cursor()
            statement: str = f"INSERT INTO notification (uid, text) VALUES (?, ?)"
            cursor.execute(statement, (user_id, notification))
            cursor.close()

        def add_use_notification_by_user_alias(
                self, user_alias: str, notification: str
        ) -> None:
            user_id: int = self.__get_user_id_by_alias(user_alias)
            self.add_user_notification_by_user_id(user_id, notification)

        def update_user(self, user: User) -> User:
            cursor: Cursor = self.db.cursor()
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
            cursor.close()
            return user

        def delete_user_notification_by_id(self, user: int, text: str) -> None:
            cursor: Cursor = self.db.cursor()
            statement: str = "DELETE FROM notification WHERE uid=? AND text=?"
            cursor.execute(statement, (user, text))
            cursor.close()

        def delete_user_notification_by_alias(self, alias: str, text: str) -> None:
            user_id: int = self.__get_user_id_by_alias(alias)
            self.delete_user_notification_by_id(user_id, text)

        def delete_user_by_id(self, user_id: int) -> None:
            cursor: Cursor = self.db.cursor()
            statement: str = "DELETE FROM user WHERE uid=?"
            cursor.execute(statement, (user_id,))
            cursor.close()

        def delete_user_by_alias(self, alias: str) -> None:
            user_id: int = self.__get_user_id_by_alias(alias)
            self.delete_user_by_id(user_id)

        @staticmethod
        def __birthday_to_string(birthday: datetime) -> str:
            return birthday.isoformat()

        def __get_user_id_by_alias(self, alias: str) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT uid FROM user WHERE alias=? LIMIT 1"
            cursor.execute(statement, (alias,))
            uid: int = cursor.fetchone()
            cursor.close()
            if uid:
                return uid
            else:
                raise UserNotFountException()

        def __get_user_id_by_first_and_last_name(
                self, first_name: str, last_name: str
        ) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = (
                "SELECT uid FROM user WHERE firstname=? AND lastname=? LIMIT 1"
            )
            cursor.execute(statement, (first_name, last_name))
            uid: int = cursor.fetchone()
            cursor.close()
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
            log.info("AlarmInterface initialized.")

        def get_alarm_by_id(self, aid: int) -> Alarm:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM alarm as a JOIN alarmrepeat as ar ON a.aid=ar.aid WHERE a.aid=? LIMIT 1"
            cursor.execute(statement, (aid,))
            alarm: Alarm = self.__tuple_to_alarm(cursor.fetchone())
            cursor.close()
            return alarm

        def get_active_and_init_alarms(self) -> tuple[list[Alarm], list[Alarm]]:
            now: datetime = datetime.now()
            weekday: str = self.skills.statics.numb_to_day[str(now.weekday())]
            now_seconds = now.hour * 3600 + now.minute * 60 + now.second
            active_alarms = self.get_active_and_passed_alarms(now, weekday)
            init_alarms = self.get_initiated_alarms(now_seconds, weekday)

            return active_alarms, init_alarms

        def get_active_and_passed_alarms(self, now, weekday) -> list[Alarm]:
            cursor: Cursor = self.db.cursor()
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
            cursor.close()
            return active_alarms

        def get_initiated_alarms(self, now_seconds, weekday) -> list[Alarm]:
            cursor: Cursor = self.db.cursor()
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
            cursor.close()
            return init_alarms

        def get_all_alarms(self) -> list[Alarm]:
            cursor: Cursor = self.db.cursor()
            statement: str = (
                "SELECT * FROM alarm as a JOIN alarmrepeat as ar ON a.aid = ar.aid"
            )
            cursor.execute(statement)
            alarms: list[Alarm] = [
                self.__tuple_to_alarm(alarm) for alarm in cursor.fetchall()
            ]
            cursor.close()
            return alarms

        def get_alarms_unfiltered(self, active: bool) -> list[Alarm]:
            cursor: Cursor = self.db.cursor()
            statement: str = (
                "SELECT * FROM alarm as a JOIN alarmrepeat as ar ON a.aid=ar.aid"
            )
            if active:
                statement = f"{statement} WHERE a.active=True"
            cursor.execute(statement)
            alarms: list[Alarm] = [
                self.__tuple_to_alarm(alarm) for alarm in cursor.fetchall()
            ]
            cursor.close()
            return alarms

        def add_alarm(self, alarm: Alarm) -> Alarm:
            alarm_id = self.__add_alarm_into_db(
                alarm.active,
                alarm.alarm_time,
                alarm.song_name,
                alarm.text,
                alarm.user_id,
            )
            self.__add_alarm_repeating_into_db(alarm_id, alarm.repeating)
            alarm.alarm_id = alarm_id
            return alarm

        def __add_alarm_repeating_into_db(
                self, alarm_id: int, repeating: AlarmRepeating
        ) -> None:
            cursor: Cursor = self.db.cursor()
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
            cursor.close()

        def __add_alarm_into_db(
                self, active: bool, alarm_time: time, song: str, text: str, user_id: int
        ) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = """INSERT INTO alarm (sname, uid, time, text, active, 
                                initiated, last_executed) 
                                VALUES (?, ?, ?, ?, ?, ?, "")"""
            cursor.execute(
                statement,
                (song, user_id, alarm_time.isoformat(), active, text, int(active)),
            )
            alarm_id: int = cursor.lastrowid
            cursor.close()
            return alarm_id

        def delete_alarm(self, aid: int) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = "DELETE FROM alarm WHERE aid=?"
            cursor.execute(statement, (aid,))
            anz_removed_alarm: int = cursor.rowcount
            statement = "DELETE FROM alarmrepeat WHERE aid=?"
            cursor.execute(statement, (aid,))
            anz_removed_repeat: int = cursor.rowcount

            if anz_removed_alarm != anz_removed_repeat:
                self.db.rollback()
                raise UnsolvableException("Removed more alarm repeating´s than alarms!")
            cursor.close()
            return anz_removed_alarm

        def update_alarm(self, alarm: Alarm):
            cursor: Cursor = self.db.cursor()
            statement: str = (
                f"UPDATE alarm SET sname=?, uid=?, time=?, text=?, active=?, "
                f"initiated=?, last_executed=? WHERE aid=?"
            )
            cursor.execute(
                statement,
                (
                    alarm.song_name,
                    alarm.user_id,
                    alarm.alarm_time.isoformat(),
                    alarm.text,
                    alarm.active,
                    alarm.initiated,
                    alarm.last_executed,
                    alarm.alarm_id,
                ),
            )
            alarm_repeat: AlarmRepeating = alarm.repeating
            statement: str = (
                f"UPDATE alarmrepeat "
                f"SET monday=?, tuesday=?, wednesday=?, thursday=?, friday=?, saturday=?, sunday=?, regular=? "
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
                    alarm.alarm_id,
                ),
            )
            cursor.close()
            return alarm

        @staticmethod
        def __tuple_to_alarm(alarm: tuple) -> Alarm:
            from src.models.alarm import Alarm, AlarmRepeating

            if not alarm:
                raise NoMatchingEntry()
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
                monday=(monday == 1),
                tuesday=(tuesday == 1),
                wednesday=(wednesday == 1),
                thursday=(thursday == 1),
                friday=(friday == 1),
                saturday=(saturday == 1),
                sunday=(sunday == 1),
                regular=(regular == 1),
            )
            return Alarm(
                alarm_id=alarm_id,
                repeating=repeating,
                song_name=song_name,
                alarm_time=time.fromisoformat(alarm_time),
                text=text,
                active=(active == 1),
                initiated=(initiated == 1),
                last_executed=datetime.fromisoformat(last_executed)
                if last_executed
                else None,
                user_id=user_id,
            )

        def __create_table(self):
            pass

    class _AudioInterface:
        def __init__(self, _db: Connection) -> None:
            self.db: Connection = _db
            self.audio_path: str = "C:\\Users\\Jakob\\PycharmProjects\\Jarvis"
            log.info("AudioInterface initialized.")

        def add_audio(self, name: str, audio_file: io.BytesIO = None) -> str:
            cursor: Cursor = self.db.cursor()
            statement: str = "INSERT INTO audio (name, path) VALUES (?, ?)"
            encoded_data = base64.b64decode(audio_file.read())
            cursor.execute(statement, (name, encoded_data))
            cursor.close()
            return name

        def update_audio_file(self, old_name: str, audio_file: AudioFile) -> None:
            cursor: Cursor = self.db.cursor()
            statement: str = "UPDATE audio SET name=?, data=? WHERE name=?"
            cursor.execute(statement, (audio_file.name, audio_file.data, old_name))
            cursor.close()

        def get_audio_file_by_name(self, audio_name: str) -> AudioFile:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM audio WHERE name=?"
            cursor.execute(statement, (audio_name,))
            audio_file: AudioFile = self.__tuple_to_audio_file(cursor.fetchone())
            cursor.close()
            return audio_file

        def get_all_audio_files(self) -> list[AudioFile]:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM audio"
            cursor.execute(statement)
            audio_files: list[AudioFile] = [
                self.__tuple_to_audio_file(result) for result in cursor.fetchall()
            ]
            cursor.close()
            return audio_files

        def get_file_names(self) -> list[str]:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT name FROM audio"
            cursor.execute(statement)
            result_set: list[tuple] = cursor.fetchall()
            cursor.close()
            # return only filenames
            return [x[0] for x in result_set]

        def delete_audio(self, audio_name: str) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT path FROM audio WHERE name=?"
            cursor.execute(statement, (audio_name,))
            statement = "DELETE FROM audio WHERE name=?"
            cursor.execute(statement, (audio_name,))
            counter: int = cursor.rowcount
            cursor.close()
            return counter

        @staticmethod
        def __tuple_to_audio_file(result_set: tuple) -> AudioFile:
            name, data = result_set
            return AudioFile(name, data)

    class _TimerInterface:
        def __init__(self, _db: Connection, user_interface) -> None:
            self.db: Connection = _db
            self.user_interface = user_interface
            log.info("TimerInterface initialized.")

        def get_all_timer(self) -> list[Timer]:
            cursor: Cursor = self.db.cursor()
            statement: str = f"SELECT * FROM timer"
            cursor.execute(statement)
            result_set: list = cursor.fetchall()
            cursor.close()
            return [self.__tuple_to_timer(timer) for timer in result_set]

        def get_timer_of_user_by_user_id(self, user: int) -> list[Timer]:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM timer WHERE uid=?"
            cursor.execute(statement, (user,))
            timer: list[Timer] = [
                self.__tuple_to_timer(alarm) for alarm in cursor.fetchall()
            ]
            cursor.close()
            return timer

        def get_timer_of_user_by_user_alias(self, user_alias: str) -> list[Timer]:
            user_id: int = self.user_interface.__get_user_id(user_alias)
            return self.get_timer_of_user_by_user_id(user_id)

        def get_timer_by_id(self, timer_id: int) -> Timer:
            cursor: Cursor = self.db.cursor()
            statement: str = f"SELECT * FROM timer WHERE id=? LIMIT 1"
            cursor.execute(statement, (timer_id,))
            timer: Timer = self.__tuple_to_timer(cursor.fetchone())
            cursor.close()
            return timer

        def add_timer(self, timer: Timer) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = (
                f"INSERT INTO timer (duration, time, text, uid) " f"VALUES(?, ?, ?, ?)"
            )
            cursor.execute(
                statement,
                (timer.duration, timer.start_time, timer.text, timer.user.uid),
            )
            result_set: int = cursor.rowcount
            statement = "SELECT id FROM timer LIMIT 1"
            cursor.execute(statement)
            # id from inserted timer - id from the first timer in the current database +1
            position: int = result_set - cursor.rowcount + 1
            cursor.close()
            return position

        def update_timer(self, timer: Timer) -> Timer:
            cursor: Cursor = self.db.cursor()
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
            cursor.close()
            return timer

        def delete_timer(self, timer_id: int) -> None:
            cursor: Cursor = self.db.cursor()
            statement: str = "DELETE FROM timer WHERE id=?"
            cursor.execute(statement, (timer_id,))
            cursor.close()

        def delete_passed_timer(self) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = "DELETE FROM timer WHERE time < ?"
            now: datetime = datetime.now()
            cursor.execute(
                statement, time(now.hour, now.minute, now.second).isoformat()
            )
            counter: int = cursor.rowcount
            cursor.close()
            return counter

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
            log.info("ReminderInterface initialized.")

        def get_passed_reminder(self) -> list[Reminder]:
            cursor: Cursor = self.db.cursor()
            now: datetime = datetime.now()
            date_string: str = now.strftime("%Y.%d.%m:%H:%M:%S")
            statement: str = (
                "SELECT * FROM reminder as r JOIN user as u ON r.id = u.id WHERE time<?"
            )
            cursor.execute(statement, (date_string,))
            reminder: list[Reminder] = [
                self.__tuple_to_reminder(r) for r in cursor.fetchall()
            ]
            cursor.close()
            return reminder

        def get_all_reminder(self) -> list[Reminder]:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM reminder"
            cursor.execute(statement)
            reminder: list[Reminder] = [
                self.__tuple_to_reminder(r) for r in cursor.fetchall()
            ]
            cursor.close()
            return reminder

        def get_reminder_by_id(self, reminder_id: int) -> Reminder:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM reminder WHERE id=?"
            cursor.execute(statement, (reminder_id,))
            reminder: Reminder = self.__tuple_to_reminder(cursor.fetchone())
            cursor.close()
            return reminder

        def add_reminder(self, reminder: Reminder) -> Reminder:
            cursor: Cursor = self.db.cursor()
            statement: str = f"INSERT INTO reminder (time, text, uid) VALUES (?, ?, ?)"
            cursor.execute(statement, (reminder.time, reminder.text, reminder.user_id))
            rid: int = cursor.lastrowid
            cursor.close()
            reminder.reminder_id = rid
            return reminder

        def delete_reminder_by_id(self, _id: int) -> int:
            statement: str = "DELETE FROM reminder WHERE id=?"
            return self.__delete_reminder_by_statement(statement, (_id,))

        def delete_reminder_by_time(self, _time: str) -> int:
            statement: str = "DELTE FROM reminder WHERE time=?"
            return self.__delete_reminder_by_statement(statement, (_time,))

        def __delete_reminder_by_statement(self, statement: str, values: tuple) -> int:
            cursor: Cursor = self.db.cursor()
            cursor.execute(statement, values)
            counter: int = cursor.rowcount
            cursor.close()
            return counter

        @staticmethod
        def __tuple_to_reminder(result_set: tuple) -> Reminder:
            if not result_set:
                raise NoMatchingEntry()
            (reminder_id, reminder_time, text, user_id) = result_set
            return Reminder(
                time=reminder_time, text=text, user_id=user_id, reminder_id=reminder_id
            )

        def __create_table(self):
            pass

    class _ShoppingListInterface:
        def __init__(self, _db: Connection) -> None:
            self.db: Connection = _db
            log.info("ShoppingListInterface initialized.")

        def get_list(self) -> list[ShoppingListItem]:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM shoppinglist"
            cursor.execute(statement)
            item_list: list[ShoppingListItem] = self.__tuple_to_shopping_list(
                cursor.fetchall()
            )
            cursor.close()
            return item_list

        def get_item(self, name: str) -> ShoppingListItem:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM shoppinglist WHERE name=?"
            cursor.execute(statement, (name,))
            shopping_item: ShoppingListItem = self.__tuple_to_shopping_list_item(
                cursor.fetchone()
            )
            cursor.close()
            return shopping_item

        def add_item(self, item: ShoppingListItem) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = (
                f"INSERT INTO shoppinglist (name, measure, quantity) VALUES (?, ?, ?)"
            )
            cursor.execute(statement, (item.name, item.measure, item.quantity))
            self.db.commit()
            item_id: int = cursor.lastrowid
            cursor.close()
            return item_id

        def update_item(self, item: ShoppingListItem) -> ShoppingListItem:
            cursor: Cursor = self.db.cursor()
            statement: str = """UPDATE shoppinglist 
                                SET name=?, measure=?, quantity=?  
                                WHERE name=?"""
            cursor.execute(statement, (item.name, item.measure, item.quantity))
            cursor.close()
            return item

        def remove_item_by_id(self, item_id: int) -> None:
            statement: str = "DELETE FROM shoppinglist WHERE id=?"
            self.__remove_item_by_statement(statement, (item_id,))

        def remove_item_by_name(self, name: str) -> None:
            statement: str = "DELETE FROM shoppinglist WHERE name=?"
            self.__remove_item_by_statement(statement, (name,))

        def __remove_item_by_statement(self, statement: str, values: tuple) -> None:
            cursor: Cursor = self.db.cursor()
            cursor.execute(statement, values)
            cursor.close()

        def clear_list(self) -> None:
            cursor: Cursor = self.db.cursor()
            statement: str = "DELETE FROM shoppinglist"
            cursor.execute(statement)
            cursor.close()

        def is_item_in_list(self, name: str) -> bool:
            cursor: Cursor = self.db.cursor()
            statement: str = f"SELECT 1 FROM shoppinglist WHERE name=? LIMIT 1"
            cursor.execute(statement, (name,))
            anz_items = cursor.rowcount
            cursor.close()
            return anz_items > 0

        def __create_table(self):
            pass

        def __tuple_to_shopping_list(
                self, result_set: list[tuple]
        ) -> list[ShoppingListItem]:
            return [self.__tuple_to_shopping_list_item(item) for item in result_set]

        @staticmethod
        def __tuple_to_shopping_list_item(item: tuple) -> ShoppingListItem:
            name, measure, quantity = item
            return ShoppingListItem(
                id=None, name=name, measure=measure, quantity=quantity
            )

    class _RoutineInterface:
        def __init__(self, _db: Connection) -> None:
            self.db: Connection = _db
            log.info("RoutineInterface initialized.")

        def get_routine(self, name: str) -> Routine:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM routine WHERE name=? LIMIT 1"
            cursor.execute(statement, (name,))
            found_routine: Routine = self.__tuple_to_routine(cursor.fetchone())
            cursor.close()
            return found_routine

        def get_routines(
                self, on_command: str = None, on_time: time = None
        ) -> list[Routine]:
            cursor: Cursor = self.db.cursor()
            if on_command:
                statement: str = """SELECT * FROM routine 
                                JOIN oncommand ON routine.name=oncommand.rname 
                                WHERE instr(?, oncommand.command) > 0"""
                cursor.execute(statement, (on_command,))
            elif on_time:
                # toDo
                statement: str = """SELECT * FROM routine"""
                cursor.execute(statement)
            else:
                statement: str = "SELECT * FROM routine"
                cursor.execute(statement)

            routines: list[tuple] = cursor.fetchall()
            return [self.__tuple_to_routine(r) for r in routines]

        def add_routine(self, new_routine: Routine) -> Routine:
            (
                name,
                description,
                calling_commands,
                retakes,
                actions,
            ) = new_routine.as_tuple()

            (
                monday,
                tuesday,
                wednesday,
                thursday,
                friday,
                saturday,
                sunday,
                specific_dates,
            ) = retakes.days.as_tuple()

            (
                times,
                after_alarm,
                after_sunrise,
                after_sunset,
                after_call,
            ) = retakes.times.as_tuple()
            cursor: Cursor = self.db.cursor()
            statement: str = (
                "INSERT INTO routine VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            )
            cursor.execute(
                statement,
                (
                    name,
                    description,
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
                ),
            )
            cursor.close()
            self.add_calling_commands(name, new_routine.calling_commands)
            new_routine.actions = self.add_actions(name, new_routine.actions)
            new_routine.retakes.times.clock_times = self.add_clock_times(
                name, new_routine.retakes.times.clock_times
            )
            new_routine.retakes.days.specific_dates = self.add_specific_dates(
                name, new_routine.retakes.days.specific_dates
            )

            return new_routine

        def add_calling_commands(
                self, routine_name: str, calling_commands: list[CallingCommand]
        ) -> list[CallingCommand]:
            for index, command in enumerate(calling_commands):
                calling_commands[index] = self.add_calling_command(
                    routine_name, command
                )
            return calling_commands

        def add_calling_command(
                self, routine_name: str, calling_command: CallingCommand
        ) -> CallingCommand:
            statement: str = "INSERT INTO oncommand (rname, command) VALUES (?, ?)"
            cursor: Cursor = self.db.cursor()
            cursor.execute(statement, (routine_name, calling_command.command))
            calling_command.ocid = cursor.lastrowid
            cursor.close()
            return calling_command

        def add_actions(
                self, routine_name: str, actions: list[RoutineCommand]
        ) -> list[RoutineCommand]:
            cursor: Cursor = self.db.cursor()
            command_statement: str = (
                "INSERT INTO routinecommands (rname, modulename) VALUES (?, ?)"
            )
            text_statement: str = "INSERT INTO commandtext VALUES (?, ?)"
            for index, action in enumerate(actions):
                cursor.execute(command_statement, (routine_name, action.module_name))
                command_id: int = cursor.lastrowid
                actions[index].cid = command_id
                for text in action.with_text:
                    cursor.execute(text_statement, (command_id, text))
            cursor.close()
            return actions

        def add_times(
                self, routine_name: str, clock_times: list[RoutineClockTime]
        ) -> None:
            pass

        def add_clock_times(
                self, routine_name: str, clock_times: list[RoutineClockTime]
        ) -> list[RoutineClockTime]:
            for index, clock_time in enumerate(clock_times):
                clock_times[index] = self.add_clock_time(routine_name, clock_time)
            return clock_times

        def add_clock_time(
                self, routine_name: str, clock_time: RoutineClockTime
        ) -> RoutineClockTime:
            statement: str = (
                "INSERT INTO routineactivationtime (rname, time) VALUES (?, ?)"
            )
            cursor: Cursor = self.db.cursor()
            cursor.execute(statement, (routine_name, clock_time.clock_time.isoformat()))
            clock_time.ratid = cursor.lastrowid
            cursor.close()
            return clock_time

        def add_specific_dates(
                self, routine_name: str, dates: list[SpecificDate]
        ) -> list[SpecificDate]:
            for index, date in dates:
                dates[index] = self.add_specific_date(routine_name, date)
            return dates

        def add_specific_date(
                self, routine_name: str, specific_date: SpecificDate
        ) -> SpecificDate:
            statement: str = "INSERT INTO routinedates (rname, time) VALUES (?, ?)"
            cursor: Cursor = self.db.cursor()
            cursor.executemany(statement, (routine_name, specific_date.date))
            specific_date.sid = cursor.lastrowid
            cursor.close()
            return specific_date

        def add_time(self, routine_name: str, clock_time: RoutineClockTime) -> None:
            pass

        def rename_routine(self, old_name: str, new_name: str) -> None:
            statement: str = f"UPDATE routine SET name=? WHERE name=?"
            cursor: Cursor = self.db.cursor()
            cursor.execute(statement, (new_name, old_name))
            cursor.close()

        def update_routine(self, old_name: str, updated_routine: Routine) -> Routine:
            statement: str = f"UPDATE routine SET name=?, description=? WHERE name=?"
            (
                name,
                description,
                calling_commands,
                retakes,
                actions,
            ) = updated_routine.as_tuple()
            cursor: Cursor = self.db.cursor()
            cursor.execute(statement, (name, description, old_name))
            cursor.close()
            updated_routine.calling_commands = self.update_calling_commands(
                updated_routine.calling_commands
            )
            self.update_retakes(updated_routine.name, updated_routine.retakes)
            self.update_actions(updated_routine.actions)
            return updated_routine

        def update_calling_commands(
                self, calling_commands: list[CallingCommand]
        ) -> list[CallingCommand]:
            for index, command in enumerate(calling_commands):
                calling_commands[index] = self.update_calling_command(command)
            return calling_commands

        def update_calling_command(
                self, calling_command: CallingCommand
        ) -> CallingCommand:
            ocid, routine_name, command = calling_command
            cursor: Cursor = self.db.cursor()
            if ocid:
                update_statement: str = (
                    "UPDATE oncommand SET rname=?, command=? WHERE ocid=?"
                )
                cursor.execute(update_statement, (routine_name, command, ocid))
            else:
                create_statement = (
                    "INSERT INTO oncommand (rname, command) VALUES (?, ?)"
                )
                cursor.execute(create_statement, (routine_name, command))
                calling_command.ocid = cursor.lastrowid
            cursor.close()
            return calling_command

        def update_actions(self, actions: list[RoutineCommand]) -> None:
            for command in actions:
                self.update_action_texts(command)

        def update_action_texts(self, routine_command: RoutineCommand) -> None:
            del_statement: str = "DELETE FROM commandtext WHERE cid=?"
            create_statement = "INSERT INTO commandtext VALUES (?, ?)"

            cursor: Cursor = self.db.cursor()
            cursor.execute(del_statement, (routine_command.cid,))
            cursor.executemany(
                create_statement,
                [
                    (routine_command.module_name, text)
                    for text in routine_command.with_text
                ],
            )
            cursor.close()

        def update_retakes(self, routine_name: str, retakes: RoutineRetakes) -> None:
            self.update_days(routine_name, retakes.days)
            self.update_time(routine_name, retakes.times)

        def update_days(self, routine_name: str, days: RoutineDays) -> None:
            (
                monday,
                tuesday,
                wednesday,
                thursday,
                friday,
                saturday,
                sunday,
                specific_dates,
            ) = days.as_tuple()
            statement: str = (
                "UPDATE routine SET monday=?, tuesday=?, wednesday=?, thursday=?, friday=?, saturday=?, "
                "sunday=? WHERE name=?"
            )
            cursor: Cursor = self.db.cursor()
            cursor.execute(
                statement,
                (
                    monday,
                    tuesday,
                    wednesday,
                    thursday,
                    friday,
                    saturday,
                    sunday,
                    routine_name,
                ),
            )
            cursor.close()

            self.update_specific_dates(routine_name, specific_dates)

        def update_time(self, routine_name: str, routine_time: RoutineTime):
            (
                times,
                after_alarm,
                after_sunrise,
                after_sunset,
                after_call,
            ) = routine_time.as_tuple()
            self.update_clock_times(times)
            statement: str = "UPDATE routine SET afteralarm=?, aftersunrise=?, aftersunset=?, aftercall=? WHERE name=?"
            cursor: Cursor = self.db.cursor()
            cursor.execute(
                statement,
                (
                    after_alarm,
                    after_sunrise,
                    after_sunset,
                    after_call,
                    routine_name,
                ),
            )
            cursor.close()

        def update_specific_dates(
                self, routine_name: str, specific_dates: list[SpecificDate]
        ) -> None:
            statement: str = "UPDATE routinedates SET rdid=?, rname=?, date=?"
            cursor: Cursor = self.db.cursor()
            cursor.executemany(
                statement,
                [
                    (
                        routine_name,
                        sd.sid,
                        sd.date.isoformat(),
                    )
                    for sd in specific_dates
                ],
            )
            cursor.close()

        def update_clock_times(self, clock_times: list[RoutineClockTime]) -> None:
            statement: str = (
                "UPDATE routineactivationtime SET ratid=?, time=? WHERE ratid=?"
            )
            cursor: Cursor = self.db.cursor()
            cursor.executemany(statement, clock_times)
            cursor.close()

        def update_clock_time(self, clock_time: RoutineClockTime) -> None:
            statement: str = (
                "UPDATE routineactivationtime SET ratid=?, time=? WHERE ratid=?"
            )
            cursor: Cursor = self.db.cursor()
            cursor.execute(
                statement, (clock_time.ratid, clock_time.clock_time.isoformat())
            )
            cursor.close()

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
            return counter

        def delete_routine_command(self, routine_command_id: int):
            cursor: Cursor = self.db.cursor()
            statement: str = "DELETE FROM commandtext WHERE rcid=?"
            cursor.execute(statement, (routine_command_id,))
            statement: str = "DELETE FROM routinecommands WHERE rcid=?"
            cursor.execute(statement, (routine_command_id,))
            cursor.close()

        def delete_on_command(self, on_command_id: int):
            statement: str = "DELETE FROM oncommand WHERE ocid=?"
            cursor: Cursor = self.db.cursor()
            cursor.execute(statement, (on_command_id,))
            cursor.close()

        def delete_routine_dates(self, routine_date_id: int):
            with self.db.cursor() as cursor:
                statement: str = "DELETE FROM routinedates WHERE rdid=?"
                cursor.execute(statement, (routine_date_id,))

        def delete_routine_activation_time(self, routine_activation_time_id: int):
            statement: str = "DELETE FROM routineactivationtime WHERE ratid=?"
            cursor: Cursor = self.db.cursor()
            cursor.execute(statement, (routine_activation_time_id,))
            cursor.close()

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

        def __create_table(self):
            pass

        def __tuple_to_routine(
                self,
                routine_tuple: tuple,
        ) -> Routine:
            # toDo: get actions of routine
            if not routine_tuple:
                raise NoMatchingEntry()
            cursor: Cursor = self.db.cursor()
            (
                name,
                description,
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
            ) = routine_tuple

            routine_dates_statement: str = "SELECT * FROM routinedates WHERE rname=?"
            cursor.execute(routine_dates_statement, (name,))

            routine_dates: list[SpecificDate] = [
                SpecificDate(date=datetime.fromisoformat(date), sid=sid)
                for sid, _, date in cursor.fetchall()
            ]

            on_command_statement: str = "SELECT * FROM oncommand WHERE rname=?"
            cursor.execute(on_command_statement, (name,))

            on_commands: list[CallingCommand] = [
                CallingCommand(
                    ocid=on_command_id, routine_name=routine_name, command=command
                )
                for on_command_id, routine_name, command, in cursor.fetchall()
            ]

            routine_days: RoutineDays = RoutineDays(
                monday=monday,
                tuesday=tuesday,
                wednesday=wednesday,
                thursday=thursday,
                friday=friday,
                saturday=saturday,
                sunday=sunday,
                routine_dates=routine_dates,
            )

            routine_activation_times_statement: str = (
                "SELECT * FROM routineactivationtime WHERE rname=?"
            )
            cursor.execute(routine_activation_times_statement, (name,))

            clock_times: list[RoutineClockTime] = [
                RoutineClockTime(
                    clock_time=time.fromisoformat(routine_time),
                    ratid=routine_clock_time_id,
                )
                for routine_clock_time_id, _, routine_time in cursor.fetchall()
            ]
            cursor.close()
            routine_times: RoutineTime = RoutineTime(
                clock_times=clock_times,
                after_alarm=after_alarm,
                after_sunrise=after_sunrise,
                after_sunset=after_sunset,
                after_call=after_call,
            )

            retakes: RoutineRetakes = RoutineRetakes(
                days=routine_days, times=routine_times
            )

            actions: list[RoutineCommand] = self.__get_routine_commands(name)

            return Routine(
                name=name,
                description=description,
                calling_commands=on_commands,
                retakes=retakes,
                actions=actions,
            )

        def __get_routine_commands(self, routine_name: str) -> list[RoutineCommand]:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM routinecommands WHERE rname=?"
            cursor.execute(statement, (routine_name,))
            commands: list[RoutineCommand] = [
                RoutineCommand(
                    module_name=module_name,
                    with_text=self.__get_texts_of_command(routine_command_id),
                    cid=routine_command_id,
                )
                for routine_command_id, _, module_name in cursor.fetchall()
            ]
            cursor.close()
            return commands

        def __get_texts_of_command(self, routine_id: int) -> list[str]:
            cursor: Cursor = self.db.cursor()
            statement: str = "SELECT * FROM commandtext WHERE cid=?"
            cursor.execute(statement, (routine_id,))
            text_list: list[str] = [text for _, text in cursor.fetchall()]
            cursor.close()
            return text_list

    class _QuizInterface:
        def __init__(self, _db: Connection) -> None:
            self.db: Connection = _db
            log.info("QuizInterface initialized.")

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

        def add_birthday(self, birthday: Birthday) -> None:
            cursor: Cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO birthdays VALUES (?, ?, ?, ?, ?)",
                (
                    birthday.first_name,
                    birthday.last_name,
                    birthday.date.isoformat(),
                ),
            )
            cursor.close()

        def get_birthday(self, first_name: str, last_name: str) -> Birthday:
            cursor: Cursor = self.db.cursor()
            statement: str = (
                "SELECT * FROM birthdays WHERE firstname=? AND lastname=? LIMIT 1"
            )
            cursor.execute(statement, (first_name, last_name))
            birthday: Birthday = self.__tuple_to_birthday(cursor.fetchone())
            cursor.close()
            return birthday

        def get_all_birthdays(self) -> list[Birthday]:
            cursor: Cursor = self.db.cursor()
            cursor.execute(f"SELECT * FROM birthdays")
            birthdays: list[Birthday] = [
                self.__tuple_to_birthday(birthday) for birthday in cursor.fetchall()
            ]
            cursor.close()
            return birthdays

        def update_birthday(
                self, old_first_name: str, old_last_name: str, birthday: Birthday
        ) -> Birthday:
            statement: str = "UPDATE birthdays SET firstname=?, lastname=?, date=? WHERE firstname=? AND lastname=?"
            cursor: Cursor = self.db.cursor()
            first_name, last_name, date = birthday
            cursor.execute(
                statement,
                (
                    first_name,
                    last_name,
                    date.isoformat(),
                    old_first_name,
                    old_last_name,
                ),
            )
            cursor.close()
            return birthday

        def delete_birthday(self, first_name: str, last_name: str) -> None:
            cursor: Cursor = self.db.cursor()
            cursor.execute(
                "DELETE FROM birthdays WHERE firstname=? AND lastname=?",
                (first_name, last_name),
            )
            cursor.close()

        @staticmethod
        def __tuple_to_birthday(result_set: tuple) -> Birthday:
            first_name, last_name, date = result_set
            return Birthday(first_name, last_name, datetime.fromisoformat(date))


if __name__ == "__main__":
    db = DataBase()
    routine: Routine = Routine(
        name="Test Routine", description="Checken, ob alles klappt"
    )

    routine.add_calling_command("Ich bin wach")
    routine.add_routine_command(
        RoutineCommand(module_name="phue", with_text=["blau", "grün"])
    )
    print(db.routine_interface.add_routine(routine))

    print(db.routine_interface.get_routine("Test Routine"))
    print(db.routine_interface.get_routines())
    routine.description = "lel"
    routine.retakes.days.monday = True
    routine.retakes.days.friday = True
    routine.retakes.days.sunday = True
    routine.retakes.times.after_alarm = True

    print(db.routine_interface.update_routine("Ich bin wach", routine))
