from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ShoppingList(Base):
    __tablename__ = "shoppinglist"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    measure = Column(String)
    quantity = Column(Float)
