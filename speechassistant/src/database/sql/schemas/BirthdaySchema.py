from datetime import date

from database.sql.schemas.AbstractSchema import AbstractSchema
from models import Birthday


class BirthdaySchema(AbstractSchema):
    def __init__(self, _id: int, first_name: str, last_name: str, _date: date):
        self.id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.date = _date

    def to_model(self, **kwargs) -> Birthday:
        return Birthday(
            first_name=self.first_name, last_name=self.last_name, date=self.date
        )

    @staticmethod
    def from_model(model: Birthday, **kwargs) -> "BirthdaySchema":
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"BirthdaySchema(id: {self.id}, first_name: {self.first_name}, last_name: {self.last_name}, date: {self.date}) "
