from sqlalchemy import Column, Integer, String, Float

from src.speechassistant.database.DataBasePersistency import DBPersistency

Base = DBPersistency.Base


class ShoppingList(Base):
    __tablename__ = "shoppinglist"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    measure = Column(String)
    quantity = Column(Float)
