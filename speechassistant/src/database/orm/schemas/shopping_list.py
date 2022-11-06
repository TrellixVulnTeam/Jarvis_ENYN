from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

from src.models.shopping_list import ShoppingListItem

Base = declarative_base()


class ShoppingListSchema(Base):
    __tablename__ = "shoppinglist"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    measure = Column(String)
    quantity = Column(Float)


def shopping_list_to_schema(model: ShoppingListItem) -> ShoppingListSchema:
    return ShoppingListSchema(
        id=model.id,
        name=model.name,
        measure=model.measure,
        quantity=model.quantity
    )


def schema_to_shopping_list(schema: ShoppingListSchema) -> ShoppingListItem:
    return ShoppingListSchema(
        id=schema.id,
        name=schema.name,
        measure=schema.measure,
        quantity=schema.quantity
    )
