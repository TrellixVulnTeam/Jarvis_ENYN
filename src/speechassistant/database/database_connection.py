from __future__ import annotations  # compatibility for < 3.10

import io
import json
import pathlib
from datetime import datetime
from typing import Callable, TypeAlias  # , TypeAlias
import os
import sqlite3
from sqlite3 import Connection, Cursor, OperationalError

from src.speechassistant.exceptions.CriticalExceptions import UnsolvableException
from src.speechassistant.resources.enums import OutputTypes
from src.speechassistant.exceptions.SQLException import *

shopping_item: TypeAlias = dict[[str, int], [str, str], [str, str], [str, float]]
timer_item: TypeAlias = dict[[str, int], [str, str], [str, str], [str, int]]
user_item: TypeAlias = dict[
    [str, int], [str, str], [str, str], [str, str], [str, dict[str, int], [str, int], [str, int]], [str, int], [str,
                                                                                                                int], [
        str, list[str]]]
routine_item: TypeAlias = dict[[str, str], [str, dict], [str, dict], [str, dict]]

from src.speechassistant.resources.module_skills import Skills


# toDo: as_tuple -> output_type: OutputTypes
# toDo: close cursor before raise

class DataBase:
    def __init__(self, root_path: str, skills: Skills) -> None:
        logging.basicConfig(level=logging.DEBUG)
        logging.info('[ACTION] Initialize DataBase...\n')
        self.db: Connection = sqlite3.connect(os.path.join(root_path, 'database', 'data_base'), check_same_thread=False)
        self.error_counter: int = 0

        self.user_interface = self._UserInterface(self.db)
        self.alarm_interface = self._AlarmInterface(self.db, skills)
        self.timer_interface = self._TimerInterface(self.db, self.user_interface)
        self.reminder_interface = self._ReminderInterface(self.db, self.user_interface)
        self.quiz_interface = self._QuizInterface(self.db)
        self.shoppinglist_interface = self._ShoppingListInterface(self.db)
        self.routine_interface = self._RoutineInterface(self.db)
        self.audio_interface = self._AudioInterface(self.db)
        self.messenger_interface = self._MessangerInterface()
        self.birthday_interface = self._BirthdayInterface(self.db)
        self.__audio_path: str = ''

        self.create_tables()

        logging.info('[INFO] DataBase successfully initialized.')

    def create_tables(self) -> None:
        # toDo: CONSTRAINTS

        # CHECK (mycolumn IN (0, 1)) -> BOOL

        logging.info('[ACTION] Create tables...')
        self.__create_table('CREATE TABLE IF NOT EXISTS audio ('
                            'name VARCHAR(30) PRIMARY KEY UNIQUE,'
                            'path VARCHAR(50) UNIQUE)')

        self.__create_table('CREATE TABLE IF NOT EXISTS user ('
                            'uid INTEGER PRIMARY KEY,'
                            'alias VARCHAR(10) UNIQUE,'
                            'firstname VARCHAR(15),'
                            'lastname VARCHAR(30),'
                            'birthday VARCHAR(10),'
                            'mid INTEGER,'
                            'sname VARCHAR(30),'
                            'FOREIGN KEY(sname) REFERENCES audio(name))')

        self.__create_table('CREATE TABLE IF NOT EXISTS alarm ('
                            'aid INTEGER PRIMARY KEY, '
                            'sname VARCHAR(30), '
                            'uid INTEGER, '
                            'hour INTEGER, '
                            'minute INTEGER, '
                            'total_seconds UNSIGNED BIG INT, '
                            'text VARCHAR(255), '
                            'active INTEGER, '
                            'initiated INTEGER, '
                            'last_executed VARCHAR(10), '
                            'FOREIGN KEY(sname) REFERENCES audio(name), '
                            'FOREIGN KEY(uid) REFERENCES user(uid))'
                            )

        self.__create_table('CREATE TABLE IF NOT EXISTS alarmrepeat ('
                            'aid INTEGER PRIMARY KEY UNIQUE,'
                            'monday INTEGER,'
                            'tuesday INTEGER,'
                            'wednesday INTEGER,'
                            'thursday INTEGER,'
                            'friday INTEGER ,'
                            'saturday INTEGER,'
                            'sunday INTEGER, '
                            'regular INTEGER, '
                            'FOREIGN KEY(aid) REFERENCES alarm(aid))')

        self.__create_table('CREATE TABLE IF NOT EXISTS timer ('
                            'id INTEGER PRIMARY KEY,'
                            'duration VARCHAR(50), '
                            'time VARCHAR(25),'
                            'text VARCHAR(255),'
                            'uid INTEGER,'
                            'FOREIGN KEY(uid) REFERENCES user(uid))')

        self.__create_table('CREATE TABLE IF NOT EXISTS shoppinglist ('
                            'id INTEGER PRIMARY KEY,'
                            'name varchar(50) UNIQUE,'
                            'measure varchar(4),'
                            'quantity FLOAT)')

        self.__create_table('CREATE TABLE IF NOT EXISTS reminder ('
                            'id INTEGER PRIMARY KEY,'
                            'time VARCHAR(19),'
                            'text VARCHAR(255),'
                            'uid INTEGER,'
                            'FOREIGN KEY(uid) REFERENCES user(uid))')

        self.__create_table('CREATE TABLE IF NOT EXISTS routine ('
                            'name VARCHAR(50) PRIMARY KEY, '
                            'description VARCHAR(255), '
                            'daily INTEGER, '
                            'monday INTEGER, '
                            'tuesday INTEGER, '
                            'wednesday INTEGER, '
                            'thursday INTEGER, '
                            'friday INTEGER, '
                            'saturday INTEGER, '
                            'sunday INTEGER, '
                            'afteralarm INTEGER, '
                            'aftersunrise INTEGER, '
                            'aftersunset INTEGER, '
                            'aftercall INTEGER)')

        self.__create_table('CREATE TABLE IF NOT EXISTS oncommand ( '
                            'ocid INTEGER PRIMARY KEY, '
                            'rname VARCHAR(50), '
                            'command VARCHAR(255), '
                            'FOREIGN KEY(rname) REFERENCES routine(rname)'
                            'UNIQUE (rname, command))')

        self.__create_table('CREATE TABLE IF NOT EXISTS routineactivationtime ('
                            'ratid INTEGER PRIMARY KEY, '
                            'rname VARCHAR(50), '
                            'hour INTEGER, '
                            'minute INTEGER, '
                            'FOREIGN KEY(rname) REFERENCES routine(rname), '
                            'UNIQUE (rname, hour, minute))')

        self.__create_table('CREATE TABLE IF NOT EXISTS routinedates ('
                            'rdid INTEGER PRIMARY KEY, '
                            'rname VARCHAR(50), '
                            'day INTEGER, '
                            'month INTEGER, '
                            'UNIQUE (rname, day, month), '
                            'FOREIGN KEY(rname) REFERENCES routine(rname))')

        self.__create_table('CREATE TABLE IF NOT EXISTS routinecommands ('
                            'rcid INTEGER PRIMARY KEY, '
                            'rname VARCHAR(50), '
                            'modulename VARCHAR(50), '
                            'FOREIGN KEY(rname) REFERENCES routine(rname))')

        self.__create_table('CREATE TABLE IF NOT EXISTS commandtext ('
                            'cid INTEGER,'
                            'text VARCHAR(255) NOT NULL,'
                            'PRIMARY KEY(cid, text),'
                            'FOREIGN KEY(cid) REFERENCES routinecommands(rcid), '
                            'UNIQUE(cid, text))')

        self.__create_table('CREATE TABLE IF NOT EXISTS quiz ('
                            'category VARCHAR(50) PRIMARY KEY)')

        self.__create_table('CREATE TABLE IF NOT EXISTS questions ('
                            'qid INTEGER PRIMARY KEY,'
                            'category REFERENCES quiz(category),'
                            'starting INTEGER,'
                            'question VARCHAR(255),'
                            'audio VARCHAR(30),'
                            'answer VARCHAR(255),'
                            'FOREIGN KEY(audio) REFERENCES audio(name))')

        self.__create_table('CREATE TABLE IF NOT EXISTS answeroptions ('
                            'category REFERENCES quiz(category),'
                            'text VARCHAR(255),'
                            'PRIMARY KEY(category, text))')

        self.__create_table('CREATE TABLE IF NOT EXISTS notification ('
                            'uid INTEGER,'
                            'text VARCHAR(255),'
                            'PRIMARY KEY(uid, text),'
                            'FOREIGN KEY(uid) REFERENCES user(uid))')

        # self.__create_table('CREATE TABLE IF NOT EXISTS messenger notifications')
        self.__create_table('CREATE TABLE IF NOT EXISTS birthdays ('
                            'firstname VARCHAR(15), '
                            'lastname VARCHAR(30), '
                            'day INTEGER, '
                            'month INTEGER, '
                            'year INTEGER, '
                            'PRIMARY KEY(firstname, lastname), '
                            'UNIQUE (firstname, lastname))')

        # #self.db.commit()

        if self.error_counter == 0:
            logging.info('[INFO] Tables successfully created!')
        else:
            msg: str = f'During the creation of {self.error_counter} tables there were problems. Manual intervention ' \
                       f'mandatory. '
            raise UnsolvableException(msg)

    def __create_table(self, command: str) -> None:
        cursor: Cursor = self.db.cursor()
        try:
            cursor.execute(command)
            logging.info(f"[INFO] Successfully created table {command.split(' ')[5]}!")
        except Exception as e:
            self.error_counter += 1
            logging.warning(f"[ERROR] Couldn't create table {command.split(' ')[5]}:\n {e}")
        cursor.close()
        self.db.commit()

    def __remove_tables(self):
        pass

    def stop(self):
        logging.info('[ACTION] Stopping database...')
        self.db.commit()
        self.db.close()

    class _UserInterface:
        def __init__(self, db: Connection) -> None:
            self.db: Connection = db
            logging.info('[INFO] UserInterface initialized.')

        def get_user(self, user: str | int) -> user_item:
            cursor: Cursor = self.db.cursor()
            if type(user) is str:
                user: int = self.__get_user_id(user)

            statement: str = f'SELECT * from user WHERE uid=? LIMIT 1'

            cursor.execute(statement, (user,))

            result_set: list[tuple[int, str, str, str, str, int, int]] = cursor.fetchone()
            cursor.close()
            return self.__build_json(result_set)

        def get_user_by_messenger_id(self, messenger_id: int) -> user_item:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * FROM user WHERE mid=? LIMIT 1'
            cursor.execute(statement, (messenger_id,))
            result_set: list[tuple] = cursor.fetchone()
            cursor.close()
            return self.__build_json(result_set)

        def get_users(self) -> list[user_item]:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * from user'
            cursor.execute(statement)
            result_set: list[tuple[int, str, str, str, str, int, int]] = cursor.fetchall()

            user_list: list[user_item] = self.__build_json(result_set)

            for user in user_list:
                notification_statement: str = f'SELECT text FROM notification WHERE uid=?'
                cursor.execute(notification_statement, (user.get("uid"),))
                notification_result_set: list[tuple] = cursor.fetchall()
                for text, in notification_result_set:
                    user["waiting_notifications"].append(text)
            cursor.close()
            return user_list

        def add_user(self, alias: str, firstname: str, lastname: str, birthday: dict, messenger_id: int = 0,
                     song_id: int = 1) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = f'INSERT INTO user (alias, firstname, lastname, birthday, mid, sname) ' \
                             f'VALUES (?, ?, ?, ?, ?, ?)'
            cursor.execute(statement, (alias, firstname, lastname, self.__birthday_to_string(birthday),
                                       messenger_id, song_id))
            uid: int = cursor.lastrowid
            cursor.close()
            self.db.commit()
            return uid

        def add_user_notification(self, user: int | str, notification: str) -> None:
            cursor: Cursor = self.db.cursor()

            if type(user) is str:
                user: int = self.__get_user_id(user)

            statement: str = f'INSERT INTO notification (uid, text) VALUES (?, ?)'
            cursor.execute(statement, (user, notification))
            cursor.close()
            self.db.commit()

        # The first line of attributes is for mapping purposes only, so that the user can be specified more easily
        def update_user(self, uid: int = None, alias: str = None, first_name: str = None, last_name: str = None,
                        _new_alias: str = None, _new_first_name: str = None, _new_last_name: str = None,
                        _birthday: dict = None, _messenger_id: int = 0, _song_name: str = 'standard'):

            cursor: Cursor = self.db.cursor()

            if uid is not None:
                statement: str = 'SELECT * FROM user WHERE uid=? LIMIT 1'
                cursor.execute(statement, (uid,))
                result_set: tuple = cursor.fetchone()
                if cursor.rowcount < 1:
                    cursor.close()
                    raise NoMatchingEntry(f'No matching user with the user-id {uid} was found in the database.')

            elif alias is not None:
                statement: str = 'SELECT * FROM user WHERE alias=? LIMIT 1'
                cursor.execute(statement, (alias,))
                result_set: tuple = cursor.fetchone()
                if cursor.rowcount < 1:
                    cursor.close()
                    raise NoMatchingEntry(f'No matching user with the alias "{alias}" was found in the database.')

            elif first_name is not None and last_name is not None:
                statement: str = """SELECT * FROM user
                                    WHERE firstname=?
                                    AND lastname=?
                                    LIMIT 1"""

                cursor.execute(statement, (first_name, last_name))
                result_set: tuple = cursor.fetchone()
                if cursor.rowcount < 1:
                    cursor.close()
                    raise NoMatchingEntry(f'No matching user with the name "{last_name, first_name}" was found '
                                          f'in the database.')
            else:
                cursor.close()
                raise ValueError('No suitable description of a user given. Either the uid, the alias or first '
                                 'and last name is required!')

            uid, alias, firstname, lastname, birthday, mid, sname = result_set

            if _new_alias is not None:
                alias = _new_alias
            if _new_first_name is not None:
                firstname = _new_first_name
            if _new_last_name is not None:
                lastname = _new_last_name
            if _birthday is not None:
                birthday = self.__birthday_to_string(_birthday)
            mid = _messenger_id

            statement: str = """UPDATE user 
                                SET alias=?, firstname=?, lastname=?, 
                                birthday=?, mid=?, sname=? 
                                WHERE uid=?"""
            cursor.execute(statement,
                           (alias, firstname, lastname, self.__birthday_to_string(birthday), mid, sname, uid))
            cursor.close()
            self.db.commit()

        def delete_user_notification(self, user: int | str, text: str) -> None:
            cursor: Cursor = self.db.cursor()

            if type(user) is str:
                user: int = self.__get_user_id(user)

            statement: str = 'DELETE FROM notification WHERE uid=? AND text=?'
            cursor.execute(statement, (user, text))
            cursor.close()
            self.db.commit()

        def delete_user(self, user: int | str) -> None:
            cursor: Cursor = self.db.cursor()

            if type(user) is str:
                user: int = self.__get_user_id(user)

            statement: str = 'DELETE FROM user WHERE uid=?'

            cursor.execute(statement, (user,))
            cursor.close()
            self.db.commit()

        @staticmethod
        def __birthday_to_string(birthday: dict) -> str:
            return str(birthday.get('year')) + str(birthday.get('month')).rjust(2, '0') + str(
                birthday.get('day')).rjust(2, '0')

        def __get_user_id(self, alias: str) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT uid FROM user WHERE alias=? LIMIT 1'
            cursor.execute(statement, (alias,))
            uid: int = cursor.fetchone()
            cursor.close()
            if uid:
                return uid
            else:
                raise UserNotFountException()

        def __create_table(self):
            pass

        def __build_json(self, result_set: list[tuple] | tuple) -> list[dict] | dict:
            if type(result_set) is list:
                result_list: list[dict] = []

                for dataset in result_set:
                    result_list.append(self.__tuple_to_dict(dataset))
                return result_list
            else:
                return self.__tuple_to_dict(result_set)

        @staticmethod
        def __tuple_to_dict(dataset: tuple) -> dict:
            uid, alias, firstname, lastname, birthday, mid, sname = dataset
            return {
                "uid": uid,
                "name": alias,
                "first_name": firstname,
                "last_name": lastname,
                "date_of_birth": {
                    "year": birthday[0:4],
                    "month": birthday[4:6],
                    "day": birthday[6:8]
                },
                "messenger_id": mid,
                "alarm_sound": sname,
                "waiting_notifications": []
            }

    class _AlarmInterface:
        def __init__(self, db: Connection, skills: Skills) -> None:
            self.db: Connection = db
            self.skills = skills
            logging.info('[INFO] AlarmInterface initialized.')

        def get_alarm(self, aid: int, as_tuple: bool = False) -> tuple | dict:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * FROM alarm as a JOIN alarmrepeat as ar ON a.aid=ar.aid WHERE aid=? LIMIT 1'
            cursor.execute(statement, (aid,))
            result_set: tuple = cursor.fetchone()
            cursor.close()
            return self.__build_json([result_set], as_tuple)[0]

        def get_alarms(self, active: bool = False, unsorted: bool = False, as_tuple: bool = False) -> \
                list[dict] | list[tuple] | tuple[list, list]:
            cursor: Cursor = self.db.cursor()
            init_result_set: list = []
            if unsorted:
                if active:
                    statement: str = 'SELECT * FROM alarm as a JOIN alarmrepeat as ar ON a.aid=ar.aid'
                else:
                    statement: str = """SELECT * FROM alarm as a 
                                        JOIN alarmrepeat as ar ON a.aid=ar.aid 
                                        WHERE a.active=True"""
                cursor.execute(statement)
                result_set: list[tuple] = cursor.fetchall()
                cursor.close()
                return self.__build_json(result_set, as_tuple)

            if active:
                now: datetime = datetime.now()
                weekday: str = self.skills.statics.numb_to_day[str(now.weekday())]
                now_seconds = now.hour * 3600 + now.minute * 60 + now.second
                active_alarms_statement: str = f'SELECT * FROM alarm as a ' \
                                               f'JOIN alarmrepeat as ar ON a.aid = ar.aid ' \
                                               f'WHERE aid.{weekday}=1 ' \
                                               f'AND a.hour >= {now.hour} ' \
                                               f'AND a.minute >= {now.minute} ' \
                                               f'AND a.active=1 ' \
                                               f'AND a.last_executed != {now.day}.{now.month}.{now.year}'
                init_alarms_statement: str = f'SELECT * FROM alarm as a ' \
                                             f'JOIN alarmrepeat as ar ON a.aid = ar.aid ' \
                                             f'WHERE aid.{weekday}=1 ' \
                                             f'AND a.total_seconds <= {now_seconds + 1800}'
                cursor.execute(init_alarms_statement)
                init_result_set: list[tuple] = cursor.fetchall()
            else:
                active_alarms_statement: str = 'SELECT * FROM alarm as a ' \
                                               'JOIN alarmrepeat as ar ON a.aid = ar.aid'
            cursor.execute(active_alarms_statement)
            active_result_set: list[tuple] = cursor.fetchall()
            active_returning_list: list[dict] = self.__build_json(active_result_set, as_tuple)
            init_returning_list: list[dict] = self.__build_json(init_result_set, as_tuple)
            cursor.close()
            return active_returning_list, init_returning_list

        def add_alarm(self, time: dict, text: str, user: int | str, repeating: dict, active: bool = True,
                      initiated: bool = False, song: str = 'standard.wav') -> int:
            cursor: Cursor = self.db.cursor()
            if type(user) is str:
                user = self.__get_user_id(user)

            statement: str = """INSERT INTO alarm (sname, uid, hour, minute, total_seconds, text, active, 
                                initiated, last_executed) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, "")"""

            cursor.execute(statement, (song, user, time["hour"], time["minute"], time["total_seconds"], text,
                                       int(active), int(initiated)))
            alarm_id: int = cursor.lastrowid

            statement: str = f'INSERT INTO alarmrepeat VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
            values: list = [alarm_id]
            for item in repeating.keys():
                values.append(str(int(repeating.get(item))))
            cursor.execute(statement, tuple(values))
            aid: int = cursor.lastrowid
            cursor.close()
            self.db.commit()
            return aid

        def delete_alarm(self, aid: int) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = 'DELETE FROM alarm WHERE aid=?'
            cursor.execute(statement, (aid,))
            anz_removed_alarm: int = cursor.rowcount
            statement = 'DELETE FROM alarmrepeat WHERE aid=?'
            cursor.execute(statement, (aid,))
            anz_removed_repeat: int = cursor.rowcount

            if anz_removed_alarm != anz_removed_repeat and anz_removed_alarm < 1:
                cursor.close()
                # toDo: maybe use another SQLException
                raise UnsolvableException('Removed more alarm repeating´s than alarms!')
            cursor.close()
            self.db.commit()
            return anz_removed_alarm

        def update_alarm(self, aid: int, _time: dict = None, _text: str = None, _user: int | str = None,
                         _active: bool = None, _initiated: bool = None, _regular: bool = None, _sound: str = None,
                         _last_executed: str = None) -> None:
            cursor: Cursor = self.db.cursor()
            # If there is no item with the name, the user should be told about it and not just not update anything
            statement: str = 'SELECT * FROM alarm WHERE aid=? LIMIT 1'
            cursor.execute(statement, (aid,))
            result_set: tuple = cursor.fetchone()
            if result_set is None:
                cursor.close()
                raise NoMatchingEntry(f'No matching element with the alarm-id {aid} was found in the database.')

            aid, sname, uid, hour, minute, total_seconds, text, active, initiated, last_executed = result_set

            if _time is not None:
                hour = _time["hour"]
                minute = _time["minute"]
            if _text is not None:
                text = _text
            if _user is not None:
                if type(_user) is str:
                    statement: str = 'SELECT uid FROM user WHERE name=? LIMIT 1'
                    cursor.execute(statement, (_user,))
                    uid: int = cursor.fetchone()
                    if cursor.rowcount < 1:
                        cursor.close()
                        raise NoMatchingEntry(f'No user found with name "{_user}.')
                else:
                    uid = _user
            if _active is not None:
                active = int(_active is True)
            if _initiated is not None:
                initiated = int(_initiated is True)
            if _sound is not None:
                sname = _sound
            if _last_executed is not None:
                if len(_last_executed) > 10:
                    cursor.close()
                    raise ValueError('Given last_executed was too long! Max length for last_executed is 10 chars.')
                last_executed = _last_executed

            statement: str = f'UPDATE alarm SET sname=?, uid=?, hour=?, minute=?, total_seconds=?, text=?, active=?, ' \
                             f'initiaded=?, last_executed=? WHERE aid=?'
            cursor.execute(statement, (sname, uid, hour, minute, total_seconds, text, active, initiated, last_executed,
                                       aid))
            cursor.close()
            self.db.commit()

        def update_repeating(self, aid: int, _monday: bool = None, _tuesday: bool = None, _wednesday: bool = None,
                             _thursday: bool = None, _friday: bool = None, _saturday: bool = None,
                             _sunday: bool = None):
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * FROM alarmrepeat WHERE aid=?'
            cursor.execute(statement, (aid,))
            if cursor.rowcount == 0:
                cursor.close()
                raise NoMatchingEntry(f'No matching element with the id {aid} was found in the database.')
            result_set: tuple = cursor.fetchone()

            aid, monday, tuesday, wednesday, thursday, friday, saturday, sunday = result_set

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

            statement: str = f'UPDATE alarmrepeat ' \
                             f'SET monday=?, tuesday=?, wednesday=?, thursday=?, friday=?, saturday=?, sunday=? ' \
                             f'WHERE aid=?'
            cursor.execute(statement, (monday, tuesday, wednesday, thursday, friday, saturday, sunday, aid))
            cursor.close()
            self.db.commit()

        def __build_json(self, result_set: list[tuple], as_tuple: bool = False) -> list[dict] | list[tuple]:
            # toDo: add alarmrepeat

            cursor: Cursor = self.db.cursor()

            if as_tuple:
                result_list: list[tuple] = []
                for aid, sname, uid, hour, minute, total_seconds, text, active, initiated, last_executed in result_set:
                    time = {"hour": hour, "minute": minute, "total_seconds": total_seconds}
                    result_list.append((aid, time, sname, uid, text, active, initiated, last_executed))
                return result_list

            result_list: list[dict] = []
            for aid, sname, uid, hour, minute, total_seconds, text, active, initiated, last_executed, _, monday, tuesday, wednesday, thursday, friday, saturday, sunday, regular in result_set:
                statement: str = 'SELECT path FROM audio WHERE name=?'
                cursor.execute(statement, (sname,))
                sound_path: str = cursor.fetchone()
                result_list.append({
                    "id": aid,
                    "time": {
                        "hour": hour,
                        "minute": minute,
                        "total_seconds": total_seconds
                    },
                    "sound": sound_path,
                    "user": uid,
                    "text": text,
                    "active": (active == 1),
                    "initiated": (initiated == 1),
                    "last_executed": last_executed,
                    "monday": monday,
                    "tuesday": tuesday,
                    "wednesday": wednesday,
                    "thursday": thursday,
                    "friday": friday,
                    "saturday": saturday,
                    "sunday": sunday,
                    "regular": regular
                })
            cursor.close()
            return result_list

        def __get_user_id(self, alias: str) -> int:
            cursor = self.db.cursor()
            cursor.execute('SELECT uid FROM user WHERE alias=?', (alias,))
            uid: int = cursor.fetchone()
            cursor.close()
            if uid is not None:
                return uid
            else:
                raise UserNotFountException()

        def __create_table(self):
            pass

    class _AudioInterface:

        def __init__(self, db: Connection) -> None:
            self.db: Connection = db
            self.audio_path: str = 'C:\\Users\\Jakob\\PycharmProjects\\Jarvis'
            logging.info('[INFO] AudioInterface initialized.')

        def add_audio(self, name: str, path: str = None, audio_file: io.BytesIO = None,
                      file_stored: bool = False) -> None:
            # IMPORTANT: file_stored allows the developer to add a file to the database which is still in the file
            # folder of the system. There will be problems, if the name is not correct or the file is not in the
            # path. Be carefully while using this attribute !!!
            cursor: Cursor = self.db.cursor()
            if path is not None:
                statement: str = 'SELECT name FROM audio WHERE path=?'
                cursor.execute(statement, (path,))
                if cursor.rowcount > 0:
                    cursor.close()
                    raise FileNameAlreadyExists()
            if name is not None:
                statement: str = 'SELECT name FROM audio WHERE name=?'
                cursor.execute(statement, (audio_file,))
                if cursor.rowcount > 0:
                    cursor.close()
                    raise FileNameAlreadyExists()

            if not file_stored:
                if path is not None and audio_file is not None:
                    cursor.close()
                    raise ValueError('Got too many arguments! Decide between the path and the audio file.')
                elif path is None and audio_file is None:
                    cursor.close()
                    raise ValueError('Neither path nor audio file given!')
                else:
                    if path is not None:
                        path = self.__justify_file_path(name, path)
                    elif audio_file is not None:
                        self.__save_audio_file(name, audio_file)
                        path = self.audio_path + f'{name}.wav'
            statement: str = 'INSERT INTO audio (name, path) VALUES (?, ?)'
            cursor.execute(statement, (name, path))
            cursor.close()
            self.db.commit()

        def update_audio(self, _audio_name: str, _new_audio_name: str = None, _path: str = None,
                         _audio_file: io.BytesIO = None) -> str:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * FROM audio WHERE name=?'
            cursor.execute(statement, (_audio_name,))
            result_set: tuple = cursor.fetchone()
            if cursor.rowcount < 1:
                cursor.close()
                raise NoMatchingEntry(f'No matching element with the audio name "{_audio_name}" was found '
                                      f'in the database.')

            name, path = result_set

            if _new_audio_name is not None:
                name = _new_audio_name
                os.rename(os.path.join(self.audio_path, _audio_name), os.path.join(self.audio_path, name))
            if _path is not None and _audio_file is not None:
                cursor.close()
                raise ValueError('Got too many arguments! Decide between the path and the audio file.')
            elif _path is not None:
                # old_path is needed after the SQL query
                old_path: str = _path
                path = self.__justify_file_path(_audio_name, _path)
            elif _audio_file is not None:
                statement: str = 'SELECT path FROM audio WHERE name=?'
                cursor.execute(statement, (_audio_name,))
                file_path: str = cursor.fetchone()
                os.remove(file_path)
                self.__save_audio_file(_audio_name, _audio_file)
                path = self.audio_path + _audio_name

            statement: str = """UPDATE audio 
                                SET name=?, path=? 
                                WHERE name=?"""
            cursor.execute(statement, (name, path, _audio_name))

            # delete file only after database access has worked
            if _path is not None:
                # delete file, if no other entry in the database uses it
                statement: str = 'SELECT name FROM audio WHERE path=?'
                cursor.execute(statement, (old_path,))
                if cursor.rowcount == 0:
                    os.remove(old_path)
                    logging.info(f'[ACTION] Audio file deleted ({old_path})')
            cursor.close()
            self.db.commit()
            return name

        def get_audio_file(self, audio: str, as_tuple: bool = False) -> tuple | dict:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * FROM audio WHERE name=?'
            cursor.execute(statement, (audio,))
            result_set: tuple = cursor.fetchone()
            cursor.close()
            if as_tuple:
                return result_set
            else:
                name, path = result_set
                return {"name": name, "path": path}

        def get_file_names(self) -> list[str]:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT name FROM audio'
            result_set: list[tuple] = cursor.fetchall()
            cursor.close()
            # return only filenames
            return [x[0] for x in result_set]

        def delete_audio(self, audio_name: str) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT path FROM audio WHERE name=?'
            cursor.execute(statement, (audio_name,))
            file_path: str = cursor.fetchone()
            statement = 'DELETE FROM audio WHERE name=?'
            cursor.execute(statement, (audio_name,))
            anz_removed: int = cursor.rowcount
            cursor.close()
            if type(anz_removed) is list:
                raise UnsolvableException('DataBase returned wrong type while deleting an entry!')
            self.db.commit()
            # delete file only after database access has worked
            os.remove(file_path)
            logging.info(f'[ACTION] Deleted audiofile "{file_path}".')
            return anz_removed

        def __justify_file_path(self, name: str, path: str) -> str:
            if not os.path.isfile(path):
                if not os.path.isfile(self.audio_path + path):
                    raise ValueError(
                        f'File "{path}" is neither in the folder of audio files, nor a valid path to an audio file!')
                else:
                    # move the file into the audio folder of the speech assistant
                    os.replace(path, self.audio_path + name + '.wav')
                    path = self.audio_path + name + '.wav'
                    logging.info(f'[ACTION] Moved audiofile "{path}" into the path.')
                    return path

        def __save_audio_file(self, name: str, audio_file: io.BytesIO) -> None:
            # write audio into a new file in the audio folder
            with open(self.audio_path + f'{name}.wav', 'wb') as file:
                file.write(audio_file.getbuffer())
            logging.info(f'[ACTION] Created audiofile "{self.audio_path + name}.wav".')

    class _TimerInterface:

        def __init__(self, db: Connection, user_interface) -> None:
            self.db: Connection = db
            self.user_interface = user_interface
            logging.info('[INFO] TimerInterface initialized.')

        def get_all_timer(self, output_type: OutputTypes) -> list[timer_item] | list[tuple]:
            cursor: Cursor = self.db.cursor()
            statement: str = f'SELECT * FROM timer'
            cursor.execute(statement)
            result_set: list = cursor.fetchall()
            cursor.close()

            if output_type == OutputTypes.DICT:
                result_list: list[dict] = []
                for timer in result_set:
                    result_list.append(self.__build_json(timer))
                return result_list
            elif output_type == OutputTypes.TUPLE:
                for timer in result_set:
                    timer[2] = self.__build_datetime_object(timer[2])
                return result_set

        def get_timer_of_user(self, user: str | int) -> list[dict]:
            cursor: Cursor = self.db.cursor()
            result_list: list[dict] = []
            if type(user) is str:
                user = self.user_interface.__get_user_id(user)
            statement: str = 'SELECT * FROM timer WHERE uid=?'
            cursor.execute(statement, (user,))
            for timer in cursor.fetchall():
                result_list.append(self.__build_json(timer))
            cursor.close()
            return result_list

        def get_timer(self, timer_id: int) -> timer_item:
            cursor: Cursor = self.db.cursor()
            statement: str = f'SELECT * FROM timer WHERE id=? LIMIT 1'
            cursor.execute(statement, (timer_id,))
            result_set: tuple[int, str, str, str, int] = cursor.fetchone()
            cursor.close()
            return self.__build_json(result_set)

        def add_timer(self, time: datetime, duration: str, text: str, user_id: int) -> int:
            if len(text) > 255:
                raise ValueError('Given text is too long!')
            if len(duration) > 50:
                duration = self.__shorten_duration_string(duration)
            cursor: Cursor = self.db.cursor()
            statement: str = f'INSERT INTO timer (duration, time, text, uid) ' \
                             f'VALUES(?, ?, ?, ?)'
            cursor.execute(statement, (duration, {self.__build_time_string(time)}, text, user_id))
            result_set: int = cursor.rowcount
            statement = 'SELECT id FROM timer LIMIT 1'
            cursor.execute(statement)
            cursor.close()
            self.db.commit()
            # id from inserted timer - id from the first timer in the current database +1
            return result_set - cursor.rowcount + 1

        def update_timer(self, timer_id: int, _duration: str = None, _time: datetime = None, _text: str = None,
                         _user: int | str = None) -> None:
            cursor: Cursor = self.db.cursor()

            statement: str = 'SELECT * FROM timer WHERE id=?'
            cursor.execute(statement, (timer_id,))
            result_set: tuple = cursor.fetchone()
            if cursor.rowcount < 1:
                cursor.close()
                raise NoMatchingEntry(f'No matching element with the timer-id {timer_id} was found in the database.')

            tid, duration, time, text, uid = result_set

            if _duration is not None:
                if len(_duration) > 50:
                    duration = self.__shorten_duration_string(_duration)
                else:
                    duration = _duration
            if _time is not None:
                time = self.__build_time_string(_time)
            if _text is not None:
                if len(_text) > 255:
                    cursor.close()
                    raise ValueError('Given text is too long!')
                text = _text
            if _user is not None:
                if type(_user) is str:
                    statement: str = 'SELECT uid FROM user WHERE name=?'
                    cursor.execute(statement, (_user,))
                    uid: int = cursor.fetchone()
                    if cursor.rowcount < 1:
                        cursor.close()
                        raise NoMatchingEntry(f'No user with name {_user} found!')
                else:
                    # SELECT is needed to ensure consistency of the data. Do not enter a uid that does not exist!
                    statement: str = 'SELECT uid FROM user WHERE uid=?'
                    cursor.execute(statement, (_user,))
                    uid = cursor.fetchone()
                    if cursor.rowcount < 1:
                        cursor.close()
                        raise NoMatchingEntry(f'No user with id {_user} found!')

            statement: str = """UPDATE timer 
                                SET duration=?, time=?, text=?, uid=? 
                                WHERE id=?"""
            cursor.execute(statement, (duration, time, text, uid, tid))
            cursor.close()
            self.db.commit()

        def delete_timer(self, timer_id: int) -> None:
            curser: Cursor = self.db.cursor()
            statement: str = 'DELETE FROM timer WHERE id=?'
            curser.execute(statement, (timer_id,))
            curser.close()

        def delete_passed_timer(self) -> None:
            curser: Cursor = self.db.cursor()
            statement: str = 'DELETE FROM timer WHERE time < ?'
            curser.execute(statement, (self.__build_time_string(datetime.now()),))
            curser.close()

        @staticmethod
        def __shorten_duration_string(duration: str) -> str:
            # try to short the duration string, else store with unknown duration
            duration_arr: list[str] = duration.split(' ')
            if len(duration_arr[0]) + len(duration_arr[1]) > 40:
                return 'Unbekannte Länge'
            else:
                return 'mehr als ' + duration_arr[0] + duration_arr[1]

        def __build_json(self, timer: tuple[int, str, str, str, int]) -> dict:
            return {
                "id": timer[0],
                "duration": timer[1],
                "time": self.__build_datetime_object(timer[2]),
                "text": timer[3],
                "uid": timer[4]
            }

        @staticmethod
        def __build_datetime_object(time_string: str) -> datetime:
            return datetime(int(time_string[0:4]), int(time_string[4:6]), int(time_string[6:8]),
                            int(time_string[8:10]), int(time_string[10:12]), int(time_string[12:]), 0)

        @staticmethod
        def __build_time_string(time: datetime) -> str:
            return str(time.date()).replace('-', '') + str(time.time())[0:8].replace(':', '')

        def __create_table(self):
            pass

    class _ReminderInterface:

        def __init__(self, db: Connection, user_interface) -> None:
            self.db: Connection = db
            self.user_interface = user_interface  # connection is necessary for __get_user_id()
            logging.info('[INFO] ReminderInterface initialized.')

        def get_reminder(self, passed: bool = False):
            cursor: Cursor = self.db.cursor()

            if passed:
                now: datetime = datetime.now()
                date_string: str = now.strftime('%Y.%d.%m:%H:%M:%S')
                statement: str = 'SELECT * FROM reminder ' \
                                 'WHERE time<?'
                cursor.execute(statement, (date_string,))
            else:
                statement: str = 'SELECT * FROM reminder'
                cursor.execute(statement)
            result_set: list[tuple[int, str, str, int]] = cursor.fetchall()
            cursor.close()
            return self.__build_json(result_set)

        def add_reminder(self, text: str, time: str | None, user: int | str = None) -> int:
            if len(text) > 255:
                raise ValueError('Given text is too long!')

            if len(time) != 19:
                raise ValueError("Given time doesn't match!")

            if user is None:
                user = -1
            elif type(user) is str:
                user = self.user_interface.__get_user_id(user)

            if time is None:
                time = ''

            cursor: Cursor = self.db.cursor()

            statement: str = f'INSERT INTO reminder (time, text, uid) ' \
                             f'VALUES (?, ?, ?)'
            cursor.execute(statement, (time, text, user))
            rid: int = cursor.lastrowid
            cursor.close()
            self.db.commit()
            return rid

        def delete_reminder(self, _id: int = None, time: str = None) -> int:
            cursor: Cursor = self.db.cursor()
            if _id is not None:
                statement: str = 'DELETE FROM reminder WHERE id=?'
                cursor.execute(statement, (_id,))
            else:
                statement: str = 'DELTE FROM reminder WHERE time=?'
                cursor.execute(statement, (time,))
            counter: int = cursor.rowcount
            cursor.close()
            self.db.commit()
            return counter

        @staticmethod
        def __build_json(result_set: list[tuple[int, str, str, int]]) -> list[dict]:
            result_list: list[dict] = []

            for _id, time, text, uid in result_set:
                result_list.append({
                    'id': _id,
                    'time': time,
                    'text': text,
                    'uid': uid
                })

            return result_list

        def __create_table(self):
            pass

    class _ShoppingListInterface:

        def __init__(self, db: Connection) -> None:
            self.db: Connection = db
            logging.info('[INFO] ShoppingListInterface initialized.')

        def get_list(self) -> list[shopping_item]:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * FROM shoppinglist'
            cursor.execute(statement)
            result_set: list[tuple[int, str, str, float]] = cursor.fetchall()
            cursor.close()
            return self.__build_json(result_set)

        def get_item(self, name: str) -> dict:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * FROM shoppinglist WHERE name=?'
            cursor.execute(statement, (name,))
            result_set: tuple = cursor.fetchone()
            cursor.close()
            return self.__build_json(result_set)

        def add_item(self, name: str, measure: str, quantity: float) -> None:
            cursor: Cursor = self.db.cursor()
            statement: str = f'INSERT INTO shoppinglist ("name", "measure", "quantity") ' \
                             f'VALUES (?, ?, ?)'
            cursor.execute(statement, (name, measure, quantity))
            cursor.close()
            self.db.commit()

        def update_item(self, name: str, quantity: float) -> None:
            cursor: Cursor = self.db.cursor()
            # If there is no item with the name, the user should be told about it and not just not update anything
            statement: str = 'SELECT 1 FROM shoppinglist WHERE name=? LIMIT 1'
            cursor.execute(statement, (name,))

            anz_results: int = cursor.rowcount
            if anz_results == 0:
                cursor.close()
                raise NoMatchingEntry(f'No matching element with the name {name} was found in the database.')

            statement: str = """UPDATE shoppinglist 
                                SET quantity=? 
                                WHERE name=?"""
            cursor.execute(statement, (quantity, name))
            cursor.close()
            self.db.commit()

        def remove_item(self, name: str) -> None:
            cursor: Cursor = self.db.cursor()
            statement: str = 'DELETE FROM shoppinglist WHERE name=?'
            cursor.execute(statement, (name,))
            cursor.close()
            self.db.commit()

        def clear_list(self) -> None:
            cursor: Cursor = self.db.cursor()
            statement: str = 'DELETE FROM shoppinglist'
            cursor.execute(statement)
            cursor.close()
            self.db.commit()

        def is_item_in_list(self, name) -> bool:
            cursor: Cursor = self.db.cursor()
            statement: str = f'SELECT 1 FROM shoppinglist WHERE name=? LIMIT 1'
            cursor.execute(statement, (name,))
            cursor.close()
            if cursor.rowcount == 1:
                return True
            else:
                return False

        def __create_table(self):
            pass

        def __build_json(self, result_set: list[tuple[int, str, str, float]] | tuple[int, str, str, float]) \
                -> list[shopping_item] | shopping_item:
            result_list: list[shopping_item] = []
            if type(result_set) is list:
                for data_set in result_set:
                    result_list.append(self.__get_data_set(data_set))
                return result_list
            else:
                return self.__get_data_set(result_set)

        @staticmethod
        def __get_data_set(data_set: tuple[int, str, str, float]):
            sid, name, measure, quantity = data_set
            if quantity.is_integer():
                quantity = int(quantity)
            return {
                "id": sid,
                "name": name,
                "measure": measure,
                "quantity": quantity
            }

    class _RoutineInterface:
        def __init__(self, db: Connection) -> None:
            self.db: Connection = db
            logging.info('[INFO] RoutineInterface initialized.')

        def get_routine(self, name: str) -> routine_item:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * FROM routine WHERE name=? LIMIT 1'
            try:
                cursor.execute(statement, (name,))
            except OperationalError:
                raise NoMatchingEntry(f'Routine with name "{name}" not found!')
            if cursor.rowcount < 1:
                raise NoMatchingEntry(f'Routine with name "{name}" not found!')
            routine_set: tuple = cursor.fetchone()
            statement: str = 'SELECT * FROM routinecommands WHERE rname=?'
            cursor.execute(statement, (name,))
            command_set: list[tuple] = cursor.fetchall()
            text_set: list[tuple] = []
            statement: str = 'SELECT * FROM commandtext WHERE cid=?'
            for command in command_set:
                cursor.execute(statement, (command[0],))
                for item in cursor.fetchall():
                    text_set.append(item)
            statement: str = 'SELECT * FROM routinedates WHERE rname=?'
            cursor.execute(statement, (name,))
            date_set: list[tuple] = cursor.fetchall()
            statement = 'SELECT * FROM routineactivationtime WHERE rname=?'
            cursor.execute(statement, (name,))
            activation_set: list[tuple] = cursor.fetchall()
            statement = 'SELECT command FROM oncommand WHERE rname=?'
            cursor.execute(statement, (name,))
            on_command_set: list[tuple] = cursor.fetchall()
            cursor.close()
            return self.__build_json(routine_set, command_set, text_set, date_set, activation_set, on_command_set)

        def get_routines(self, on_command: str = None, on_time: dict = None) -> list[routine_item]:
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
                statement: str = 'SELECT * FROM routinecommands WHERE rname=?'
                cursor.execute(statement, (rout[0],))
                command_set: list[tuple] = cursor.fetchall()
                text_set: list[tuple] = []
                for command in command_set:
                    statement = 'SELECT * FROM commandtext WHERE cid=?'
                    cursor.execute(statement, (command[0],))
                    for item in cursor.fetchall():
                        text_set.append(item)

                statement = 'SELECT * FROM routinedates WHERE rname=?'
                cursor.execute(statement, (rout[0],))
                data_set: list[tuple] = cursor.fetchall()

                statement = 'SELECT * FROM routineactivationtime WHERE rname=?'
                cursor.execute(statement, (rout[0],))
                activation_set: list[tuple] = cursor.fetchall()

                statement = 'SELECT command FROM oncommand WHERE rname=?'
                cursor.execute(statement, (rout[0],))
                on_command_set: list[tuple] = cursor.fetchall()

                #print(f'rout: {rout}, command_set: {command_set}, text_set: {text_set}, date_set: {data_set}, activation_set: {activation_set}, on_command_set: {on_command_set}')
                routine_list.append(
                    self.__build_json(rout, command_set, text_set, data_set, activation_set, on_command_set))

            cursor.close()
            return routine_list

        def get_routine_command(self, rcid: int) -> dict:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * FROM routinecommand WHERE rcid=? LIMIT 1'
            cursor.execute(statement, (rcid,))
            rcid, rname, modulename = cursor.fetchone()
            statement = 'SELECT * FROM commandtext WHERE rcid=?'
            commands: list[tuple] = cursor.fetchall()
            cursor.execute(statement, (rcid,))
            cursor.close()
            return {
                'id': rcid,
                'rname': rname,
                'modulename': modulename,
                'text': [text for _, text in commands]
            }

        def get_routine_dates(self, rdid: int) -> dict:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * FROM routinedates WHERE rdid=? LIMIT 1'
            cursor.execute(statement, (rdid,))
            rdid, rname, day, month = cursor.fetchone()
            cursor.close()
            return {'id': rdid, 'rname': rname, 'day': day, 'month': month}

        def get_on_command(self, ocid: int) -> dict:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * FROM oncommand WHERE ocid=?'
            cursor.execute(statement, (ocid,))
            ocid, rname, command = cursor.fetchone()
            cursor.close()
            return {'id': ocid, 'rname': rname, 'command': command}

        def get_routine_activation_time(self, ratid: int) -> dict:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * FROM routineactivationtime WHERE ratid=?'
            cursor.execute(statement, (ratid,))
            ratid, rname, command = cursor.fetchone()
            cursor.close()
            return {'id': ratid, 'rname': rname, 'command': command}

        def add_routine(self, routine: dict) -> None:
            cursor: Cursor = self.db.cursor()
            statement: str = """INSERT INTO routine (name, description, daily, monday, tuesday, wednesday, thursday, 
                                friday, saturday, sunday, afteralarm, aftersunrise, aftersunset, aftercall) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """
            values: list = [routine.get("name"), routine.get("description")]
            for key in ['daily', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                values.append(str(int(routine['retakes']['days'][key] is True)))
            for key in ['after_alarm', 'after_sunrise', 'after_sunset', 'after_call']:
                values.append(str(int(routine["retakes"]["activation"][key] is True)))
            cursor.execute(statement, tuple(values))

            statement = 'SELECT last_insert_rowid()'
            cursor.execute(statement)

            self.__add_commands(routine['actions']['commands'], routine.get("name"))

            statement = 'INSERT INTO routinedates (rname, day, month) VALUES (?, ?, ?)'
            for item in routine['retakes']['days']['date_of_day']:
                cursor.execute(statement, (routine["name"], item.get("day"), item.get("month")))

            statement = 'INSERT INTO routineactivationtime (rname, hour, minute) VALUES (?, ?, ?)'
            for item in routine['retakes']['activation']['clock_time']:
                cursor.execute(statement, (routine["name"], item["hour"], item["minute"]))

            statement = 'INSERT INTO oncommand (rname, command) VALUES(?, ?)'
            for item in routine['on_commands']:
                cursor.execute(statement, (routine["name"], item))

            cursor.close()
            self.db.commit()

        def add_routine_by_values(self, name, description, daily, monday, tuesday, wednesday, thursday,
                                  friday, saturday, sunday, afteralarm, aftersunrise, aftersunset, aftercall):
            cursor: Cursor = self.db.cursor()
            statement: str = """INSERT INTO routine (name, description, daily, monday, tuesday, wednesday, thursday, 
                                            friday, saturday, sunday, afteralarm, aftersunrise, aftersunset, aftercall) 
                                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """
            cursor.execute(statement, (name, description, daily, monday, tuesday, wednesday, thursday,
                                       friday, saturday, sunday, afteralarm, aftersunrise, aftersunset, aftercall))
            cursor.close()
            self.db.commit()

        def create_routine_commands(self, rname: str, modulename: str, text: list[str]) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = 'INSERT INTO routinecommands (rname, modulename) VALUES (?, ?)'
            cursor.execute(statement, (rname, modulename))
            rcid: int = cursor.lastrowid

            if text is not None:
                statement = 'INSERT INTO commandtext VALUES (?, ?)'
                cursor.executemany(statement, text)

            cursor.close()
            self.db.commit()
            return rcid

        def create_on_command(self, rname: str, command: str) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = 'INSERT INTO oncommand (rname, command) VALUES (?, ?)'
            cursor.execute(statement, (rname, command))
            ocid: int = cursor.lastrowid
            cursor.close()
            self.db.commit()
            return ocid

        def create_routine_dates(self, rname: str, day: int, month: int):
            cursor: Cursor = self.db.cursor()
            statement: str = 'INSERT INTO routinedates (rname, day, month) VALUES (?, ?, ?)'
            cursor.execute(statement, (rname, day, month))
            rdid: int = cursor.lastrowid
            cursor.close()
            self.db.commit()
            return rdid

        def create_routine_activation_time(self, rname: str, hour: int, minute: int) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = 'INSERT INTO routineactivationtime (rname, hour, minute) VALUES (?, ?, ?)'
            cursor.execute(statement, (rname, hour, minute))
            ratid: int = cursor.lastrowid
            cursor.close()
            self.db.commit()
            return ratid

        def update_routine(self, old_name: str, new_routine_dict: dict = None, _name: str = None,
                           _description: str = None, _daily: bool = None, _monday: bool = None,
                           _tuesday: bool = None, _wednesday: bool = None, _thursday: bool = None, _friday: bool = None,
                           _saturday: bool = None, _sunday: bool = None, _after_alarm: bool = None,
                           _after_sunrise: bool = None, _after_sunset: bool = None, _after_call: bool = None,
                           _dates: list = None, _clock_time: list = None, _commands: list = None):
            cursor: Cursor = self.db.cursor()

            if new_routine_dict is not None:
                _name = new_routine_dict['name']
                _description = new_routine_dict['description']

                _retakes: dict = new_routine_dict['retakes']['days']
                _daily = _retakes['daily']
                _monday = _retakes['monday']
                _tuesday = _retakes['tuesday']
                _wednesday = _retakes['wednesday']
                _thursday = _retakes['thursday']
                _friday = _retakes['friday']
                _saturday = _retakes['saturday']
                _sunday = _retakes['sunday']

                _activation: dict = new_routine_dict['retakes']['activation']
                _after_alarm = _activation['after_alarm']
                _after_sunrise = _activation['after_sunrise']
                _after_sunset = _activation['after_sunset']
                _after_call = _activation['after_call']

                _dates = _retakes['date_of_day']
                _clock_time = _activation['clock_time']
                _commands = new_routine_dict['actions']['commands']

            statement: str = 'SELECT * FROM routine WHERE name=? LIMIT 1'
            cursor.execute(statement, (old_name,))
            result_set: tuple = cursor.fetchone()
            if cursor.rowcount < 1:
                cursor.close()
                raise NoMatchingEntry(f'No matching routine with the name {old_name} was found in the database.')

            name, description, daily, monday, tuesday, wednesday, thursday, friday, saturday, sunday, after_alarm, \
            after_sunrise, after_sunset, after_call = result_set

            if _name is not None:
                if len(_name) > 50:
                    cursor.close()
                    raise ValueError('Given name is too long!')
                name = _name
                # toDo: update names of other tables

            if _description is not None:
                if len(_description) > 255:
                    cursor.close()
                    raise ValueError('Given text is too long!')
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

            statement: str = f'UPDATE routine ' \
                             f'SET name=?, description=?, daily=?, monday=?, tuesday=?, wednesday=?, thursday=?, ' \
                             f'friday=?, saturday=?, sunday=?, afteralarm=?, aftersunrise=?, aftersunset=?, aftercall=? ' \
                             f'WHERE name=?'
            cursor.execute(statement, (name, description, daily, monday, tuesday, wednesday, thursday, friday, saturday,
                                       sunday, after_alarm, after_sunrise, after_sunset, after_call, old_name))

            if _dates is not None:
                statement: str = 'UPDATE routinedates SET day=?, month=? WHERE rdid=?'
                values: list[tuple] = [(item["day"], item["month"], item["id"]) for item in _dates]
                cursor.executemany(statement, values)

            if _clock_time is not None:
                statement: str = 'UPDATE routineactivationtime SET hour=?, minute=? WHERE ratid=?'
                values: list[tuple] = [(item["hour"], item["minute"], item["id"]) for item in _clock_time]
                cursor.executemany(statement, values)

            if _commands is not None:
                statement: str = 'UPDATE routinecommands SET modulename=? WHERE rcid=?'
                values: list[tuple] = [(item["module_name"], (item["id"])) for item in _commands]
                cursor.executemany(statement, values)

                statement: str = 'UPDATE commandtext SET text=? WHERE rcid=?'
                values: list[tuple] = [(item["text"], item["id"]) for item in _commands]
                cursor.executemany(statement, values)
            cursor.close()
            self.db.commit()

        def update_date_of_day(self, rdid: int, day: int, month: int):
            cursor: Cursor = self.db.cursor()
            statement: str = 'UPDATE routinedates SET day=?, month=? WHERE rdid=?'
            cursor.execute(statement, (day, month, rdid))
            cursor.close()
            self.db.commit()

        def update_activation_time(self, ratid: int, hour: int, minute: int):
            cursor: Cursor = self.db.cursor()
            statement: str = 'UPDATE routineactivationtime SET hour=?, minute=? WHERE ratid=?'
            cursor.execute(statement, (hour, minute, ratid))
            cursor.close()
            self.db.commit()

        def update_routine_commands(self, rcid: int, modulename: str, text: list[str]):
            cursor: Cursor = self.db.cursor()
            statement: str = 'UPDATE routinecommands SET modulename=? WHERE rcid=?'
            cursor.execute(statement, (modulename, rcid))
            cursor.close()
            self.db.commit()

        def update_command_text(self, rcid: int, module_name: str, text: list[str]):
            cursor: Cursor = self.db.cursor()
            statement: str = 'DELETE FROM commandtext WHERE rcid=?'
            cursor.execute(statement, (rcid,))
            statement = 'INSERT INTO commandtext VALUES (?, ?)'
            values: list[tuple] = [(rcid, item) for item in text]
            cursor.executemany(statement, values)
            cursor.close()
            self.db.commit()

        def update_on_command(self, ocid: int, command: str) -> None:
            cursor: Cursor = self.db.cursor()
            statement: str = 'UPDATE FROM oncommand SET command=? WHERE ocid=?'
            cursor.execute(statement, (command, ocid))
            cursor.close()
            self.db.commit()

        def update_on_commands(self, rname: str, commands: list[str]):
            cursor: Cursor = self.db.cursor()
            try:
                statement: str = 'DELETE FROM oncommand WHERE rname=?'
                cursor.execute(statement, (rname,))
                statement = 'INSERT INTO oncommand (rname, command) VALUES (?, ?)'
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
                attribute.replace('_', '')
                if attribute == 'name':
                    self.update_routine(routine_name, _name=value)
                if attribute in ['description', 'daily', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                                 'saturday', 'sunday', 'afteralarm', 'aftersunrise', 'aftersunset', 'aftercall']:
                    statement: str = 'UPDATE routine SET ' + '?=?'
                    cursor.execute(statement, (attribute, value))
                elif attribute == 'commands':
                    self.update_routine(routine_name, _commands=value)
            cursor.close()
            self.db.commit()

        def delete_routine(self, routine_name: str) -> int:
            cursor: Cursor = self.db.cursor()
            cursor.execute('DELETE FROM routineactivationtime WHERE rname=?', (routine_name,))
            cursor.execute('DELETE FROM routinedates WHERE rname=?', (routine_name,))
            cursor.execute('DELETE FROM commandtext WHERE rname=?', (routine_name,))
            cursor.execute('DELETE FROM routinecommands WHERE rname=?', (routine_name,))
            cursor.execute('DELETE FROM routine WHERE rname=?', (routine_name,))
            counter: int = cursor.rowcount
            cursor.close()
            self.db.commit()
            return counter

        def delete_routine_command(self, rcid: int):
            cursor: Cursor = self.db.cursor()
            statement: str = 'DELETE FROM commandtext WHERE rcid=?'
            cursor.execute(statement, (rcid,))
            statement: str = 'DELETE FROM routinecommands WHERE rcid=?'
            cursor.execute(statement, (rcid,))
            cursor.close()
            self.db.commit()

        def delete_on_command(self, ocid: int):
            cursor: Cursor = self.db.cursor()
            statement: str = 'DELETE FROM oncommand WHERE ocid=?'
            cursor.execute(statement, (ocid,))
            cursor.close()
            self.db.commit()

        def delete_routine_dates(self, rdid: int):
            cursor: Cursor = self.db.cursor()
            statement: str = 'DELETE FROM routinedates WHERE rdid=?'
            cursor.execute(statement, (rdid,))
            cursor.close()
            self.db.commit()

        def delete_routine_activation_time(self, ratid: int):
            cursor: Cursor = self.db.cursor()
            statement: str = 'DELETE FROM routineactivationtime WHERE ratid=?'
            cursor.execute(statement, (ratid,))
            cursor.close()
            self.db.commit()

        def __add_commands(self, commands: list[dict], name: str):
            cursor: Cursor = self.db.cursor()
            statement: str = 'INSERT INTO routinecommands (rname, modulename) VALUES (?, ?)'
            for module in commands:
                cursor.execute(statement, (name, module.get("module_name")))
                cursor.execute('SELECT last_insert_rowid()')
                module_id, = cursor.fetchone()

                for text in module.get('text'):
                    cursor.execute(f'INSERT INTO commandtext (cid, text) VALUES (?, ?)', (module_id, text))
            cursor.close()

        @staticmethod
        def __build_json(routine: tuple, commands: list[tuple], commandtext: list[tuple], dates: list[tuple],
                         activation: list[tuple], on_commands: list[tuple]) -> routine_item:
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
            name, description, daily, monday, tuesday, wednesday, thursday, friday, saturday, sunday, afteralarm, \
            aftersunrise, aftersunset, aftercall = routine
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
                        "date_of_day": []
                    },
                    "activation": {
                        "clock_time": [],
                        "after_alarm": (afteralarm == 1),
                        "after_sunrise": (aftersunrise == 1),
                        "after_sunset": (aftersunset == 1),
                        "after_call": (aftercall == 1)
                    }
                },
                "actions": {
                    "commands": []
                }
            }

            for rdid, rid, day, month in dates:
                result_dict["retakes"]["days"]["date_of_day"].append({
                    "id": rdid,
                    "day": day,
                    "month": month
                })

            for ratid, rid, _hour, _min in activation:
                result_dict["retakes"]["activation"]["clock_time"].append({
                    "id": ratid,
                    "hour": _hour,
                    "min": _min
                })

            for _id, rid, module_name in commands:
                text_list: list = []

                for cid, text in commandtext:
                    if cid == _id:
                        text_list.append(text)

                result_dict["actions"]["commands"].append({
                    "id": _id,
                    "module_name": module_name,
                    "text": text_list
                })

            for command, in on_commands:
                result_dict["on_commands"].append(command)

            return result_dict

        def __create_table(self):
            pass

    class _QuizInterface:
        def __init__(self, db: Connection) -> None:
            self.db: Connection = db
            logging.info('[INFO] QuizInterface initialized.')

        def add_question(self, theme: str, question: str, audio: str | io.BytesIO, answer: str):
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
            if msg['content_type'] == 'text':
                pass

    class _BirthdayInterface:
        def __init__(self, db: Connection) -> None:
            self.db: Connection = db

        def add_birthday(self, first_name: str, last_name: str, day: int, month: int, year: int) -> None:
            cursor: Cursor = self.db.cursor()
            cursor.execute('INSERT INTO birthdays VALUES (?, ?, ?, ?, ?)', (first_name, last_name, day, month, year))
            cursor.close()
            self.db.commit()

        def get_birthday(self, first_name: str, last_name: str) -> dict:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * FROM birthdays WHERE firstname=? AND lastname=?'
            cursor.execute(statement, (first_name, last_name))
            result_set: tuple = cursor.fetchone()
            cursor.close()
            return self.__build_json(result_set)

        def get_all_birthdays(self) -> list[dict]:
            cursor: Cursor = self.db.cursor()
            result_list: list[dict] = []

            cursor.execute(f'SELECT * FROM birthdays')
            result_set: list[tuple] = cursor.fetchall()
            cursor.close()
            for item in result_set:
                result_list.append(self.__build_json(item))

            return result_list

        def update_birthday(self, _old_first_name: str, _old_last_name: str, _new_first_name: str = None,
                            _new_last_name: str = None, _day: int = None, _month: int = None,
                            _year: int = None) -> None:

            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * FROM birthdays WHERE firstname=? AND lastname=?'
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
            cursor.execute(statement, (first_name, last_name, day, month, year, _old_first_name, _old_last_name))
            cursor.close()
            self.db.commit()

        def delete_birthday(self, first_name: str, last_name: str) -> None:
            cursor: Cursor = self.db.cursor()
            cursor.execute('DELETE FROM birthdays WHERE firstname=? AND lastname=?', (first_name, last_name))
            cursor.close()
            self.db.commit()

        @staticmethod
        def __build_json(result_set: tuple) -> dict:
            return {
                'first_name': result_set[0],
                'last_name': result_set[1],
                'day': result_set[2],
                'month': result_set[3],
                'year': result_set[4]
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
    db = DataBase('C:\\Users\\Jakob\\PycharmProjects\\Jarvis\\src\\speechassistant\\', None)
    print(db.routine_interface.get_routines())
    # db.alarm_interface.add_alarm({"hour": 10, "minute": 0, "total_seconds":5234324}, "Hallo Welt", -1, {"monday": True, "tuesday": True, "wednesday": True, "thursday": True, "friday": True, "saturday": False, "sunday": False, "regular": True})
    # print(db.alarm_interface.get_alarms())