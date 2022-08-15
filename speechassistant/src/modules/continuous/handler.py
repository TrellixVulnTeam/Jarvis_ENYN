import logging
import time

from src.models import ContinuousModule
from src.modules import Modules
from src.modules.continuous.observer import ObserverItem


class ContinuousModuleHandler:
    def __init__(self, modules: Modules) -> None:
        self.observer: dict[int, ObserverItem] = {}
        self.modules = modules
        self.counter: int = 0
        self.running_counter: int = 0
        self.active: bool = True

    def subscribe(self, module: ContinuousModule) -> None:
        if module.intervall_in_seconds in self.observer.keys():
            self.observer[module.intervall_in_seconds] = ObserverItem(self, module.intervall_in_seconds)
        self.observer[module.intervall_in_seconds].module_list.append(module)
        self.counter += 1

    def stop_all(self) -> None:
        self.active = False
        if self.counter > 0:
            logging.info("[ACTION] ------ Modules are terminated...")
            [observer.stop() for observer in self.observer.values()]
            while self.running_counter > 0:
                time.sleep(0.05)
            logging.info("[INFO] Continuous Modules stopped!")

        else:
            logging.info("-- (None to finish)")
