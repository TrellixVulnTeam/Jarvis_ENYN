from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Time, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class BirthdaySchema(Base):
    __tablename__ = "birthday"

    first_name = Column(String, primary_key=True)
    last_name = Column(String, primary_key=True)
    date = Column(DateTime)
