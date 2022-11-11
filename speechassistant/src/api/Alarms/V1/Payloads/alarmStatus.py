from src.api.utils import CamelModel


class AlarmStatus(CamelModel):
    status: bool
