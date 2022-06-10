import uvicorn
from fastapi import FastAPI, Request
from fastapi.routing import APIRoute, APIRouter

from src.speechassistant.api.routers import alarm, audioFile, module, reminder, routine

app = FastAPI()


@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}


@app.get("/")
def test():
    return {"Success": "nice"}


def start() -> None:
    api: FastAPI = FastAPI()

    v1: FastAPI = FastAPI()
    v1.include_router(alarm.router, prefix="/alarms", tags=["Wecker"], dependencies=[])
    v1.include_router(reminder.router, prefix="/reminder", tags=["reminder"], dependencies=[])
    v1.include_router(module.router, prefix="/modules", tags=["modules"], dependencies=[])
    v1.include_router(audioFile.router, prefix="/audioFiles", tags=["audioFiles"], dependencies=[])
    v1.include_router(routine.router, prefix="/routines", tags=["routines"], dependencies=[])

    api.mount(app=v1, path="/v1", name="v1")

    app.mount(app=api, path="/api", name="api")


if __name__ == "__main__":
    start()
    uvicorn.run(app, host="0.0.0.0", port=8080)
