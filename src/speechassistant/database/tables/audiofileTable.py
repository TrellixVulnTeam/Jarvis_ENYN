from sqlalchemy import Table, String, LargeBinary, Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()

AUDIO_FILE_TABLE_NAME = "audiofiles"

audioFileTable = Table(
    AUDIO_FILE_TABLE_NAME,
    Base.metadata,
    Column("name", String),
    Column("data", LargeBinary)
)