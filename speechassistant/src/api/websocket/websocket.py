from fastapi import APIRouter, status
from starlette.websockets import WebSocket

from src.api.Routines.V1.Logic.routine import RoutineLogic
from src.models.routine import Routine

router: APIRouter = APIRouter()


@router.post("/", response_model=Routine, status_code=status.HTTP_201_CREATED)
async def create_routine(routine: Routine):
    return RoutineLogic.create_routine(routine)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text("Lel")