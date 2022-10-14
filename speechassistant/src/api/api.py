import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from src.api.Alarms.V1.Controller import alarm
from src.api.AudioFiles.V1.Controller import audioFile
from src.api.Modules.V1.Controller import module
from src.api.Reminder.V1.Controller import reminder
from src.api.Routines.V1.Controller import routine

description: str = """

"""

app = FastAPI(
    title="Jarvis API",
    description=description,
    version="0.0.1",
    contact={"name": "Jakob Priesner", "email": "jakob.priesner@outlook.de"},
)


@app.get("/app")
def read_main(request: Request):
    return {
        "message": "Hello from speech assistant app",
        "root_path": request.scope.get("root_path"),
    }


@app.get("/")
def redirect_to_latest_docs(request: Request):
    return RedirectResponse(request.scope.get("root_path") + "api/latest/docs")


def start() -> None:
    api: FastAPI = FastAPI()

    v1: FastAPI = FastAPI()
    v1.include_router(alarm.router, prefix="/alarms", tags=["Wecker"], dependencies=[])
    v1.include_router(reminder.router, prefix="/reminder", tags=["reminder"], dependencies=[])
    v1.include_router(module.router, prefix="/modules", tags=["modules"], dependencies=[])
    v1.include_router(
        audioFile.router, prefix="/audio-files", tags=["audioFiles"], dependencies=[])
    v1.include_router(
        routine.router, prefix="/routines", tags=["routines"], dependencies=[]
    )

    api.mount(app=v1, path="/v1", name="v1")
    api.mount(app=v1, path="/latest", name="lastest")

    app.mount(app=api, path="/api", name="api")

    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    start()

