from enum import Enum
from io import BytesIO

from pydantic.main import BaseModel


class QueueType(Enum):
    # lower indices are played earlier,
    # music is played separate.
    EFFECT = 0
    TTS = 1
    NOTIFICATION = 2
    AUDIO = 3
    MUSIC = 4


class AudioQueryType(Enum):
    SONG_NAME: 0
    AUDIO_BYTES: 1


class QueueItem(BaseModel):
    PRIORITY: int = 1
    queue_type: QueueType
    value: str | BytesIO
    wait_until_done: bool
    sample_rate: int = 44100

    class Config:
        arbitrary_types_allowed = True


class MusicQueueItem(QueueItem):
    song_type: AudioQueryType
