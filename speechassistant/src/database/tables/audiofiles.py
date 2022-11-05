from sqlalchemy import Table, String, LargeBinary, Column

from database.database_persistency import DBPersistency

DB_PERSISTENCY = DBPersistency.get_instance()

AUDIO_FILE_TABLE_NAME = "audiofiles"

audioFileTable = Table(
    AUDIO_FILE_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("name", String),
    Column("data", LargeBinary),
)
