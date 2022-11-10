from database.sql.schemas.AbstractSchema import AbstractSchema, Model, Schema
from models import RoutineCommand


class RoutineCommandSchema(AbstractSchema):
    def __init__(self, _id: int, module_name: str, routine_name: str):
        self.id = _id
        self.module_name = module_name
        self.routine_name = routine_name

    def to_model(
        self, schema: "RoutineCommandSchema", with_text: list[any]
    ) -> RoutineCommand:
        return RoutineCommand(
            module_name=schema.module_name, with_text=with_text, cid=schema.id
        )

    @staticmethod
    def from_model(model: Model, **kwargs) -> Schema:
        pass

    def __repr__(self) -> str:
        pass
