from sqlalchemy import Table, Integer, Column, String, Float

from src.database.orm.database_persistency import OrmPersistency

DB_PERSISTENCY = OrmPersistency.get_instance()

SHOPPING_LIST_TABLE_NAME = "shoppinglist"

shoppingListTable = Table(
    SHOPPING_LIST_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("id", Integer),
    Column("name", String),
    Column("measure", String),
    Column("quantity", Float),
)
