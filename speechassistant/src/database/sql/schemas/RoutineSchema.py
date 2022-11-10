from database.sql.schemas.AbstractSchema import AbstractSchema, Model, Schema


class RoutineSchema(AbstractSchema):
    def __init__(
        self,
        _id: int,
        name: str,
        description: str,
        monday: bool,
        tuesday: bool,
        wednesday: bool,
        thursday: bool,
        friday: bool,
        saturday: bool,
        sunday: bool,
        after_alarm: bool,
        after_sunrise: bool,
        after_sunset: bool,
        after_call: bool,
    ):
        self.id = _id
        self.name = name
        self.description = description
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.sunday = sunday
        self.after_alarm = after_alarm
        self.after_sunrise = after_sunrise
        self.after_sunset = after_sunset
        self.after_call = after_call

    def to_model(self, **kwargs) -> Model:
        pass

    @staticmethod
    def from_model(model: Model, **kwargs) -> Schema:
        pass

    def __repr__(self) -> str:
        pass
