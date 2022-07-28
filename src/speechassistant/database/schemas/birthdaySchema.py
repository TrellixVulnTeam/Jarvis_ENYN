from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BirthdaySchema(Base):
    __tablename__ = "birthdays"

    first_name = Column(String, primary_key=True)
    last_name = Column(String, primary_key=True)
    date = Column(DateTime)
