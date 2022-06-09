from fastapi import FastAPI, status

from src.speechassistant.api.logic.routineLogic import RoutineLogic
from src.speechassistant.models.routine import Routine

routine_service: FastAPI = FastAPI()


@routine_service.post("/", response_model=Routine, status_code=status.HTTP_201_CREATED)
async def create_routine(routine: Routine):
    return RoutineLogic.create_routine(routine)


@routine_service.get("/", response_model=list[Routine], status_code=status.HTTP_200_OK)
async def read_all_routines():
    return RoutineLogic.read_all_routines()


@routine_service.get(
    "/{routine_name}", response_model=Routine, status_code=status.HTTP_200_OK
)
async def read_routine_by_name(routine_name: str):
    return RoutineLogic.read_routine_by_name(routine_name)


@routine_service.put(
    "/{routine_name}", response_model=Routine, status_code=status.HTTP_200_OK
)
async def update_routine_by_name(routine_name: str, routine: Routine):
    return RoutineLogic.update_routine_by_name(routine_name, routine)


@routine_service.delete("/{routine_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_routine_by_name(routine_name: str):
    return RoutineLogic.delete_routine_by_name(routine_name)
