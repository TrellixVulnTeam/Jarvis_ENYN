from datetime import datetime

from sqlalchemy.orm import declarative_base

from src.api.utils.converter import CamelModel
from src.enums import OutputTypes
from src.modules import skills

Base = declarative_base()


class Reminder(CamelModel):
    time: datetime
    text: str
    user_id: int
    reminder_id: int

    """def to_json(self) -> dict:
        return {
            "reminderId": self.rid,
            "time": self.time.isoformat(),
            "text": self.text,
            "user": self.user.to_json(),
        }"""


def __get_reminder_text(text: str) -> str:
    intent: str = __get_intent(text)

    intent = intent.replace("ich", "du")
    intent = intent.replace("mich", "dich")

    return intent


def __get_intent(text: str) -> str:
    if " zu " in text:
        return skills.get_text_between("zu", text, output=OutputTypes.STRING)
    elif "dass" in text:
        return skills.get_text_between("dass", text, output=OutputTypes.STRING)
    elif " ans" in text:
        return skills.get_text_between("ans", text, output=OutputTypes.STRING)
    else:
        return __get_intent_with_unknown_start_word(text)


def __get_intent_with_unknown_start_word(text: str) -> str:
    pass
