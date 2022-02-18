import mysql.connector as mysql

class DataBase:
    def __init__(self):
        self.speech_assistant_db = mysql.connect(
            host="",
            user="",
            password=""
        )

    def add_alarm(self, alarm):
        pass
