import pkgutil
import time
import traceback
from pathlib import Path
from threading import Thread
from typing import TYPE_CHECKING

from src import log
from src.models import User, ContinuousModule
from .wrapper import ModuleWrapper
from .continuous import ContinuousModuleHandler

if TYPE_CHECKING:
    from src.core import Core


class Modules:
    __instance = None

    @staticmethod
    def get_instance():
        if Modules.__instance is None:
            Modules()
        return Modules.__instance

    def __init__(self) -> None:
        if Modules.__instance is not None:
            raise Exception("Singleton cannot be instantiated more than once!")

        log.getLogger().setLevel(log.INFO)

        self.core: Core = Core.get_instance()
        self.local_storage: dict = self.core.local_storage
        self.modules: list = []
        self.continuous_modules: list = []

        self.continuous_stopped: bool = False
        self.continuous_threads_counter: int = 0
        self.continuous_handler: ContinuousModuleHandler = ContinuousModuleHandler(self)
        self.module_threads_counter: int = 0

        Modules.__instance = self

        self.load_modules()

    def load_modules(self) -> None:
        self.local_storage["modules"]: dict = {}
        time.sleep(1)
        log.info("---------- MODULES...  ----------")
        self.modules: list = self.get_modules(self.__get_modules_impl_path())
        if self.modules is []:
            log.info("-- (None present)")
        log.info("\n----- Continuous MODULES... -----")
        self.continuous_modules: list = self.get_modules(self.__get_continuous_impl_path(), continuous=True)
        if self.continuous_modules is []:
            log.info("-- (None present)")

    def get_modules(self, directory: Path, continuous: bool = False) -> list:
        modules: list = []

        self.__load_all_modules(continuous, directory, modules)

        modules.sort(
            key=lambda module: module.PRIORITY if hasattr(module, "PRIORITY") else 0,
            reverse=True,
        )
        return modules

    def __load_all_modules(self, continuous, directory, modules):
        for finder, name, ispkg in pkgutil.walk_packages(self.__path_with_impl(directory)):
            log.debug(f"Processing Module with name \"{name}\"")
            try:
                mod = self.__load_one_module(finder, name)
            except Exception as e:
                log.exception(e)
                # TODO: catch only exceptions, that are thrown from loader and finder
                self.__handle_loading_error(name)
                continue
            else:
                self.__log_module_status(continuous, name)
                modules.append(mod)

    def __load_one_module(self, finder, name):
        loader = finder.find_module(name)
        mod = loader.load_module(name)
        self.local_storage["modules"][name]: dict = {
            "name": name,
            "status": "loaded",
        }
        return mod

    def __handle_loading_error(self, name):
        log.debug(traceback.print_exc())
        self.local_storage["modules"][name]: dict = {
            "name": name,
            "status": "error",
        }
        log.warning(f"Module {name} is incorrect and was skipped!")

    @staticmethod
    def __log_module_status(continuous, name):
        if continuous:
            log.info("Continuous module {} loaded".format(name))
        else:
            log.info("Modul {} loaded".format(name))

    @staticmethod
    def __path_with_impl(path: Path) -> str:
        return str(path.joinpath("impl"))

    def query_threaded(self, name: str, text: str, user: User, messenger: bool = False) -> bool:
        analysis = self.__get_text_analysis(text)

        if name is not None:
            return self.__start_module(analysis, messenger, name, text, user)
        elif text is not None:
            return self.__find_matching_module(analysis, messenger, text, user) is not None

        return False

    def __find_matching_module(self, analysis, messenger, text, user) -> Thread | None:
        for module in self.modules:
            try:
                if module.is_valid(str(text).lower()):
                    self.core.active_modules[str(text)] = ModuleWrapper(
                        text, analysis, messenger, user, self.core)
                    return self.__start_module_in_new_thread(module, text)
            except AttributeError:
                log.warning(f"Module {module.__name__} has no is_valid() function!")
            except Exception as e:
                log.exception(e)
                log.warning(f"Module {module.__name__} could not be queried!")

    def __start_module(self, analysis, messenger, name, text, user):
        module = next((x for x in self.modules if x.__name__ == name), None)
        if not module:
            log.error(f"Modul {name} could not be found!")
            return False
        self.core.active_modules[str(text)] = ModuleWrapper(text, analysis, messenger, user, self.core)
        self.__start_module_in_new_thread(module, text)
        return True

    def __get_text_analysis(self, text) -> dict:
        if text:
            try:
                return self.core.analyzer.analyze(str(text))
            except Exception as e:
                log.exception(e)
                log.warning("Sentence analysis failed!")
        return {}

    def __start_module_in_new_thread(self, module, text) -> Thread:
        mt: Thread = Thread(target=self.run_threaded_module, args=(text, module))
        mt.daemon = True
        mt.start()
        log.debug(f"Module {module.__name__} started...")
        return mt

    def start_continuous(self) -> None:
        if not self.continuous_modules == []:
            self.__start_all_continuous_modules()
        else:
            log.info("-- (None present)")

    def start_module(
            self,
            user: User = None,
            text: str = None,
            name: str = None,
            messenger: bool = False,
    ) -> bool:
        analysis: dict = self.__get_text_analysis(text)

        if name is not None:
            if not self.__start_module(analysis, messenger, name, text, user):
                return False
            log.info(f"--Modul {name} was called directly (Parameter: {text})--")
        else:
            thread: Thread = self.__find_matching_module(analysis, messenger, text, user)
            if not thread:
                return False
            self.start_module(user=user, name="wartende_benachrichtigung")
            return True

    def run_threaded_module(self, text: str, module) -> None:
        try:
            module.handle(text, self.core.active_modules[str(text)])
        except Exception as e:
            log.error(f"Runtime error in module {module.__name__}. The module was terminated.\n")
            log.exception(e)
            self.core.active_modules[str(text)].say(
                f"Entschuldige, es gab ein Problem mit dem Modul {module.__name__}.")
        finally:
            del self.core.active_modules[str(text)]

    def run_module(self, text: str, module_wrapper: ModuleWrapper) -> None:
        for module in self.modules:
            if module.is_valid(text):
                module.handle(text, module_wrapper)

    def run_continuous(self) -> None:
        # Runs the continuous_modules. Continuous_modules always run in the background,
        # to wait for events other than voice commands (e.g. sensor values, data etc.).
        self.core.continuous_modules = {}

        self.__start_all_continuous_modules()

    def __start_all_continuous_modules(self):
        for module in self.continuous_modules:
            continuous_module: ContinuousModule = ContinuousModule(
                name=module.__name__,
                interval_time=module.INTERVALL if hasattr(module, "INTERVAL") else 0,
                run_function=module.handle
            )
            self.continuous_handler.subscribe(continuous_module)

    def stop_continuous(self) -> None:
        self.continuous_handler.stop_all()

    @staticmethod
    def __get_modules_impl_path() -> Path:
        return Path(__file__).parent.joinpath("on_call")

    @staticmethod
    def __get_continuous_impl_path() -> Path:
        return Path(__file__).parent.joinpath("continuous")

    def __repr__(self) -> str:
        # todo
        return str.join(",", [module.__name__ for module in self.modules])
