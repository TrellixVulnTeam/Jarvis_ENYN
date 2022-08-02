from sqlalchemy import Table, String, LargeBinary, Column, MetaData
from sqlalchemy.future import Engine

meta = MetaData()

AUDIO_FILE_TABLE_NAME = "audiofiles"

audioFileTable = Table(
    AUDIO_FILE_TABLE_NAME, meta, Column("name", String), Column("data", LargeBinary)
)


def create_tables(engine: Engine):
    meta.create_all(engine)
