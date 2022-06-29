from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Time, DateTime
from sqlalchemy.orm import relationship

from src.speechassistant.database.DataBasePersistency import DBPersistency
from src.speechassistant.models.alarm import Alarm, AlarmRepeating

Base = DBPersistency.Base


class AlarmRepeatingSchema(Base):
    __tablename__ = "alarm_repeatings"

    id = Column(Integer, primary_key=True)
    alarm_id = Column(Integer, ForeignKey("alarms.id"))
    monday = Column(Boolean)
    tuesday = Column(Boolean)
    wednesday = Column(Boolean)
    thursday = Column(Boolean)
    friday = Column(Boolean)
    saturday = Column(Boolean)
    sunday = Column(Boolean)
    regular = Column(Boolean)

    def __repr__(self) -> str:
        return f"AlarmRepeatingSchema(monday={self.monday}, tuesday={self.tuesday}, wednesday={self.wednesday}, thursday={self.thursday}, friday={self.friday}, saturday={self.saturday}, sunday={self.sunday}"


class AlarmSchema(Base):
    __tablename__ = "alarms"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    alarm_time = Column(Time)
    repeating = relationship("AlarmRepeatingSchema")
    song_name = Column(String)
    active = Column(Boolean)
    initiated = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))
    last_executed = Column(DateTime)


def alarm_to_schema(alarm: Alarm) -> AlarmSchema:
    alarm_repeating_schema: AlarmRepeatingSchema = AlarmRepeatingSchema(
        monday=alarm.repeating.monday,
        tuesday=alarm.repeating.tuesday,
        wednesday=alarm.repeating.wednesday,
        thursday=alarm.repeating.thursday,
        friday=alarm.repeating.friday,
        saturday=alarm.repeating.saturday,
        sunday=alarm.repeating.sunday,
        regular=alarm.repeating.regular,
    )

    return AlarmSchema(
        id=alarm.alarm_id,
        text=alarm.text,
        alarm_time=alarm.alarm_time,
        repeating=alarm_repeating_schema,
        song_name=alarm.song_name,
        active=alarm.active,
        initiated=alarm.initiated,
        user_id=alarm.user_id,
        last_executed=alarm.last_executed,
    )


def schema_to_alarm(alarm_schema: AlarmSchema) -> Alarm:
    alarm_repeating: AlarmRepeating = AlarmRepeating(
        monday=alarm_schema.repeating.monday,
        tuesday=alarm_schema.repeating.tuesday,
        wednesday=alarm_schema.repeating.wednesday,
        thursday=alarm_schema.repeating.thursday,
        friday=alarm_schema.repeating.friday,
        saturday=alarm_schema.repeating.saturday,
        sunday=alarm_schema.repeating.sunday,
        regular=alarm_schema.repeating.regular,
    )

    return Alarm(
        alarm_id=alarm_schema.id,
        text=alarm_schema.text,
        alarm_time=alarm_schema.alarm_time,
        repeating=alarm_repeating,
        song_name=alarm_schema.song_name,
        active=alarm_schema.active,
        initiated=alarm_schema.initiated,
        user_id=alarm_schema.user_id,
        last_executed=alarm_schema.last_executed,
    )
