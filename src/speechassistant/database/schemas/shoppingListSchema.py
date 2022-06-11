from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class ShoppingList(Base):
    __tablename__ = "shopping_list"

    id = Column(Integer, primary_key=True, sqlite_autoincrement=True)
    name = Column(String)
    measure = Column(String)
    quantity = Column(Float)
