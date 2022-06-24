import os
import pkgutil
from pathlib import Path

from models.module import Module


class ModuleLogic:
    @staticmethod
    def create_module(module: Module) -> Module:
        return None

    @staticmethod
    def read_all_modules() -> list[Module]:
        return None

    @staticmethod
    def read_all_module_names() -> list[str]:
        module_names = []
        module_path = Path(os.path.dirname(__file__)).parents[2].joinpath("modules")
        for finder, name, ispkg in pkgutil.walk_packages([str(module_path)]):
            module_names.append(name)
        return module_names

    @staticmethod
    def read_module_by_name(module_name: str) -> Module:
        return None

    @staticmethod
    def update_module(module_name: str, module: Module) -> Module:
        return None

    @staticmethod
    def delete_module(module_name: str) -> None:
        return None
