from sqlalchemy import Table, Integer, Column, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

SHOPPING_LIST_TABLE_NAME = "shoppinglist"

shoppingListTable = Table(
    SHOPPING_LIST_TABLE_NAME,
    Base.metadata,
    Column("id", Integer),
    Column("name", String),
    Column("measure", String),
    Column("quantity", Float)
)
