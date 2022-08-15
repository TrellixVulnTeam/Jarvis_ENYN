import logging
import time
import traceback
from threading import Thread

from src.models import ContinuousModule
from src.modules import Modules
from src.modules.continuous import ContinuousModuleHandler


class ObserverItem:
    def __init__(self, handler: ContinuousModuleHandler, timeout_in_seconds: int):
        self.module_list: list[ContinuousModule] = []
        self.__handler: ContinuousModuleHandler = handler
        self.__timeout = timeout_in_seconds
        self.__modules: Modules = handler.modules
        self.__core = self.__modules.core
        self.__start()

    def __start(self) -> None:
        thread: Thread = Thread(target=self.__run, args=())
        thread.daemon = True
        thread.start()

    def __run(self) -> None:
        while self.__handler.active:
            self.__start_all_modules()
            time.sleep(self.__timeout)

    def __start_all_modules(self):
        for module in self.module_list:
            if __name__ == "__main__":
                self.__create_module_wrapper(module)
            try:
                self.__handler.running_counter += 1
                module.run_function(self.__core.continuous_modules[module.name],
                                    self.__core.local_storage, )
                self.__handler.running_counter -= 1
                logging.debug(f"[ACTION] Module {module.name} started")
            except Exception:
                self.__handle_error(module)

    def __handle_error(self, module):
        logging.debug(traceback.print_exc())
        logging.info(
            f"[ERROR] Runtime-Error in Continuous-Module {module.name}. The module is no longer executed.\n")
        del self.__core.continuous_modules[module.name]
        self.__modules.continuous_modules.remove(module)

    def __create_module_wrapper(self, module: ContinuousModule):
        self.__core.continuous_modules[module.name] = self.__modules.module_wrapper_continuous(
            self.__core, module.intervall_in_seconds, self.__modules)
