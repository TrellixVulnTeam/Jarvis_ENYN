from fastapi import APIRouter, status

from src.api.Reminder.V1.Logic.reminder import ReminderLogic
from src.models.reminder import Reminder

router: APIRouter = APIRouter()


@router.post("/", response_model=Reminder, status_code=status.HTTP_201_CREATED)
async def create_reminder(reminder: Reminder):
    return ReminderLogic.create_reminder(reminder)


@router.get("/", response_model=list[Reminder], status_code=status.HTTP_200_OK)
async def read_all_reminder(passed: bool = False):
    if passed:
        return ReminderLogic.read_passed_reminder()
    else:
        return ReminderLogic.read_all_reminder()


@router.get("/{reminder_id}", response_model=Reminder, status_code=status.HTTP_200_OK)
async def read_reminder_by_id(reminder_id: int):
    return ReminderLogic.read_reminder_by_id(reminder_id)


@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reminder_by_id(reminder_id: int):
    ReminderLogic.delete_reminder(reminder_id)
