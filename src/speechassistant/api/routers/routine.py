from fastapi import APIRouter, status

from src.speechassistant.api.logic.routineLogic import RoutineLogic
from src.speechassistant.models.routine import Routine

router: APIRouter = APIRouter()


@router.post("/", response_model=Routine, status_code=status.HTTP_201_CREATED)
async def create_routine(routine: Routine):
    return RoutineLogic.create_routine(routine)


@router.get("/", response_model=list[Routine], status_code=status.HTTP_200_OK)
async def read_all_routines():
    return RoutineLogic.read_all_routines()


@router.get(
    "/{routine_name}", response_model=Routine, status_code=status.HTTP_200_OK
)
async def read_routine_by_name(routine_name: str):
    return RoutineLogic.read_routine_by_name(routine_name)


@router.put(
    "/{routine_name}", response_model=Routine, status_code=status.HTTP_200_OK
)
async def update_routine_by_name(routine_name: str, routine: Routine):
    return RoutineLogic.update_routine_by_name(routine_name, routine)


@router.delete("/{routine_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_routine_by_name(routine_name: str):
    return RoutineLogic.delete_routine_by_name(routine_name)
