from sqlalchemy import Column, String, DateTime

from src.speechassistant.database.DataBasePersistency import DBPersistency

Base = DBPersistency.Base


class BirthdaySchema(Base):
    __tablename__ = "birthdays"

    first_name = Column(String, primary_key=True)
    last_name = Column(String, primary_key=True)
    date = Column(DateTime)
