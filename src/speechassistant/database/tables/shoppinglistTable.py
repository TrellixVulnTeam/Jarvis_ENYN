from sqlalchemy import Table, Integer, Column, String, Float, MetaData
from sqlalchemy.future import Engine

meta = MetaData()

SHOPPING_LIST_TABLE_NAME = "shoppinglist"

shoppingListTable = Table(
    SHOPPING_LIST_TABLE_NAME,
    meta,
    Column("id", Integer),
    Column("name", String),
    Column("measure", String),
    Column("quantity", Float),
)


def create_tables(engine: Engine):
    meta.create_all(engine)
