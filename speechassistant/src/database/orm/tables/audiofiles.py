from sqlalchemy import Table, String, LargeBinary, Column

from src.database.orm.database_persistency import OrmPersistency

DB_PERSISTENCY = OrmPersistency.get_instance()

AUDIO_FILE_TABLE_NAME = "audiofiles"

audioFileTable = Table(
    AUDIO_FILE_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("name", String),
    Column("data", LargeBinary),
)
