from src.database.sql.schemas.AbstractSchema import AbstractSchema, Schema
from src.models import AlarmRepeating


class AlarmRepeatingSchema(AbstractSchema):
    def __init__(self, _id: int, monday: bool, tuesday: bool, wednesday: bool, thursday: bool, friday: bool,
                 saturday: bool, sunday: bool, regular: bool):
        super().__init__()
        self.id = _id
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.sunday = sunday
        self.regular = regular

    def to_model(self) -> AlarmRepeating:
        return AlarmRepeating(
            monday=self.monday,
            tuesday=self.tuesday,
            wednesday=self.wednesday,
            thursday=self.thursday,
            friday=self.friday,
            saturday=self.saturday,
            sunday=self.sunday,
            regular=self.regular
        )

    @staticmethod
    def from_model(model: AlarmRepeating, alarm_id: int) -> Schema:
        return AlarmRepeatingSchema(
            _id=alarm_id,
            monday=model.monday,
            tuesday=model.tuesday,
            wednesday=model.wednesday,
            thursday=model.thursday,
            friday=model.friday,
            saturday=model.saturday,
            sunday=model.sunday,
            regular=model.regular
        )

    def __repr__(self) -> str:
        return f"AlarmRepeatingSchema(id: {self.id}, monday: {self.monday}, tuesday: {self.tuesday}, wednesday: {self.wednesday}, thursday: {self.thursday}, friday: {self.friday}, saturday: {self.saturday}, sunday: {self.sunday}, regular: {self.regular})"
