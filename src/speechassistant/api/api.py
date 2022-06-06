import uvicorn
from fastapi import FastAPI, Request

from src.speechassistant.api.services.alarmService import alarm_service
from src.speechassistant.api.services.audioFileService import audio_file_service
from src.speechassistant.api.services.moduleService import module_service
from src.speechassistant.api.services.reminderService import reminder_service

app = FastAPI()


@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}


@app.get("/")
def test():
    return {"Success": "nice"}


def start() -> None:
    app.mount("/alarms", alarm_service)
    app.mount("/reminder", reminder_service)
    app.mount("/modules", module_service)
    app.mount("/audioFiles", audio_file_service)


if __name__ == "__main__":
    start()
    uvicorn.run(app, host="0.0.0.0", port=8080)
