from __future__ import annotations  # compatibility for < 3.10

import io
import pathlib
from datetime import datetime
from typing import Callable  # , TypeAlias
import os
import sqlite3
from sqlite3 import Connection, Cursor

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

# toDo: except IndexError -> if ... is None
# toDo: as_tuple -> output_type: OutputTypes
# toDo: fetch_one -> LIMIT 1

class DataBase:
    def __init__(self, root_path: str, skills: Skills) -> None:
        logging.basicConfig(level=logging.DEBUG)
        logging.info('[ACTION] Initialize DataBase...\n')
        self.db: Connection = sqlite3.connect(os.path.join(root_path, 'database\\data_base'), check_same_thread=False)
        self.error_counter: int = 0

        self.user_interface = self._UserInterface(self.db, self.__execute)
        self.alarm_interface = self._AlarmInterface(self.db, self.__execute, skills)
        self.timer_interface = self._TimerInterface(self.db, self.__execute, self.user_interface)
        self.reminder_interface = self._ReminderInterface(self.db, self.__execute, self.user_interface)
        self.quiz_interface = self._QuizInterface(self.db)
        self.shoppinglist_interface = self._ShoppingListInterface(self.db, self.__execute)
        self.routine_interface = self._RoutineInterface(self.db, self.__execute)
        self.audio_interface = self._AudioInterface(self.db, self.__execute)
        self.messenger_interface = self._MessangerInterface(self.__execute)
        self.birthday_interface = self._BirthdayInterface(self.__execute)
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
                            'regular INTEGER)')

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
                            'time VARCHAR(14),'
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

        self.__create_table('CREATE TABLE IF NOT EXISTS oncommand ('
                            'rname VARCHAR(50), '
                            'command VARCHAR(255), '
                            'FOREIGN KEY(rname) REFERENCES routine(rname)'
                            'PRIMARY KEY(rname, command))')

        self.__create_table('CREATE TABLE IF NOT EXISTS routineactivationtime ('
                            'rname VARCHAR(50), '
                            'hour INTEGER, '
                            'minute INTEGER, '
                            'FOREIGN KEY(rname) REFERENCES routine(rname), '
                            'PRIMARY KEY(rname, hour, minute))')

        self.__create_table('CREATE TABLE IF NOT EXISTS routinedates ('
                            'rname VARCHAR(50),'
                            'day INTEGER,'
                            'month INTEGER,'
                            'PRIMARY KEY(rname, day, month),'
                            'FOREIGN KEY(rname) REFERENCES routine(rname))')

        self.__create_table('CREATE TABLE IF NOT EXISTS routinecommands ('
                            'cid INTEGER PRIMARY KEY, '
                            'rname VARCHAR(50), '
                            'modulename VARCHAR(50), '
                            'FOREIGN KEY(rname) REFERENCES routine(rname))')

        self.__create_table('CREATE TABLE IF NOT EXISTS commandtext ('
                            'cid INTEGER,'
                            'text VARCHAR(255) NOT NULL,'
                            'PRIMARY KEY(cid, text),'
                            'FOREIGN KEY(cid) REFERENCES routinecommands(cid), '
                            'UNIQUE(cid, text))')

        self.__create_table('CREATE TABLE IF NOT EXISTS quiz ('
                            'category VARCHAR(50) PRIMARY KEY)')

        self.__create_table('CREATE TABLE IF NOT EXISTS questions ('
                            'category REFERENCES quiz(category) PRIMARY KEY,'
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

        # self.__create_table('CREATE TABLE IF NOT EXISTS messengernotifications')
        self.__create_table('CREATE TABLE IF NOT EXISTS birthdays ('
                            'firstname VARCHAR(15),'
                            'lastname VARCHAR(30),'
                            'day INTEGER,'
                            'month INTEGER,'
                            'year INTEGER,'
                            'PRIMARY KEY(firstname, lastname),'
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
        finally:
            cursor.close()

    def __remove_tables(self):
        pass

    def stop(self):
        logging.info('[ACTION] Stopping database...')
        self.db.commit()
        self.db.close()

    class _UserInterface:
        def __init__(self, db: Connection, execute: Callable[[str, tuple | None], list]) -> None:
            self.db: Connection = db
            self.exec_func: Callable = execute
            logging.info('[INFO] UserInterface initialized.')

        def get_user(self, user: str | int) -> user_item:
            cursor: Cursor = self.db.cursor()
            if type(user) is str:
                user: int = self.__get_user_id(user)

            statement: str = f'SELECT * from user WHERE uid=?'

            cursor.execute(statement, (user,))

            result_set: list[tuple[int, str, str, str, str, int, int]] = cursor.fetchone()
            cursor.close()
            return self.__build_json(result_set)

        def get_user_by_messenger_id(self, messenger_id: int) -> user_item:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * FROM user WHERE mid=?'
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
                     song_id: int = 1) -> None:
            cursor: Cursor = self.db.cursor()
            statement: str = f'INSERT INTO user (alias, firstname, lastname, birthday, mid, sname) ' \
                             f'VALUES (?, ?, ?, ?, ?, ?)'
            cursor.execute(statement, (alias, firstname, lastname, self.__birthday_to_string(birthday),
                                       messenger_id, song_id))
            cursor.close()

        def add_user_notification(self, user: int | str, notification: str):
            cursor: Cursor = self.db.cursor()

            if type(user) is str:
                user: int = self.__get_user_id(user)

            statement: str = f'INSERT INTO notification (uid, text) VALUES (?, ?)'
            cursor.execute(statement, (user, notification))
            cursor.close()

        # The first line of attributes is for mapping purposes only, so that the user can be specified more easily
        def update_user(self, uid: int = None, alias: str = None, first_name: str = None, last_name: str = None,
                        _new_alias: str = None, _new_first_name: str = None, _new_last_name: str = None,
                        _birthday: dict = None, _messenger_id: int = 0, _song_name: str = 'standard'):

            cursor: Cursor = self.db.cursor()

            if uid is not None:
                statement: str = 'SELECT * FROM user WHERE uid=?'
                try:
                    cursor.execute(statement, (uid,))
                    result_set: tuple = cursor.fetchone()
                except IndexError:
                    raise NoMatchingEntry(f'No matching user with the user-id {uid} was found in the database.')

            elif alias is not None:
                statement: str = 'SELECT * FROM user WHERE alias=?'
                try:
                    cursor.execute(statement, (alias,))
                    result_set: tuple = cursor.fetchone()
                except IndexError:
                    raise NoMatchingEntry(f'No matching user with the alias "{alias}" was found in the database.')

            elif first_name is not None and last_name is not None:
                statement: str = """SELECT * FROM user
                                    WHERE firstname=?
                                    AND lastname=?"""
                try:
                    cursor.execute(statement, (first_name, last_name))
                    result_set: tuple = cursor.fetchone()
                except IndexError:
                    raise NoMatchingEntry(f'No matching user with the name "{last_name, first_name}" was found '
                                          f'in the database.')
            else:
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
            cursor.execute(statement, (alias, firstname, lastname, self.__birthday_to_string(birthday), mid, sname, uid))
            cursor.close()

        def delete_user_notification(self, user: int | str, text: str) -> None:
            cursor: Cursor = self.db.cursor()

            if type(user) is str:
                user: int = self.__get_user_id(user)

            statement: str = 'DELETE FROM notification WHERE uid=? AND text=?'
            cursor.execute(statement, (user, text))
            cursor.close()

        def delete_user(self, user: int | str) -> None:
            cursor: Cursor = self.db.cursor()

            if type(user) is str:
                user: int = self.__get_user_id(user)

            statement: str = 'DELETE FROM user WHERE uid=?'

            cursor.execute(statement, (user,))
            cursor.close()

        @staticmethod
        def __birthday_to_string(birthday: dict) -> str:
            return str(birthday.get('year')) + str(birthday.get('month')).rjust(2, '0') + str(
                birthday.get('day')).rjust(2, '0')

        def __get_user_id(self, alias: str) -> int:
            user_result_set: list[tuple[str]] = self.exec_func(f'SELECT uid FROM user WHERE alias=?', (alias,))
            if len(user_result_set) == 1:
                return int(user_result_set[0][0])
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
        def __init__(self, db: Connection, execute: Callable[[str, tuple | None], list], skills: Skills) -> None:
            self.db: Connection = db
            self.exec_func = execute
            self.skills = skills
            logging.info('[INFO] AlarmInterface initialized.')

        def get_alarm(self, aid: int, as_tuple: bool = False) -> tuple | dict:
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * FROM alarm as a JOIN alarmrepeat as ar ON a.aid=ar.aid WHERE aid=?'
            cursor.execute(statement, (aid,))
            result_set: tuple = cursor.fetchone()
            cursor.close()
            return self.__build_json(result_set, as_tuple)

        def get_alarms(self, active: bool = False, unsorted: bool = False, as_tuple: bool = False) -> \
                tuple[list[dict],list[dict]] | dict:
            cursor: Cursor = self.db.cursor()
            init_result_set: list = []
            if unsorted:
                if active:
                    statement: str = 'SELECT * FROM alarm as a ' \
                                     'JOIN alarmrepeat as ar ON a.aid=ar.aid'
                else:
                    statement: str = 'SELECT * FROM alarm as a ' \
                                     'JOIN alarmrepeat as ar ON a.aid=ar.aid ' \
                                     'WHERE a.active=true'
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
                      initiated: bool = False, song: str = 'standard.wav') -> None:
            cursor: Cursor = self.db.cursor()
            if type(user) is str:
                user = self.__get_user_id(user)

            statement: str = f'INSERT INTO alarm (sname, uid, hour, minute, total_seconds, text, active, initiated, last_executed) ' \
                             f'VALUES (?, ?, ?, ?, ?, ?, ?, ?, "")'

            cursor.execute(statement, (song, user, time["hour"], time["minute"], time["total_seconds"], text,
                                       int(active), int(initiated)))
            alarm_id: int = cursor.lastrowid()

            statement: str = f'INSERT INTO alarmrepeat VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
            values: list = [alarm_id]
            for item in repeating.keys():
                values.append(str(int(repeating.get(item))))
            cursor.execute(statement, tuple(values))
            cursor.close()

        def delete_alarm(self, aid: int) -> int:
            cursor: Cursor = self.db.cursor()
            statement: str = 'DELETE FROM alarm WHERE aid=?'
            cursor.execute(statement, (aid,))
            anz_removed_alarm: int = cursor.rowcount
            statement = 'DELETE FROM alarmrepeat WHERE aid=?'
            cursor.execute(statement, (aid,))
            anz_removed_repeat: int = cursor.rowcount

            if anz_removed_alarm != anz_removed_repeat and anz_removed_alarm < 1:
                # toDo: maybe use another SQLException
                raise UnsolvableException('Removed more alarm repeating´s than alarms!')
            cursor.close()
            return anz_removed_alarm

        def update_alarm(self, aid: int, _time: dict = None, _text: str = None, _user: int | str = None,
                         _active: bool = None, _initiated: bool = None, _regular: bool = None, _sound: str = None,
                         _last_executed: str = None) -> None:
            cursor: Cursor = self.db.cursor()
            # If there is no item with the name, the user should be told about it and not just not update anything
            statement: str = 'SELECT * FROM alarm WHERE aid=?'
            cursor.execute(statement, (aid,))
            result_set: tuple = cursor.fetchone()
            if result_set is None:
                raise NoMatchingEntry(f'No matching element with the alarm-id {aid} was found in the database.')

            aid, sname, uid, hour, minute, total_seconds, text, active, initiated, last_executed = result_set

            if _time is not None:
                hour = _time["hour"]
                minute = _time["minute"]
            if _text is not None:
                text = _text
            if _user is not None:
                if type(_user) is str:
                    try:
                        statement: str = 'SELECT uid FROM user WHERE name=?'
                        cursor.execute(statement, (_user,))
                        uid: int = cursor.fetchone()[0]
                    except IndexError:
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
                    raise ValueError('Given last_executed was too long! Max length for last_executed is 10 chars.')
                last_executed = _last_executed

            statement: str = f'UPDATE alarm SET sname=?, uid=?, hour=?, minute=?, total_seconds=?, text=?, active=?, ' \
                             f'initiaded=?, last_executed=? WHERE aid=?'
            cursor.execute(statement, (sname, uid, hour, minute, total_seconds, text, active, initiated, last_executed,
                                       aid))
            cursor.close()

        def update_repeating(self, aid: int, _monday: bool = None, _tuesday: bool = None, _wednesday: bool = None,
                             _thursday: bool = None, _friday: bool = None, _saturday: bool = None,
                             _sunday: bool = None):
            cursor: Cursor = self.db.cursor()
            try:
                statement: str = 'SELECT * FROM alarmrepeat WHERE aid=?'
                cursor.execute(statement, (aid,))
                result_set: tuple = cursor.fetchone()[0]
            except:
                raise NoMatchingEntry(f'No matching element with the id {aid} was found in the database.')

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

        def __build_json(self, result_set: list[tuple], as_tuple: bool = False) -> list[dict] | list[tuple]:
            # toDo: add alarmrepeat

            if as_tuple:
                result_list: list[tuple] = []
                for aid, sname, uid, hour, minute, total_seconds, text, active, initiated, last_executed in result_set:
                    time = {"hour": hour, "minute": minute, "total_seconds": total_seconds}
                    result_list.append((aid, time, sname, uid, text, active, initiated, last_executed))
                return result_list

            result_list: list[dict] = []
            print(result_set)
            for aid, sname, uid, hour, minute, total_seconds, text, active, initiated, last_executed, _, monda, tuesday, wednesday, thursday, friday, saturday, sunday, regular in result_set:
                sound_path: str = self.exec_func(f'SELECT path FROM audio WHERE name=?', (sname,))[0]
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
                    "active": active,
                    "initiated": initiated,
                    "last_executed": last_executed
                })
            return result_list

        def __get_user_id(self, alias: str) -> int:
            user_result_set: list[tuple[str]] = self.exec_func(f'SELECT uid FROM user WHERE alias=?', (alias,))
            if len(user_result_set) == 1:
                return int(user_result_set[0][0])
            else:
                raise UserNotFountException()

        def __create_table(self):
            pass

    class _AudioInterface:

        def __init__(self, db: Connection, execute: Callable[[str, tuple | None], list]) -> None:
            self.db: Connection = db
            self.exec_func = execute
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
                    raise FileNameAlreadyExists()
            if name is not None:
                statement: str = 'SELECT name FROM audio WHERE name=?'
                cursor.execute(statement, (audio_file,))
                if cursor.rowcount > 0:
                    raise FileNameAlreadyExists()

            if not file_stored:
                if path is not None and not audio_file is None:
                    raise ValueError('Got too many arguments! Decide between the path and the audio file.')
                elif path is None and audio_file is None:
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

        def update_audio(self, _audio_name: str, _new_audio_name: str = None, _path: str = None,
                         _audio_file: io.BytesIO = None) -> str:
            cursor: Cursor = self.db.cursor()
            try:
                statement: str = 'SELECT * FROM audio WHERE name=?'
                cursor.execute(statement, (_audio_name,))
                result_set: tuple = cursor.fetchone()[0]
            except IndexError:
                raise NoMatchingEntry(f'No matching element with the audio name "{_audio_name}" was found '
                                      f'in the database.')

            name, path = result_set

            if _new_audio_name is not None:
                name = _new_audio_name
                os.rename(os.path.join(self.audio_path, _audio_name), os.path.join(self.audio_path, name))
            if _path is not None and _audio_file is not None:
                raise ValueError('Got too many arguments! Decide between the path and the audio file.')
            elif _path is not None:
                # old_path is needed after the SQL query
                old_path: str = _path
                path = self.__justify_file_path(_audio_name, _path)
            elif _audio_file is not None:
                statement: str = 'SELECT path FROM audio WHERE name=?'
                cursor.execute(statement, (_audio_name,))
                file_path: str = cursor.fetchone()[0]
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
            file_path: str = cursor.fetchone()[0]
            statement = 'DELETE FROM audio WHERE name=?'
            cursor.execute(statement, (audio_name,))
            anz_removed: int = cursor.rowcount
            cursor.close()
            if type(anz_removed) is list:
                raise UnsolvableException('DataBase returned wrong type while deleting an entry!')
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

        def __init__(self, db: Connection, execute: Callable[[str, tuple | None], list], user_interface) -> None:
            self.db: Connection = db
            self.exec_func = execute
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
            # id from inserted timer - id from the first timer in the current database +1
            return result_set - cursor.rowcount + 1

        def update_timer(self, timer_id: int, _duration: str = None, _time: datetime = None, _text: str = None,
                         _user: int | str = None) -> None:
            cursor: Cursor = self.db.cursor()

            statement: str = 'SELECT * FROM timer WHERE id=?'
            cursor.execute(statement, (timer_id,))
            result_set: tuple = cursor.fetchone()
            if cursor.rowcount < 1:
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
                    raise ValueError('Given text is too long!')
                text = _text
            if _user is not None:
                if type(_user) is str:
                    try:
                        statement: str = 'SELECT uid FROM user WHERE name=?'
                        cursor.execute(statement, (_user,))
                        uid: int = cursor.fetchone()[0]
                    except IndexError:
                        raise NoMatchingEntry(f'No user with name {_user} found!')
                else:
                    # SELECT is needed to ensure consistency of the data. Do not enter a uid that does not exist!
                    try:
                        statement: str = 'SELECT uid FROM user WHERE uid=?'
                        cursor.execute(statement, (_user,))
                        uid = cursor.fetchone()[0]
                    except IndexError:
                        raise NoMatchingEntry(f'No user with id {_user} found!')

            statement: str = """UPDATE timer 
                                SET duration=?, time=?, text=?, uid=? 
                                WHERE id=?"""
            cursor.execute(statement, (duration, time, text, uid, tid))
            cursor.close()

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

        def __init__(self, db: Connection, execute: Callable[[str, tuple | None], list], user_interface) -> None:
            self.db: Connection = db
            self.exec_func: Callable = execute
            self.user_interface = user_interface  # connection is necessary for __get_user_id()
            logging.info('[INFO] ReminderInterface initialized.')

        def get_reminder(self):
            cursor: Cursor = self.db.cursor()
            statement: str = 'SELECT * FROM reminder'
            cursor.execute(statement)
            result_set: list[tuple[int, str, str, int]] = cursor.fetchall()
            cursor.close()
            return self.__build_json(result_set)

        def add_reminder(self, text: str, time: str | None, user: int | str = None) -> None:
            if len(text) > 255:
                raise ValueError('Given text is too long!')

            if len(time) != 14:
                raise ValueError("Given time doesn't match!")

            if user is None:
                user = -1
            elif type(user) is str:
                user = self.user_interface.__get_user_id(user)

            if time is None:
                time = ''

            curser: Cursor = self.db.cursor()

            statement: str = f'INSERT INTO reminder (time, text, uid) ' \
                             f'VALUES (?, ?, ?)'
            curser.execute(statement, (time, text, user))
            curser.close()

        def delete_reminder(self, _id: int) -> None:
            cursor: Cursor = self.db.cursor()
            statement: str = 'DELETE FROM reminder WHERE id=?'
            cursor.execute(statement, (_id,))
            cursor.close()

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

        def __init__(self, db: Connection, execute: Callable[[str, tuple | None], list]) -> None:
            self.db: Connection = db
            self.exec_func: Callable = execute
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
            result_set: tuple = cursor.fetchone()[0]
            cursor.close()
            return self.__build_json(result_set)




































        def add_item(self, name: str, measure: str, quantity: float) -> None:
            statement: str = f'INSERT INTO shoppinglist ("name", "measure", "quantity") ' \
                             f'VALUES (?, ?, ?)'
            self.exec_func(statement, (name, measure, quantity))

        def update_item(self, name: str, quantity: float) -> None:
            # If there is no item with the name, the user should be told about it and not just not update anything
            anz_results: int = len(self.exec_func(f'SELECT * FROM shoppinglist WHERE name=?', (name,)))
            if anz_results == 0:
                raise NoMatchingEntry(f'No matching element with the name {name} was found in the database.')

            statement: str = f'UPDATE shoppinglist ' \
                             f'SET quantity=? ' \
                             f'WHERE name=?'
            self.exec_func(statement, (quantity, name))

        def remove_item(self, name: str) -> None:
            statement: str = f'DELETE FROM shoppinglist WHERE name=?'
            self.exec_func(statement, (name,))

        def clear_list(self) -> None:
            statement: str = f'DELETE FROM shoppinglist'
            self.exec_func(statement, ())

        def is_item_in_list(self, name) -> bool:
            statement: str = f'SELECT * FROM shoppinglist WHERE name=?'
            result_set = self.exec_func(statement, (name,))
            if result_set:
                return True
            else:
                return False

        def __create_table(self):
            pass

        def __build_json(self, result_set: list[tuple[int, str, str, float]] | tuple[int, str, str, float]) -> list[shopping_item] | shopping_item:
            result_list: list[shopping_item] = []
            if type(result_set) is list:
                for data_set in result_set:
                    result_list.append(self.__get_data_set(data_set))
                return result_list
            else:
                return self.__get_data_set(result_set)

        @staticmethod
        def __get_data_set(data_set: tuple[int, str, str, float]):
            name, measure, quantity = data_set
            if quantity.is_integer():
                quantity = int(quantity)
            return {
                "name": name,
                "measure": measure,
                "quantity": quantity
            }

    class _RoutineInterface:
        def __init__(self, db: Connection, execute: Callable[[str, tuple | None], list]) -> None:
            self.db: Connection = db
            self.exec_func: Callable = execute
            logging.info('[INFO] RoutineInterface initialized.')

        def get_routine(self, name: str) -> routine_item:
            routine_set: tuple = self.exec_func(f'SELECT * FROM routine WHERE name=?', (name,))[0]
            command_set: list[tuple] = self.exec_func(f'SELECT * FROM routinecommands WHERE rname=?', (name,))
            text_set: list[tuple] = []
            for command in command_set:
                for item in self.exec_func(f'SELECT * FROM commandtext WHERE cid=?', (command[0],)):
                    text_set.append(item)
            date_set: list[tuple] = self.exec_func(f'SELECT * FROM routinedates WHERE rname=?', (name,))
            activation_set: list[tuple] = self.exec_func(f'SELECT * FROM routineactivationtime WHERE rname=?', (name,))
            on_command_set: list[tuple] = self.exec_func(f'SELECT command FROM oncommand WHERE rname=?', (name,))
            return self.__build_json(routine_set, command_set, text_set, date_set, activation_set, on_command_set)

        def get_routines(self, on_command: str = None) -> list[routine_item]:
            routine_list: list[dict] = []
            if on_command is None:
                routine_set: list[tuple] = self.exec_func(f'SELECT * FROM routine', ())
            else:
                routine_set: list[tuple] = self.exec_func(f'SELECT * FROM  routine '
                                                          f'INNER JOIN oncommand ON routine.name=oncommand.rname '
                                                          f'WHERE instr(?, oncommand.command) > 0', (on_command,))

            for rout in routine_set:
                command_set: list[tuple] = self.exec_func(f'SELECT * FROM routinecommands WHERE rname=?', (rout[0],))
                text_set: list[tuple] = []
                for command in command_set:
                    for item in self.exec_func(f'SELECT * FROM commandtext WHERE cid=?', (command[0],)):
                        text_set.append(item)
                date_set: list[tuple] = self.exec_func(f'SELECT * FROM routinedates WHERE rname=?', (rout[0],))
                activation_set: list[tuple] = self.exec_func(
                    f'SELECT * FROM routineactivationtime WHERE rname=?', (rout[0],))

                on_command_set: list[tuple] = self.exec_func(f'SELECT command FROM oncommand WHERE rname=?', (rout[0],))

                routine_list.append(
                    self.__build_json(rout, command_set, text_set, date_set, activation_set, on_command_set))

            return routine_list

        def add_routine(self, routine: dict) -> None:
            statement: str = f'INSERT INTO routine (name, description, daily, monday, tuesday, wednesday, thursday, friday, ' \
                             f'saturday, sunday, afteralarm, aftersunrise, aftersunset, aftercall)' \
                             f'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            values: list = [routine.get("name"), routine.get("description")]
            for key in ['daily', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                values.append(str(int(routine['retakes']['days'][key] is True)))
            for key in ['after_alarm', 'after_sunrise', 'after_sunset', 'after_call']:
                values.append(str(int(routine["retakes"]["activation"][key] is True)))
            self.exec_func(statement, tuple(values))

            name: str = self.exec_func('SELECT last_insert_rowid()', ())[0][0]

            self.__add_commands(routine['actions']['commands'], name)

            for item in routine['retakes']['days']['date_of_day']:
                self.exec_func(
                    f'INSERT INTO routinedates (rname, day, month) VALUES (?, ?, ?)',
                    (name, item.get("day"), item.get("month")))

            for item in routine['retakes']['activation']['clock_time']:
                self.exec_func(f'INSERT INTO routineactivationtime VALUES (?, ?, ?)',
                               (name, item["hour"], item["minute"]))

            for item in routine['on_commands']:
                self.exec_func(f'INSERT INTO oncommand VALUES(?, ?)', (name, item))

        def update_routine(self, old_name: str, _name: str = None, _description: str = None, _daily: bool = None,
                           _monday: bool = None,
                           _tuesday: bool = None, _wednesday: bool = None, _thursday: bool = None, _friday: bool = None,
                           _saturday: bool = None, _sunday: bool = None, _after_alarm: bool = None,
                           _after_sunrise: bool = None, _after_sunset: bool = None, _after_call: bool = None,
                           _dates: list = None, _clock_time: list = None, _commands: list = None):
            try:
                result_set: tuple = self.exec_func(f'SELECT * FROM routine WHERE name=?', (old_name,))[0]
            except IndexError:
                raise NoMatchingEntry(f'No matching routine with the name {old_name} was found in the database.')

            name, description, daily, monday, tuesday, wednesday, thursday, friday, saturday, sunday, after_alarm, \
            after_sunrise, after_sunset, after_call = result_set

            if _name is not None:
                if len(_name) > 50:
                    raise ValueError('Given name is too long!')
                name = _name
                # toDo: update names of other tables

            if _description is not None:
                if len(_description) > 255:
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
            self.exec_func(statement, (name, description, daily, monday, tuesday, wednesday, thursday, friday, saturday,
                                       sunday, after_alarm, after_sunrise, after_sunset, after_call, old_name))

            if _dates is not None:
                # delete old entries
                self.exec_func(f'DELETE FROM routinedates WHERE rname=?', (name,))

                for item in _dates:
                    self.exec_func(
                        f'INSERT INTO routinedates VALUES (?, ?, ?)', (name, item.get("day"), item.get("month")))

            if _clock_time is not None:
                # delete old entries
                self.exec_func(f'DELETE FROM routineactivationtime WHERE rname=?', (name,))
                for item in _clock_time:
                    self.exec_func(f'INSERT INTO routineactivationtime '
                                   f'VALUES (?, ?, ?)', (name, item.get("hour"), item.get("minute")))

            if _commands is not None:
                # delete old entries
                result_set: list[tuple] = self.exec_func(f'SELECT cid FROM routinecommands WHERE rname=?', (name,))
                for item in result_set:
                    logging.info(item[0])
                    self.exec_func(f'DELETE FROM commandtext WHERE cid=?', (item[0],))
                    self.exec_func(f'DELETE FROM routinecommands WHERE cid=?', (item[0],))

                self.__add_commands(_commands, name)

        def delete_routine(self, routine_id: int) -> None:
            self.exec_func(f'DELETE FROM routineactivationtime WHERE rid=?', (routine_id,))
            self.exec_func(f'DELETE FROM routinedates WHERE rid=?', (routine_id,))
            self.exec_func(f'DELETE FROM commandtext WHERE rid=?', (routine_id,))
            self.exec_func(f'DELETE FROM routinecommands WHERE rid=?', (routine_id,))
            self.exec_func(f'DELETE FROM routine WHERE rid=?', (routine_id,))

        def __add_commands(self, commands: list[dict], name: str):
            for module in commands:
                self.exec_func(
                    f'INSERT INTO routinecommands (name, modulename) VALUES (?, ?)', (name, module.get("module_name")))
                module_id: int = self.exec_func('SELECT last_insert_rowid()', ())[0][0]

                for text in module.get('text'):
                    self.exec_func(f'INSERT INTO commandtext VALUES (?, ?)', (module_id, text))

        @staticmethod
        def __build_json(routine: tuple, commands: list[tuple], commandtext: list[tuple], dates: list[tuple],
                         activation: list[tuple], on_commands: list[tuple]) -> routine_item:
            result_dict = {
                "id": routine[0],
                "name": routine[1],
                "descriptions": routine[2],
                "on_commands": [],
                "retakes": {
                    "days": {
                        "daily": (routine[3] == 1),
                        "monday": (routine[4] == 1),
                        "tuesday": (routine[5] == 1),
                        "wednesday": (routine[6] == 1),
                        "thursday": (routine[7] == 1),
                        "friday": (routine[8] == 1),
                        "saturday": (routine[9] == 1),
                        "sunday": (routine[10] == 1),
                        "date_of_day": []
                    },
                    "activation": {
                        "clock_time": [],
                        "after_alarm": (routine[11] == 1),
                        "after_sunrise": (routine[12] == 1),
                        "after_sunset": (routine[13] == 1),
                        "after_call": (routine[14] == 1)
                    }
                },
                "actions": {
                    "commands": []
                }
            }

            for rid, day, month in dates:
                result_dict["retakes"]["days"]["date_of_day"].append({
                    "day": day,
                    "month": month
                })

            for rid, _hour, _min in activation:
                result_dict["retakes"]["activation"]["clock_time"].append({
                    "hour": _hour,
                    "min": _min
                })

            for _id, rid, module_name in commands:
                text_list: list = []

                for cid, text in commandtext:
                    if cid == _id:
                        text_list.append(text)

                result_dict["actions"]["commands"].append({
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
        def __init__(self, execute: Callable[[str, tuple | None], list]) -> None:
            self.exec_func: Callable = execute

        def add_rejected_message(self, msg):
            if msg['content_type'] == 'text':
                pass

    class _BirthdayInterface:
        def __init__(self, execute: Callable[[str, tuple | None], list]) -> None:
            self.exec_func: Callable = execute

        def add_birthday(self, first_name: str, last_name: str, day: int, month: int, year: int) -> None:
            self.exec_func(f'INSERT INTO birthdays '
                           f'VALUES (?, ?, ?, ?, ?)', (first_name, last_name, day, month, year))

        def get_birthday(self, first_name: str, last_name: str) -> dict:
            result_set: tuple = self.exec_func(f'SELECT * FROM birthdays '
                                               f'WHERE firstname=? '
                                               f'AND lastname=?', (first_name, last_name))[0]
            return self.__build_json(result_set)

        def get_all_birthdays(self) -> list[dict]:
            result_list: list[dict] = []
            result_set: list[tuple] = self.exec_func(f'SELECT * FROM birthdays', ())
            for item in result_set:
                result_list.append(self.__build_json(item))

            return result_list

        def update_birthday(self, _old_first_name: str, _old_last_name: str, _new_first_name: str = None,
                            _new_last_name: str = None, _day: int = None, _month: int = None,
                            _year: int = None) -> None:
            first_name, last_name, day, month, year = self.exec_func(f'SELECT * FROM birthdays '
                                                                     f'WHERE firstname=? AND lastname=?',
                                                                     (_old_first_name, _old_last_name))[0]

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

            statement: str = f'UPDATE birthdays ' \
                             f'SET firstname="{first_name}" ' \
                             f'lastname="{last_name}" ' \
                             f'day={day} ' \
                             f'month={month} ' \
                             f'year={year} ' \
                             f'WHERE firstname=? ' \
                             f'AND lastname=?'
            self.exec_func(statement, (_old_first_name, _old_last_name))

        def delete_birthday(self, first_name: str, last_name: str) -> None:
            self.exec_func(f'DELETE FROM birthdays WHERE firstname=? AND lastname=?', (first_name, last_name))

        @staticmethod
        def __build_json(result_set: tuple) -> dict:
            return {
                'first_name': result_set[0],
                'last_name': result_set[1],
                'day': result_set[2],
                'month': result_set[3],
                'year': result_set[4]
            }

    def __execute(self, command: str, values: tuple = ()) -> list | int:
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
            cursor.close()
