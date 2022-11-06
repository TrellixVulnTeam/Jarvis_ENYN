from .alarms import ALARM_TABLE_NAME, ALARM_REPEATING_TABLE_NAME
from .audiofiles import AUDIO_FILE_TABLE_NAME
from .birthdays import BIRTHDAY_TABLE_NAME
from .reminder import REMINDER_TABLE_NAME
from .routines import *
from .shoppinglist import SHOPPING_LIST_TABLE_NAME
from .timer import TIMER_TABLE_NAME
from .users import USER_TABLE_NAME

DBPersistency.get_instance().meta.create_all()
