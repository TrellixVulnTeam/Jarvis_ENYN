from fastapi import APIRouter, status, HTTPException

from api.logic.alarmLogic import AlarmLogic
from models.alarm import Alarm

router: APIRouter = APIRouter()

APPLICATION_JSON = "application/json"


@router.post(
    "/",
    response_model=Alarm,
    status_code=status.HTTP_201_CREATED,
)
async def create_alarm(alarm: Alarm):
    return AlarmLogic.create_alarm(alarm)


@router.get("/", response_model=list[Alarm], status_code=status.HTTP_200_OK)
async def read_all_alarms():
    return AlarmLogic.read_all_alarms()


@router.get("/{alarm_id}", response_model=Alarm, status_code=status.HTTP_200_OK)
async def read_alarm_by_id(alarm_id: int):
    return AlarmLogic.read_alarm_by_id(alarm_id)


@router.put("/{alarm_id}", response_model=Alarm, status_code=status.HTTP_200_OK)
async def update_alarm(alarm_id: int, alarm: Alarm):
    if alarm_id != alarm.alarm_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Ids doesn't match!",
        )
    return AlarmLogic.update_alarm(alarm)


@router.delete(
    "/{alarm_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_alarm(alarm_id: int):
    return AlarmLogic.delete_alarm(alarm_id)
