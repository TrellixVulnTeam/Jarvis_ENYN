from typing import Type

from src.database.connection.abstract_database_connection import (
    Schema,
    Model,
    AbstractDataBaseConnection,
)
from src.database.schemas.shopping_list import (
    ShoppingListSchema,
    shopping_list_to_schema,
    schema_to_shopping_list,
)
from src.models.shopping_list import ShoppingListItem


class ShoppingListInterface(
    AbstractDataBaseConnection[ShoppingListItem, ShoppingListSchema]
):
    @staticmethod
    def _schema_to_model(model_schema: Schema) -> Model:
        return schema_to_shopping_list(model_schema)

    @staticmethod
    def _model_to_schema(model: Model) -> Schema:
        return shopping_list_to_schema(model)

    @staticmethod
    def _get_model_id(model: ShoppingListItem) -> int:
        return model.id

    @staticmethod
    def _get_model_type() -> Type[Model]:
        return ShoppingListItem

    @staticmethod
    def _get_schema_type() -> Type[Schema]:
        return ShoppingListSchema

    def __int__(self) -> None:
        super().__init__()
