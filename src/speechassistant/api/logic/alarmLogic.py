from src.speechassistant.database.database_connection import DataBase
from src.speechassistant.exceptions.SQLException import NoMatchingEntry
from src.speechassistant.models.alarm import Alarm

alarm_interface: any = DataBase.get_instance().alarm_interface


class AlarmLogic:
    @staticmethod
    def create_alarm(alarm: Alarm) -> Alarm:
        return alarm_interface.add_alarm(alarm)

    @staticmethod
    def read_all_alarms() -> list[Alarm]:
        print(alarm_interface.get_all_alarms())
        return alarm_interface.get_all_alarms()

    @staticmethod
    def read_alarm_by_id(alarm_id: int) -> Alarm:
        return alarm_interface.get_alarm_by_id(alarm_id)

    @staticmethod
    def update_alarm(alarm: Alarm) -> Alarm:
        return alarm_interface.update_alarm(alarm)

    @staticmethod
    def delete_alarm(alarm_id: int) -> None:
        if alarm_interface.delete_alarm(alarm_id) < 1:
            raise NoMatchingEntry()
