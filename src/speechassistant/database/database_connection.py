import io
import logging
from datetime import datetime
from typing import Callable, TypeAlias
import os

from src.speechassistant.exceptions.CriticalExceptions import UnsolvableException

import sqlite3
from sqlite3 import Connection, Cursor

from src.speechassistant.exceptions.SQLException import *

shopping_item: TypeAlias = dict[[str, int], [str, str], [str, str], [str, float]]
timer_item: TypeAlias = dict[[str, int], [str, str], [str, str], [str, int]]
user_item: TypeAlias = dict[
    [str, int], [str, str], [str, str], [str, str], [str, dict[str, int], [str, int], [str, int]], [str, int], [str,
                                                                                                                int], [
        str, list[str]]]
routine_item: TypeAlias = dict[[str, str], [str, dict], [str, dict], [str, dict]]


class DataBase:
    def __init__(self, root_path: str) -> None:
        logging.basicConfig(level=logging.DEBUG)
        logging.info('[ACTION] Initialize DataBase...\n')
        self.db = sqlite3.connect(f'{root_path}database\\data_base')
        self.error_counter: int = 0

        self.alarm_interface = self._AlarmInterface(self.db, self.__execute)
        self.timer_interface = self._TimerInterface(self.db, self.__execute)
        self.reminder_interface = self._ReminderInterface(self.db, self.__execute)
        self.quiz_interface = self._QuizInterface(self.db)
        self.shoppinglist_interface = self._ShoppingListInterface(self.db, self.__execute)
        self.user_interface = self._UserInterface(self.db, self.__execute)
        self.routine_interface = self._RoutineInterface(self.db, self.__execute)
        self.audio_interface = self._AudioInterface(self.db, self.__execute)
        self.__audio_path: str = ''

        logging.info('\n[INFO] DataBase successfully initialized.')

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
                            'mid INTEGER UNIQUE,'
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
                            'sunday INTEGER)')

        self.__create_table('CREATE TABLE IF NOT EXISTS timer ('
                            'id INTEGER PRIMARY KEY,'
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
                            'rid INTEGER PRIMARY KEY, '
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

        self.__create_table('CREATE TABLE IF NOT EXISTS routineactivation ('
                            'rid INTEGER, '
                            'hour INTEGER, '
                            'minute INTEGER, '
                            'FOREIGN KEY(rid) REFERENCES routine (rid), '
                            'PRIMARY KEY(rid, hour, minute))')

        self.__create_table('CREATE TABLE IF NOT EXISTS routinedates ('
                            'rid INTEGER,'
                            'day INTEGER,'
                            'month INTEGER,'
                            'PRIMARY KEY(rid, day, month),'
                            'FOREIGN KEY(rid) REFERENCES routine(rid))')

        self.__create_table('CREATE TABLE IF NOT EXISTS routinecommands ('
                            'id INTEGER PRIMARY KEY, '
                            'rid INTEGER NOT NULL, '
                            'modulename VARCHAR(50), '
                            'FOREIGN KEY(rid) REFERENCES routine(rid))')

        self.__create_table('CREATE TABLE IF NOT EXISTS commandtext ('
                            'rid INTEGER,'
                            'text VARCHAR(255) NOT NULL,'
                            'PRIMARY KEY(rid, text),'
                            'FOREIGN KEY(rid) REFERENCES routinecommands(id))')

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

        self.db.commit()

        if self.error_counter == 0:
            logging.info('\n[INFO] Tables successfully created!')
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
        self.db.close()

    class _AlarmInterface:
        def __init__(self, db: Connection, execute: Callable[[str], list]) -> None:
            self.db: Connection = db
            self.exec_func = execute
            logging.info('[INFO] AlarmInterface initialized.')

        def get_alarms(self) -> list[dict]:
            result_set: list = self.exec_func('SELECT * FROM alarm')
            returning_list: list[dict] = []
            for item in result_set:
                returning_list.append(self.__build_json(item))
            return returning_list

        def add_alarm(self, time: dict, text: str, user_id: int, repeating: dict, active: bool = True,
                      initiated: bool = False, song: str = 'standard.wav') -> None:
            if active:
                active_int: int = 1
            else:
                active_int: int = 0

            if initiated:
                init_int = 1
            else:
                init_int = 0

            statement: str = f'INSERT INTO alarm (sname, uid, hour, minute, total_seconds, text, active, initiated) ' \
                             f'VALUES ({song}, {user_id}, {time["hour"]}, {time["minute"]}, ' \
                             f'{time["total_seconds"]}, "{text}", {active_int}, {init_int})'

            self.exec_func(statement)

            alarm_id: int = self.exec_func('SELECT last_insert_rowid()')[0][0]

            statement: str = f'INSERT INTO alarmrepeat VALUES ({alarm_id}, '
            for item in repeating.keys():
                if repeating.get(item):
                    statement += str(1) + ', '
                else:
                    statement += str(0) + ', '
            self.exec_func(statement[:len(statement) - 2] + ')')

        def delete_alarm(self, aid: int) -> None:
            self.exec_func(f'DELETE FROM alarm WHERE aid={aid}')
            self.exec_func(f'DELETE FROM alarmrepeat WHERE aid={aid}')

        def update_alarm(self, aid: int, time: dict = None, text: str = None, user: int = None, active: bool = None,
                         initiated: bool = None, sound: str = None):
            old_alarm: tuple = self.exec_func(f'SELECT * FROM alarm WHERE aid={aid}')[0]
            if not time is None:
                old_alarm[3] = time["hour"]
                old_alarm[4] = time["minute"]
            if not text is None:
                old_alarm[6] = text
            if not user is None:
                old_alarm[2] = user
            if not active is None:
                old_alarm[7] = int(active == True)
            if not initiated is None:
                old_alarm[8] = int(initiated == True)
            if not sound is None:
                old_alarm[1] = initiated

            statement: str = f'UPDATE alarm SET sname="{old_alarm[2]}", uid={old_alarm[3]}, hour={old_alarm[4]}, minute={old_alarm[5]}, total_seconds={old_alarm[6]}, text="{old_alarm[7]}", ' \
                             f'active={old_alarm[8]}, initiaded={old_alarm[9]} ' \
                             f'WHERE aid={aid}'
            self.exec_func(statement)

        def update_repeating(self, aid: int, monday: bool = None, tuesday: bool = None, wednesday: bool = None,
                             thursday: bool = None, friday: bool = None, saturday: bool = None, sunday: bool = None):
            old_repeating: tuple = self.exec_func(f'SELECT * FROM alarmrepeat WHERE aid={aid}')[0]
            if monday is not None:
                old_repeating[1] = int(monday is True)
            if tuesday is not None:
                old_repeating[1] = int(tuesday is True)
            if wednesday is not None:
                old_repeating[1] = int(wednesday is True)
            if thursday is not None:
                old_repeating[1] = int(thursday is True)
            if friday is not None:
                old_repeating[1] = int(friday is True)
            if saturday is not None:
                old_repeating[1] = int(saturday is True)
            if sunday is not None:
                old_repeating[1] = int(sunday is True)

            statement: str = f'UPDATE alarmrepeat ' \
                             f'SET monday={monday}, tuesday={tuesday}, wednesday={wednesday}, thursday={thursday}, friday={friday}, saturday={saturday}, friday={friday} ' \
                             f'WHERE aid={aid}'

        def __build_json(self, result_set: list) -> dict | list[dict]:
            result_list: list[dict] = []
            for aid, sname, uid, hour, minute, total_seconds, text, active, initiated in result_set:
                sound_path: str = self.exec_func(f'SELECT path FROM audio WHERE name="{sname}"')[0]
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

        def __init__(self, db: Connection, execute: Callable[[str], list]) -> None:
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

            self.exec_func(f'INSERT INTO audio (name, path) VALUES ("{name}", "{path}")')

        def update_audio(self, audio_name: str, new_audio_name: str = None, path: str = None,
                         audio_file: io.BytesIO = None) -> None:
            old_audio: tuple = self.exec_func(f'SELECT * FROM audio WHERE name="{audio_name}"')[0]
            if new_audio_name is not None:
                old_audio[0] = new_audio_name

            if path is not None and audio_file is not None:
                raise ValueError('Got too many arguments! Decide between the path and the audio file.')
            elif path is not None:
                old_path: str = old_audio[1]
                old_audio[1] = self.__justify_file_path(audio_name, path)
            elif audio_file is not None:
                self.__save_audio_file(audio_name, audio_file)

            statement: str = f'UPDATE FROM audio ' \
                             f'SET path="{old_audio[0]}" ' \
                             f'WHERE name="{old_audio[1]}"'
            self.exec_func(statement)

            # delete file only after database access has worked
            if path is not None:
                # delete file, if no other entry in the database uses it
                path_refs: list = self.exec_func(f'SELECT name FROM audio WHERE path={old_path}')
                if len(path_refs) == 0:
                    os.remove(old_path)

        def delete_audio(self, audio_name: str) -> None:
            file_path: str = self.exec_func(f'SELECT path FROM audio WHERE name="{audio_name}"')[0][0]
            self.exec_func(f'DELETE FROM audio WHERE name="{audio_name}"')

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

        def __init__(self, db: Connection, execute: Callable[[str], list]) -> None:
            self.db: Connection = db
            self.exec_func = execute
            logging.info('[INFO] TimerInterface initialized.')

        def get_all_timer(self) -> list[timer_item]:
            result_dict: list[dict] = []
            statement: str = f'SELECT * FROM timer'
            result_set: list = self.exec_func(statement)
            for timer in result_set:
                result_dict.append(self.__build_json(timer))

            return result_set

        def get_timer(self, timer_id: int) -> timer_item:
            statement: str = f'SELECT * FROM timer WHERE id={timer_id} LIMIT 1'
            result_set: list[tuple[int, str, str, str, int]] = self.exec_func(statement)

            return self.__build_json(result_set[0])

        def add_timer(self, time: datetime, text: str, user_id: int) -> None:
            if len(text) > 255:
                raise ValueError('Given text is too long!')

            statement: str = f'INSERT INTO timer (time, text, uid) ' \
                             f'VALUES("{self.__build_time_string(time)}", "{text}", {user_id})'
            self.exec_func(statement)

        def update_timer(self, timer_id: int, time: datetime = None, text: str = None, uid: int = None) -> None:
            old_timer: tuple = self.exec_func(f'SELECT * FROM timer WHERE id={timer_id}')[0]

            if time is not None:
                old_timer[1] = self.__build_time_string(time)
            if text is not None:
                if len(text) > 255:
                    raise ValueError('Given text is too long!')
                old_timer[2] = text
            if uid is not None:
                old_timer[3] = uid

            statement: str = f'UPDATE timer ' \
                             f'SET time="{old_timer[1]}", text="{old_timer[2]}", uid={old_timer[3]} ' \
                             f'WHERE id={old_timer[4]}'
            self.exec_func(statement)

        def delete_timer(self, timer_id: int) -> None:
            self.exec_func(f'DELETE FROM timer WHERE id={timer_id}')

        @staticmethod
        def __build_json(timer: tuple[int, str, str, str, int]) -> dict:
            time: str = timer[1]
            return {
                "id": timer[0],
                "time": datetime(int(time[0:4]), int(time[4:6]), int(time[6:8]),
                                 int(time[8:10]), int(time[10:12]), int(time[12:]), 0),
                "text": timer[2],
                "uid": timer[3]
            }

        @staticmethod
        def __build_time_string(time: datetime) -> str:
            return str(time.date()).replace('-', '') + str(time.time())[0:8].replace(':', '')

        def __create_table(self):
            pass

    class _ReminderInterface:

        def __init__(self, db: Connection, execute: Callable[[str], list]) -> None:
            self.db: Connection = db
            self.exec_func: Callable = execute
            logging.info('[INFO] ReminderInterface initialized.')

        def get_reminder(self):
            statement: str = f'SELECT * FROM reminder'
            result_set: list[tuple[int, str, str, int]] = self.exec_func(statement)

            return self.__build_json(result_set)

        def add_reminder(self, text: str, time: str | None, user: int | str = None) -> None:
            if len(text) > 255:
                raise ValueError('Given text is too long!')

            if len(time) != 14:
                raise ValueError("Given time doesn't match!")

            if user is None:
                user = -1
            elif type(user) is str:
                user = self.__get_user_id(user)

            if time is None:
                time = ''

            statement: str = f'INSERT INTO reminder (time, text, uid) ' \
                             f'VALUES ("{time}", "{text}", "{user}")'
            self.exec_func(statement)

        def delete_reminder(self, _id: int):
            self.exec_func(f'DELETE FROM reminder WHERE id={_id}')

        def __get_user_id(self, alias: str) -> int:
            user_result_set: list[tuple[str]] = self.exec_func(f'SELECT uid FROM user WHERE alias="{alias}"')
            if len(user_result_set) == 1:
                return int(user_result_set[0][0])
            else:
                raise UserNotFountException()

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

        def __init__(self, db: Connection, execute: Callable[[str], list]) -> None:
            self.db: Connection = db
            self.exec_func: Callable = execute
            logging.info('[INFO] ShoppingListInterface initialized.')

        def get_list(self) -> list[shopping_item]:
            statement: str = 'SELECT * FROM shoppinglist'
            result_set: list[tuple[int, str, str, float]] = self.exec_func(statement)
            return self.__build_json(result_set)

        def add_item(self, name: str, measure: str, quantity: float) -> None:
            statement: str = f'INSERT INTO shoppinglist ("name", "measure", "quantity") ' \
                             f'VALUES ("{name}", "{measure}", {quantity})'
            self.exec_func(statement)

        def update_item(self, name: str, quantity: float) -> None:
            statement: str = f'UPDATE shoppinglist ' \
                             f'SET quantity="{quantity}" ' \
                             f'WHERE name="{name}"'
            self.exec_func(statement)

        def remove_item(self, name: str) -> None:
            statement: str = f'DELETE FROM shoppinglist WHERE name="{name}"'
            self.exec_func(statement)

        def clear_list(self) -> None:
            statement: str = f'DELETE FROM shoppinglist'
            self.exec_func(statement)

        def __create_table(self):
            pass

        @staticmethod
        def __build_json(result_set: list[tuple[int, str, str, float]]) -> list[shopping_item]:
            result_list: list[shopping_item] = []

            for rid, name, measure, quantity in result_set:
                result_list.append({
                    "id": rid,
                    "name": name,
                    "measure": measure,
                    "quantity": quantity
                })
            return result_list

    class _UserInterface:
        def __init__(self, db: Connection, execute: Callable[[str], list]) -> None:
            self.db: Connection = db
            self.exec_func: Callable = execute
            logging.info('[INFO] UserInterface initialized.')

        def get_user(self, user: str | int) -> user_item:
            if type(user) is str:
                user: int = self.__get_user_id(user)

            statement: str = f'SELECT * from user WHERE uid="{user}"'
            result_set: list[tuple[int, str, str, str, str, int, int]] = self.exec_func(statement)
            return self.__build_json(result_set)[0]

        def get_users(self) -> list[user_item]:
            statement: str = 'SELECT * from user'
            result_set: list[tuple[int, str, str, str, str, int, int]] = self.exec_func(statement)

            user_list: list[user_item] = self.__build_json(result_set)

            for user in user_list:
                notification_statement: str = f'SELECT text FROM notification WHERE uid="{user.get("uid")}"'
                notification_result_set: list[tuple] = self.exec_func(notification_statement)
                for text, in notification_result_set:
                    user["waiting_notifications"].append(text)

            return user_list

        def add_user(self, alias: str, firstname: str, lastname: str, birthday: dict, messenger_id: int = 0,
                     song_id: int = 1) -> None:
            statement: str = f'INSERT INTO user (alias, firstname, lastname, birthday, mid, sid)' \
                             f'VALUES ("{alias}", "{firstname}", "{lastname}", ' \
                             f'"{self.__birthday_to_string(birthday)}", "{messenger_id}", "{song_id}") '
            self.exec_func(statement)

        def add_user_notification(self, user: int | str, notification: str):
            if type(user) is str:
                user: int = self.__get_user_id(user)

            statement: str = f'INSERT INTO notification (uid, text) VALUES ("{user}", "{notification}")'
            self.exec_func(statement)

        def update_user(self, uid: int, alias: str, firstname: str, lastname: str, birthday: dict,
                        messenger_id: int = 0, song_id: int = 1):
            # toDo: dynamic
            statement: str = f'UPDATE user ' \
                             f'SET alias="{alias}", firstname="{firstname}", lastname="{lastname}", ' \
                             f'birthday="{self.__birthday_to_string(birthday)}", mid="{messenger_id}", sid="{song_id}" '\
                             f'WHERE uid={uid}'
            self.exec_func(statement)

        def delete_user_notification(self, user: int | str, text: str) -> None:
            if type(user) is str:
                user: int = self.__get_user_id(user)

            statement: str = f'DELETE FROM notification WHERE uid="{user}" AND text="{text}"'
            self.exec_func(statement)

        def delete_user(self, user: int | str) -> None:
            if type(user) is str:
                user: int = self.__get_user_id(user)

            statement: str = f'DELETE FROM user WHERE uid="{user}"'
            self.exec_func(statement)

        @staticmethod
        def __birthday_to_string(birthday: dict) -> str:
            return str(birthday.get('year')) + str(birthday.get('month')).rjust(2, '0') + str(
                birthday.get('day')).rjust(2, '0')

        def __get_user_id(self, alias: str) -> int:
            user_result_set: list[tuple[str]] = self.exec_func(f'SELECT uid FROM user WHERE alias="{alias}"')
            if len(user_result_set) == 1:
                return int(user_result_set[0][0])
            else:
                raise UserNotFountException()

        def __create_table(self):
            pass

        @staticmethod
        def __build_json(result_set: list[tuple]) -> list:
            result_list: list[dict] = []

            for uid, alias, firstname, lastname, birthday, mid, sid in result_set:
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
                    "alarm_sound": sid,
                    "waiting_notifications": []
                })
            return result_list

    class _RoutineInterface:
        def __init__(self, db: Connection, execute: Callable[[str], list]) -> None:
            self.db: Connection = db
            self.exec_func: Callable = execute
            logging.info('[INFO] RoutineInterface initialized.')

        def get_routine(self, routine_id: int) -> routine_item:
            routine_set: tuple = self.exec_func(f'SELECT * FROM routine WHERE rid={routine_id}')[0]
            command_set: list[tuple] = self.exec_func(f'SELECT * FROM routinecommands WHERE rid={routine_id}')
            text_set: list[tuple] = self.exec_func(f'SELECT * FROM commandtext WHERE rid={routine_id}')
            date_set: list[tuple] = self.exec_func(f'SELECT * FROM routinedates WHERE rid={routine_id}')
            activation_set: list[tuple] = self.exec_func(f'SELECT * FROM routineactivation WHERE rid={routine_id}')

            return self.__build_json(routine_set, command_set, text_set, date_set, activation_set)

        def get_routines(self) -> list[routine_item]:
            routine_list: list[dict] = []
            routine_set: list[tuple] = self.exec_func(f'SELECT * FROM routine')

            for routine in routine_set:
                command_set: list[tuple] = self.exec_func(f'SELECT * FROM routinecommands WHERE rid={routine[0]}')
                text_set: list[tuple] = self.exec_func(f'SELECT * FROM commandtext WHERE rid={routine[0]}')
                date_set: list[tuple] = self.exec_func(f'SELECT * FROM routinedates WHERE rid={routine[0]}')
                activation_set: list[tuple] = self.exec_func(f'SELECT * FROM routineactivation WHERE rid={routine[0]}')

                routine_list.append(self.__build_json(routine, command_set, text_set, date_set, activation_set))

            return routine_list

        def add_routine(self, routine: dict) -> None:
            statement: str = f'INSERT INTO routine (description, daily, monday, tuesday, wednesday, thursday, friday, '\
                             f'saturday, sunday, afteralarm, aftersunrise, aftersunset, aftercall)' \
                             f'VALUES ("{routine.get("description")}", '
            for key in ['daily', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                statement += str(int(routine['retakes']['days'][key] is True)) + ', '
            for key in ['after_alarm', 'after_sunrise', 'after_sunset', 'after_call']:
                statement += str(int(routine["retakes"]["activation"][key] is True)) + ', '
            self.exec_func(statement[0:len(statement) - 2] + ')')

            rid: int = self.exec_func('SELECT last_insert_rowid()')[0][0]

            for module in routine['actions']['commands']:
                self.exec_func(f'INSERT INTO routinecommands (rid, modulename) VALUES ({rid}, "{module.get("module_name")}")')
                module_id: int = self.exec_func('SELECT last_insert_rowid()')[0][0]

                for text in module.get('text'):
                    self.exec_func(f'INSERT INTO commandtext VALUES ({module_id}, "{text}")')

            if len(routine['retakes']['days']['date_of_day']) > 0:
                for item in routine['retakes']['days']['date_of_day']:
                    logging.info('------------' + str(type(item)))
                    self.exec_func(f'INSERT INTO routinedates VALUES ({rid}, {item.get("day")}, {item.get("month")})')

            for item in routine['retakes']['activation']['clock_time']:
                self.exec_func(f'INSERT INTO routineactivation VALUES ({rid}, {item["hour"]}, {item["minute"]})')

        def update_routine(self):
            pass

        def delete_routine(self, routine_id: int) -> None:
            self.exec_func(f'DELETE FROM routineactivation WHERE rid={routine_id}')
            self.exec_func(f'DELETE FROM routinedates WHERE rid={routine_id}')
            self.exec_func(f'DELETE FROM commandtext WHERE rid={routine_id}')
            self.exec_func(f'DELETE FROM routinecommands WHERE rid={routine_id}')
            self.exec_func(f'DELETE FROM routine WHERE rid={routine_id}')

        @staticmethod
        def __build_json(routine: tuple, commands: list[tuple], commandtext: list[tuple], dates: list[tuple],
                         activation: list[tuple]) -> routine_item:
            result_dict = {
                "id": routine[0],
                "descriptions": routine[1],
                "retakes": {
                    "days": {
                        "daily": (routine[2] == 1),
                        "monday": (routine[3] == 1),
                        "tuesday": (routine[4] == 1),
                        "wednesday": (routine[5] == 1),
                        "thursday": (routine[6] == 1),
                        "friday": (routine[7] == 1),
                        "saturday": (routine[8] == 1),
                        "sunday": (routine[9] == 1),
                        "date_of_day": []
                    },
                    "activation": {
                        "clock_time": [],
                        "after_alarm": (routine[10] == 1),
                        "after_sunrise": (routine[11] == 1),
                        "after_sunset": (routine[12] == 1),
                        "after_call": (routine[13] == 1)
                    }
                },
                "actions": {
                    "commands": []
                }
            }

            for rid, day, month in dates:
                result_dict["retakes"]["date_of_day"].append({
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

    def __execute(self, command: str) -> list:
        cursor: Cursor = self.db.cursor()
        result_set: list
        try:
            cursor.execute(command)
            result_set = cursor.fetchall()
        except Exception as e:
            self.error_counter += 1
            logging.warning(f"[ERROR] Couldn't execute SQL command: {command}:\n {e}")
            raise SQLException(f"Couldn't execute SQL Statement: {command}\n{e}")
        finally:
            cursor.close()
        self.db.commit()
        return result_set


if __name__ == "__main__":
    dbb = DataBase("C:\\Users\\Jakob\\PycharmProjects\\Jarvis2\\src\\speechassistant\\")
    dbb.create_tables()

    dbb.stop()
