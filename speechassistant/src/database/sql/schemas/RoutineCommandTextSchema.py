from database.sql.schemas.AbstractSchema import AbstractSchema, Model, Schema


class RoutineCommandTextSchema(AbstractSchema):
    def __init__(self, _id: int, text: str, routine_command_id: int):
        self.id = _id
        self.text = text
        self.routine_command_id = routine_command_id

    def to_model(self, **kwargs) -> Schema:
        pass

    @staticmethod
    def from_model(model: Model, **kwargs) -> Schema:
        pass

    def __repr__(self) -> str:
        pass
