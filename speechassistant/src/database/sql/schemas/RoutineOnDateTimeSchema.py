import datetime

from database.sql.schemas.AbstractSchema import AbstractSchema, Model, Schema


class RoutineOnDateTimeSchema(AbstractSchema):
    def __init__(self, _id: int, month: int, day: int, time: datetime.time):
        self.id: int = _id
        self.month: int = month
        self.day: int = day
        self.time: datetime.time = time

    def to_model(self, **kwargs) -> Model:
        pass

    @staticmethod
    def from_model(model: Model, **kwargs) -> Schema:
        pass

    def __repr__(self) -> str:
        pass
