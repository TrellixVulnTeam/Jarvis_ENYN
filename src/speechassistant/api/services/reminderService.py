from fastapi import FastAPI, status

from src.speechassistant.api.logic.reminderLogic import ReminderLogic
from src.speechassistant.models.reminder import Reminder

reminder_service: FastAPI = FastAPI()


@reminder_service.post(
    "/", response_model=Reminder, status_code=status.HTTP_201_CREATED
)
async def create_reminder(reminder: Reminder):
    return ReminderLogic.create_reminder(reminder)


@reminder_service.get(
    "/", response_model=list[Reminder], status_code=status.HTTP_200_OK
)
async def read_all_reminder(passed: bool = False):
    if passed:
        return ReminderLogic.read_passed_reminder()
    else:
        return ReminderLogic.read_all_reminder()


@reminder_service.get(
    "/{reminder_id}", response_model=Reminder, status_code=status.HTTP_200_OK
)
async def read_reminder_by_id(reminder_id: int):
    return ReminderLogic.read_reminder_by_id(reminder_id)


@reminder_service.delete(
    "/{reminder_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_reminder_by_id(reminder_id: int):
    ReminderLogic.delete_reminder(reminder_id)
