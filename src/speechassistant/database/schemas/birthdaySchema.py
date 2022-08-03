from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from src.speechassistant.models.birthday import Birthday

Base = declarative_base()


class BirthdaySchema(Base):
    __tablename__ = "birthdays"

    first_name = Column(String, primary_key=True)
    last_name = Column(String, primary_key=True)
    date = Column(DateTime)


def birthday_to_schema(model: Birthday) -> BirthdaySchema:
    return BirthdaySchema(
        first_name=model.first_name,
        last_name=model.last_name,
        date=model.date
    )


def schema_to_birthday(schema: BirthdaySchema) -> Birthday:
    return Birthday(
        first_name=schema.first_name,
        last_name=schema.last_name,
        date=schema.date
    )
