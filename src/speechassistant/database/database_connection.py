from __future__ import annotations  # compatibility for < 3.10

import io
from datetime import datetime
from typing import Callable#, TypeAlias
import os

from src.speechassistant.exceptions.CriticalExceptions import UnsolvableException
from src.speechassistant.resources.enums import OutputTypes

import sqlite3
from sqlite3 import Connection, Cursor

from src.speechassistant.exceptions.SQLException import *

#shopping_item: TypeAlias = dict[[str, int], [str, str], [str, str], [str, float]]
#timer_item: TypeAlias = dict[[str, int], [str, str], [str, str], [str, int]]
#user_item: TypeAlias = dict[
#    [str, int], [str, str], [str, str], [str, str], [str, dict[str, int], [str, int], [str, int]], [str, int], [str,
#                                                                                                                int], [
#        str, list[str]]]
#routine_item: TypeAlias = dict[[str, str], [str, dict], [str, dict], [str, dict]]

class DataBase:
    def __init__(self, root_path: str) -> None:
        logging.basicConfig(level=logging.DEBUG)
        logging.info('[ACTION] Initialize DataBase...\n')
        self.db = sqlite3.connect(f'{root_path}database\\data_base', check_same_thread=False)
        self.cursor = self.db.cursor()
        self.error_counter: int = 0

        self.user_interface = self._UserInterface(self.db, self.__execute)
        self.alarm_interface = self._AlarmInterface(self.db, self.__execute)
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
                            'aid INTEGER PRIMARY KEY,'
                            'sname VARCHAR(30),'
                            'uid INTEGER,'
                            'hour INTEGER,'
                            'minute INTEGER,'
                            'total_seconds UNSIGNED BIG INT,'
                            'text VARCHAR(255),'
                            'active INTEGER,'
                            'initiated INTEGER,'
                            'FOREIGN KEY(sname) REFERENCES audio(name),'
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
            raise UnsolvableException(f'During the creation of {self.error_counter} tables there were problems. '
                                      'Manual intervention mandatory.')

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
        self.cursor.close()
        self.db.close()

    class _UserInterface:
        def __init__(self, db: Connection, execute: Callable[[str, tuple | None], list]) -> None:
            self.db: Connection = db
            self.exec_func: Callable = execute
            logging.info('[INFO] UserInterface initialized.')

        def get_user(self, user: str | int) -> user_item:
            if type(user) is str:
                user: int = self.__get_user_id(user)

            statement: str = f'SELECT * from user WHERE uid=?'
            result_set: list[tuple[int, str, str, str, str, int, int]] = self.exec_func(statement, (user,))
            return self.__build_json(result_set)[0]

        def get_user_by_messenger_id(self, messenger_id: int) -> user_item:
            result_set: list[tuple] = self.exec_func(f'SELECT * FROM user WHERE mid=?', (messenger_id,))
            return self.__build_json(result_set)[0]

        def get_users(self) -> list[user_item]:
            statement: str = 'SELECT * from user'
            result_set: list[tuple[int, str, str, str, str, int, int]] = self.exec_func(statement, ())

            user_list: list[user_item] = self.__build_json(result_set)

            for user in user_list:
                notification_statement: str = f'SELECT text FROM notification WHERE uid=?'
                notification_result_set: list[tuple] = self.exec_func(notification_statement, (user.get("uid"),))
                for text, in notification_result_set:
                    user["waiting_notifications"].append(text)

            return user_list

        def add_user(self, alias: str, firstname: str, lastname: str, birthday: dict, messenger_id: int = 0,
                     song_id: int = 1) -> None:
            statement: str = f'INSERT INTO user (alias, firstname, lastname, birthday, mid, sname) ' \
                             f'VALUES (?, ?, ?, ?, ?, ?)'
            self.exec_func(statement, (alias, firstname, lastname, self.__birthday_to_string(birthday), messenger_id, song_id))

        def add_user_notification(self, user: int | str, notification: str):
            if type(user) is str:
                user: int = self.__get_user_id(user)

            statement: str = f'INSERT INTO notification (uid, text) VALUES (?, ?)'
            self.exec_func(statement, (user, notification))

        # The first line of attributes is for mapping purposes only, so that the user can be specified more easily
        def update_user(self, uid: int = None, alias: str = None, first_name: str = None, last_name: str = None,
                        _new_alias: str = None, _new_first_name: str = None, _new_last_name: str = None,
                        _birthday: dict = None, _messenger_id: int = 0, _song_name: str = 'standard'):

            # SELECT(s) is/are needed to ensure consistency of the data. Do not enter a value that does not exist!

            if uid is not None:
                try:
                    result_set: tuple = self.exec_func(f'SELECT * FROM user WHERE uid=?', (uid,))[0]
                except IndexError:
                    raise NoMatchingEntry(f'No matching user with the user-id {uid} was found in the database.')
            elif alias is not None:
                try:
                    result_set: tuple = self.exec_func(f'SELECT * FROM user WHERE alias=?', (alias,))[0]
                except IndexError:
                    raise NoMatchingEntry(f'No matching user with the alias "{alias}" was found in the database.')
            elif first_name is not None and last_name is not None:
                try:
                    result_set: tuple = self.exec_func(f'SELECT * FROM user '
                                                       f'WHERE firstname=? '
                                                       f'AND lastname=?', (first_name, last_name))[0]
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

            # SELECT is needed to ensure consistency of the data. Do not enter a song name that does not exist!
            try:
                sname = self.exec_func(f'SELECT name FROM audio WHERE name=?', (_song_name,))[0]
            except IndexError:
                raise NoMatchingEntry(f'No matching audio file with the name {_song_name} was found in the database.')

            statement: str = f'UPDATE user ' \
                             f'SET alias=?, firstname=?, lastname=?, ' \
                             f'birthday=?, mid=?, sname=? ' \
                             f'WHERE uid=?'
            self.exec_func(statement, (alias, firstname, lastname, self.__birthday_to_string(birthday), mid, sname, uid))

        def delete_user_notification(self, user: int | str, text: str) -> None:
            if type(user) is str:
                user: int = self.__get_user_id(user)

            statement: str = f'DELETE FROM notification WHERE uid=? AND text=?'
            self.exec_func(statement, (user, text))

        def delete_user(self, user: int | str) -> None:
            if type(user) is str:
                user: int = self.__get_user_id(user)

            statement: str = f'DELETE FROM user WHERE uid=?'
            self.exec_func(statement, (user,))

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

        @staticmethod
        def __build_json(result_set: list[tuple]) -> list:
            result_list: list[dict] = []

            for uid, alias, firstname, lastname, birthday, mid, sname in result_set:
                result_list.append({
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
                })
            return result_list

    class _AlarmInterface:
        def __init__(self, db: Connection, execute: Callable[[str, tuple | None], list]) -> None:
            self.db: Connection = db
            self.exec_func = execute
            logging.info('[INFO] AlarmInterface initialized.')

        def get_alarms(self) -> list[dict]:
            result_set: list = self.exec_func('SELECT * FROM alarm', ())
            returning_list: list[dict] = []
            for item in result_set:
                returning_list.append(self.__build_json(item))
            return returning_list

        def add_alarm(self, time: dict, text: str, user_id: int, repeating: dict, active: bool = True,
                      initiated: bool = False, song: str = 'standard.wav') -> None:

            statement: str = f'INSERT INTO alarm (sname, uid, hour, minute, total_seconds, text, active, initiated) ' \
                             f'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'

            self.exec_func(statement, (song, user_id, time["hour"], time["minute"], time["total_seconds"], text,
                                       int(active), int(initiated)))

            alarm_id: int = self.exec_func('SELECT last_insert_rowid()', ())[0][0]

            statement: str = f'INSERT INTO alarmrepeat VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
            values: list = [alarm_id]
            for item in repeating.keys():
                if repeating.get(item):
                    values.append("1")
                else:
                    values.append("0")
            self.exec_func(statement, tuple(values))

        def delete_alarm(self, aid: int) -> None:
            self.exec_func(f'DELETE FROM alarm WHERE aid=?', (aid,))
            self.exec_func(f'DELETE FROM alarmrepeat WHERE aid=?', (aid,))

        def update_alarm(self, aid: int, _time: dict = None, _text: str = None, _user: int | str = None,
                         _active: bool = None, _initiated: bool = None, _regular: bool = None, _sound: str = None):

            # If there is no item with the name, the user should be told about it and not just not update anything
            try:
                result_set: tuple = self.exec_func(f'SELECT * FROM alarm WHERE aid=', (aid,))[0]
            except IndexError:
                raise NoMatchingEntry(f'No matching element with the alarm-id {aid} was found in the database.')

            aid, sname, uid, hour, minute, total_seconds, text, active, initiated = result_set

            if _time is not None:
                hour = _time["hour"]
                minute = _time["minute"]
            if _text is not None:
                text = _text
            if _user is not None:
                if type(_user) is str:
                    try:
                        uid = self.exec_func('SELECT uid FROM user WHERE name=?', (_user,))[0]
                    except IndexError:
                        raise NoMatchingEntry(f'No user found with name "{_user}.')
                else:
                    uid = _user
            if _active is not None:
                active = int(_active is True)
            if _initiated is not None:
                initiated = int(_initiated is True)
            if _sound is not None:
                if len(self.exec_func(f'SELECT * FROM audio WHERE name=?', (_sound,))) == 0:
                    raise NoMatchingEntry(f'No audio found with name "{_sound}')
                sname = _sound

            statement: str = f'UPDATE alarm SET sname=?, uid=?, hour=?, minute=?, total_seconds=?, text=?, active=?, ' \
                             f'initiaded=? WHERE aid=?'
            self.exec_func(statement, (sname, uid, hour, minute, total_seconds, text, active, initiated, aid))

        def update_repeating(self, aid: int, _monday: bool = None, _tuesday: bool = None, _wednesday: bool = None,
                             _thursday: bool = None, _friday: bool = None, _saturday: bool = None,
                             _sunday: bool = None):
            try:
                result_set: tuple = self.exec_func(f'SELECT * FROM alarmrepeat WHERE aid=?', (aid,))[0]
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
            self.exec_func(statement, (monday, tuesday, wednesday, thursday, friday, saturday, sunday, aid))

        def __build_json(self, result_set: list) -> dict | list[dict]:
            result_list: list[dict] = []
            for aid, sname, uid, hour, minute, total_seconds, text, active, initiated in result_set:
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
                    "initiated": initiated
                })
            return result_list

        def __create_table(self):
            pass

    class _AudioInterface:

        def __init__(self, db: Connection, execute: Callable[[str, tuple | None], list]) -> None:
            self.db: Connection = db
            self.exec_func = execute
            self.audio_path: str = ''
            logging.info('[INFO] AudioInterface initialized.')

        def add_audio(self, name: str, path: str = None, audio_file: io.BytesIO = None) -> None:

            if path is not None and not audio_file is None:
                raise ValueError('Got too many arguments! Decide between the path and the audio file.')
            elif path is not None:
                path = self.__justify_file_path(name, path)
            elif audio_file is not None:
                self.__save_audio_file(name, audio_file)
                path = self.audio_path + f'{name}.wav'
            else:
                raise ValueError('Neither path nor audio file given!')

            self.exec_func(f'INSERT INTO audio (name, path) VALUES (?, ?)', (name, path))

        def update_audio(self, _audio_name: str, _new_audio_name: str = None, _path: str = None,
                         _audio_file: io.BytesIO = None) -> None:
            try:
                result_set: tuple = self.exec_func(f'SELECT * FROM audio WHERE name=?', (_audio_name,))[0]
            except IndexError:
                raise NoMatchingEntry(f'No matching element with the audio name "{_audio_name}" was found '
                                      f'in the database.')

            name, path = result_set

            if _new_audio_name is not None:
                name = _new_audio_name

            if _path is not None and _audio_file is not None:
                raise ValueError('Got too many arguments! Decide between the path and the audio file.')
            elif _path is not None:
                # old_path is needed after the SQL query
                old_path: str = _path
                path = self.__justify_file_path(_audio_name, _path)
            elif _audio_file is not None:
                self.__save_audio_file(_audio_name, _audio_file)
                path = self.audio_path + _audio_name

            statement: str = f'UPDATE FROM audio ' \
                             f'SET path=? ' \
                             f'WHERE name=?'
            self.exec_func(statement, (name, path))

            # delete file only after database access has worked
            if path is not None:
                # delete file, if no other entry in the database uses it
                path_refs: list = self.exec_func(f'SELECT name FROM audio WHERE path=?', (old_path))
                if len(path_refs) == 0:
                    os.remove(old_path)
                    logging.info(f'[ACTION] Audio file deleted ({old_path})')

        def delete_audio(self, audio_name: str) -> None:
            file_path: str = self.exec_func(f'SELECT path FROM audio WHERE name=?', (audio_name,))[0][0]
            self.exec_func(f'DELETE FROM audio WHERE name=?', (audio_name,))

            # delete file only after database access has worked
            os.remove(file_path)
            logging.info(f'[ACTION] Deleted audiofile "{file_path}".')

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

            statement: str = f'SELECT * FROM timer'
            result_set: list = self.exec_func(statement, ())

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
            result_list: list[dict] = []
            if type(user) is str:
                user = self.user_interface.__get_user_id(user)

            result_set: list[tuple] = self.exec_func(f'SELECT * FROM timer WHERE uid=?', (user,))
            for timer in result_set:
                result_list.append(self.__build_json(timer))

            return result_list

        def get_timer(self, timer_id: int) -> timer_item:
            statement: str = f'SELECT * FROM timer WHERE id=? LIMIT 1'
            result_set: list[tuple[int, str, str, str, int]] = self.exec_func(statement, (timer_id,))

            return self.__build_json(result_set[0])

        def add_timer(self, time: datetime, duration: str, text: str, user_id: int) -> int:
            if len(text) > 255:
                raise ValueError('Given text is too long!')
            if len(duration) > 50:
                duration = self.__shorten_duration_string(duration)

            statement: str = f'INSERT INTO timer (duration, time, text, uid) ' \
                             f'VALUES(?, ?, ?, ?)'
            result_set: list | int = self.exec_func(statement, (duration, {self.__build_time_string(time)}, text, user_id))
            if type(result_set) is list:
                raise RuntimeError(f'__execute() returned wrong type on INSERT command! (command: {statement})')
            else:
                # id from inserted timer - id from the first timer in the current database +1
                return int(result_set) - self.exec_func('SELECT id FROM timer LIMIT 1', ())[0][0] + 1

        def update_timer(self, timer_id: int, _duration: str = None, _time: datetime = None, _text: str = None,
                         _user: int | str = None) -> None:

            try:
                result_set: tuple = self.exec_func(f'SELECT * FROM timer WHERE id=?', (timer_id,))[0]
            except IndexError:
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
                        uid = self.exec_func(f'SELECT uid FROM user WHERE name=?', (_user,))[0]
                    except IndexError:
                        raise NoMatchingEntry(f'No user with name {_user} found!')
                else:
                    # SELECT is needed to ensure consistency of the data. Do not enter a uid that does not exist!
                    try:
                        uid = self.exec_func(f'SELECT uid FROM user WHERE uid=?', (_user,))[0]
                    except IndexError:
                        raise NoMatchingEntry(f'No user with id {_user} found!')

            statement: str = f'UPDATE timer ' \
                             f'SET duration=?, time=?, text=?, uid=? ' \
                             f'WHERE id=?'
            self.exec_func(statement, (duration, time, text, uid, tid))

        def delete_timer(self, timer_id: int) -> None:
            self.exec_func(f'DELETE FROM timer WHERE id=?', (timer_id,))

        def delete_passed_timer(self) -> None:
            self.exec_func(f'DELETE FROM timer WHERE time < ?', (self.__build_time_string(datetime.now()),))

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
            statement: str = f'SELECT * FROM reminder'
            result_set: list[tuple[int, str, str, int]] = self.exec_func(statement, ())

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

            statement: str = f'INSERT INTO reminder (time, text, uid) ' \
                             f'VALUES (?, ?, ?)'
            self.exec_func(statement, (time, text, user))

        def delete_reminder(self, _id: int):
            self.exec_func(f'DELETE FROM reminder WHERE id=?', (_id,))

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
            statement: str = 'SELECT * FROM shoppinglist'
            result_set: list[tuple[int, str, str, float]] = self.exec_func(statement, ())
            return self.__build_json(result_set)

        def get_item(self, name: str) -> dict:
            result_set = self.exec_func(f'SELECT * FROM shoppinglist WHERE name=?', (name,))
            return self.__build_json(result_set)[0]

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

        @staticmethod
        def __build_json(result_set: list[tuple[int, str, str, float]]) -> list[shopping_item]:
            result_list: list[shopping_item] = []

            for name, measure, quantity in result_set:
                if quantity.is_integer():
                    quantity = int(quantity)
                result_list.append({
                    "name": name,
                    "measure": measure,
                    "quantity": quantity
                })
            return result_list

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
        result_set: list = []
        try:
            result_set = self.cursor.execute(command, values).fetchall()
            if 'insert into' in command.lower():
                return self.cursor.lastrowid
        except Exception as e:
            self.error_counter += 1
            logging.warning(f"[ERROR] Couldn't execute SQL command: {command}:\n {e}")
            self.db.rollback()
            raise SQLException(f"Couldn't execute SQL Statement: {command}\n{e}")
        return result_set
