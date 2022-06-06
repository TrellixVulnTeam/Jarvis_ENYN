from fastapi import FastAPI, status, HTTPException

from src.speechassistant.api.logic.alarmLogic import AlarmLogic
from src.speechassistant.models.alarm import Alarm

alarm_service: FastAPI = FastAPI()

APPLICATION_JSON = "application/json"


@alarm_service.post(
    "/",
    response_model=Alarm,
    status_code=status.HTTP_201_CREATED,
)
async def create_alarm(alarm: Alarm):
    return AlarmLogic.create_alarm(alarm)


@alarm_service.get("/", response_model=list[Alarm], status_code=status.HTTP_200_OK)
async def read_all_alarms():
    return AlarmLogic.read_all_alarms()


@alarm_service.get("/{alarm_id}", response_model=Alarm, status_code=status.HTTP_200_OK)
async def read_alarm_by_id(alarm_id: int):
    return AlarmLogic.read_alarm_by_id(alarm_id)


@alarm_service.put("/{alarm_id}", response_model=Alarm, status_code=status.HTTP_200_OK)
async def update_alarm(alarm_id: int, alarm: Alarm):
    if alarm_id != alarm.alarm_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Ids doesn't match!",
        )
    return AlarmLogic.update_alarm(alarm)


@alarm_service.delete(
    "/{alarm_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_alarm(alarm_id: int):
    return AlarmLogic.delete_alarm(alarm_id)
