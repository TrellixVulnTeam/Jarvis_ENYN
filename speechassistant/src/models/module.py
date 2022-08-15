from typing import Callable

from src.api.utils.converter import CamelModel
from .user import User


class Module(CamelModel):
    name: str
    user: User = None
    messenger: bool = False
    text: str = None


class ContinuousModule(CamelModel):
    name: str
    intervall_in_seconds: int = None
    run_function: Callable = None
