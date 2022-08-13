import logging
import os
import pkgutil
import random
import time
import traceback
from threading import Thread

from module_wrapper import ModuleWrapper, ModuleWrapperContinuous
from src.models.user import User
from src.resources import Skills


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

        logging.getLogger().setLevel(logging.INFO)
        from core import Core

        self.core: Core = Core.get_instance()
        self.local_storage: dict = self.core.local_storage
        self.modules: list = []
        self.continuous_modules: list = []

        self.module_wrapper = ModuleWrapper
        self.module_wrapper_continuous = ModuleWrapperContinuous

        self.continuous_stopped: bool = False
        self.continuous_threads_running: int = 0

        Modules.__instance = self

        self.load_modules()

    def load_modules(self) -> None:
        self.local_storage["modules"]: dict = {}
        time.sleep(1)
        logging.info("---------- MODULES...  ----------")
        self.modules: list = self.get_modules("modules")
        if self.modules is []:
            print("[INFO] -- (None present)")
        logging.info("\n----- Continuous MODULES... -----")
        self.continuous_modules: list = self.get_modules(
            "modules/continuous", continuous=True
        )
        if self.continuous_modules is []:
            print("[INFO] -- (None present)")

    def get_modules(self, directory: str, continuous: bool = False) -> list:
        dirname: str = os.path.dirname(os.path.abspath(__file__))
        locations: list = [os.path.join(dirname, directory)]
        modules: list = []
        if "modules" not in self.local_storage:
            self.local_storage["modules"]: dict = {}
        for finder, name, ispkg in pkgutil.walk_packages(locations):
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)
                self.local_storage["modules"][name]: dict = {
                    "name": name,
                    "status": "loaded",
                }
            except Exception:
                # catch only exceptions, that are thrown from loader and finder
                traceback.print_exc()
                self.local_storage["modules"][name]: dict = {
                    "name": name,
                    "status": "error",
                }
                print("[WARNING] Module {} is incorrect and was skipped!".format(name))
                continue
            else:
                if continuous:
                    logging.info("[INFO] Continuous module {} loaded".format(name))
                    modules.append(mod)
                else:
                    logging.info("[INFO] Modul {} loaded".format(name))
                    modules.append(mod)
        modules.sort(
            key=lambda module: module.PRIORITY if hasattr(module, "PRIORITY") else 0,
            reverse=True,
        )
        return modules

    def query_threaded(
            self, name: str, text: str, user: dict, messenger: bool = False
    ) -> bool:
        mod_skill: Skills = self.core.skills
        if text is None:
            # generate a random text
            # text: str = str(random.randint(0, 1000000000))
            analysis: dict = {}
        else:
            # else there is a valid text -> analyze
            try:
                analysis: dict = self.core.analyzer.analyze(str(text))
            except Exception:
                traceback.print_exc()
                logging.warning("[ERROR] Sentence analysis failed!")
                analysis: dict = {}
        if name is not None:
            # Module was called via start_module
            for module in self.modules:
                if module.__name__ == name:
                    self.core.active_modules[
                        str(text)
                    ]: ModuleWrapper = self.module_wrapper(
                        self.core, text, analysis, messenger, user
                    )
                    mt: Thread = Thread(
                        target=self.run_threaded_module, args=(text, module, mod_skill)
                    )
                    mt.daemon = True
                    mt.start()
                    return True
            print("[ERROR] Modul {} could not be found!".format(name))
        elif text is not None:
            # Search the modules normally
            for module in self.modules:
                try:
                    if module.isValid(str(text).lower()):
                        self.core.active_modules[str(text)] = self.module_wrapper(
                            text, analysis, messenger, user
                        )
                        mt: Thread = Thread(
                            target=self.run_threaded_module,
                            args=(text, module, mod_skill),
                        )
                        mt.daemon = True
                        mt.start()
                        return True
                except Exception:
                    traceback.print_exc()
                    print(
                        "[ERROR] Modul {} could not be queried!".format(module.__name__)
                    )
        return False

    def start_continuous(self) -> None:
        self.continuous_threads_running: int = 0
        if not self.continuous_modules == []:
            cct: Thread = Thread(target=self.run_continuous)
            cct.daemon = True
            cct.start()
            self.continuous_threads_running += 1
        else:
            print("[INFO] -- (None present)")
        return

    def start_module(
            self,
            user: User = None,
            text: str = None,
            name: str = None,
            messenger: bool = False,
    ) -> bool:
        mod_skill: Skills = self.core.skills
        analysis: dict = {}
        if text is None:
            text: str = str(random.randint(0, 1000000000))
        else:
            try:
                analysis: dict = self.core.analyzer.analyze(str(text))
                # logging.info('Analysis: ' + str(analysis))
            except Exception:
                traceback.print_exc()
                logging.warning("[WARNING] Sentence analysis failed!")

        if name is not None:
            for module in self.modules:
                if module.__name__ == name:
                    logging.info(
                        "[ACTION] --Modul {} was called directly (Parameter: {})--".format(
                            name, text
                        )
                    )
                    self.core.active_modules[
                        str(text)
                    ]: ModuleWrapper = self.module_wrapper(
                        text, analysis, messenger, user
                    )
                    mt: Thread = Thread(
                        target=self.run_threaded_module, args=(text, module, mod_skill)
                    )
                    mt.daemon = True
                    mt.start()
                    return True
        else:
            try:
                analysis: dict = self.core.analyzer.analyze(str(text))
            except Exception:
                traceback.print_exc()
                print("[ERROR] Sentence analysis failed!")
                analysis: dict = {}
            for module in self.modules:
                try:
                    if module.isValid(text.lower()):
                        self.core.active_modules[
                            str(text)
                        ]: ModuleWrapper = self.module_wrapper(
                            text, analysis, messenger, user
                        )
                        mt: Thread = Thread(
                            target=self.run_threaded_module,
                            args=(text, module, mod_skill),
                        )
                        mt.daemon = True
                        mt.start()
                        mt.join()  # wait until Module is done...
                        self.start_module(user=user, name="wartende_benachrichtigung")
                        return True
                except AttributeError:
                    logging.warning(
                        f"[WARNING] {module.__name__} has no isValid() function!"
                    )
                except Exception:
                    traceback.print_exc()
                    print(
                        "[ERROR] Modul {} could not be queried!".format(module.__name__)
                    )
        return False

    def run_threaded_module(self, text: str, module, mod_skill: Skills) -> None:
        try:
            module.handle(text, self.core.active_modules[str(text)], mod_skill)
        except Exception:
            traceback.print_exc()
            print(
                "[ERROR] Runtime error in module {}. The module was terminated.\n".format(
                    module.__name__
                )
            )
            self.core.active_modules[str(text)].say(
                "Entschuldige, es gab ein Problem mit dem Modul {}.".format(
                    module.__name__
                )
            )
        finally:
            # Maybe a try catch is acquired
            del self.core.active_modules[str(text)]
            return

    def run_module(
            self, text: str, module_wrapper: ModuleWrapper, mod_skill: Skills
    ) -> None:
        for module in self.modules:
            if module.isValid(text):
                module.handle(text, module_wrapper, mod_skill)

    def run_continuous(self) -> None:
        # Runs the continuous_modules. Continuous_modules always run in the background,
        # to wait for events other than voice commands (e.g. sensor values, data etc.).
        self.core.continuous_modules = {}
        for module in self.continuous_modules:
            interval_time: int = module.INTERVALL if hasattr(module, "INTERVAL") else 0
            if __name__ == "__main__":
                self.core.continuous_modules[
                    module.__name__
                ] = self.module_wrapper_continuous(self.core, interval_time, self)
            try:
                module.start(
                    self.core.continuous_modules[module.__name__],
                    self.core.local_storage,
                )
                logging.info("[ACTION] Modul {} started".format(module.__name__))
            except Exception:
                # traceback.print_exc()
                continue
        self.local_storage["module_counter"]: int = 0
        while not self.continuous_stopped:
            for module in self.continuous_modules:
                if (
                        time.time()
                        - self.core.continuous_modules[module.__name__].last_call
                        >= self.core.continuous_modules[module.__name__].intervall_time
                ):
                    self.core.continuous_modules[
                        module.__name__
                    ].last_call = time.time()
                    try:
                        module.run(
                            self.core.continuous_modules[module.__name__],
                            self.core.skills,
                        )
                    except Exception:
                        traceback.print_exc()
                        print(
                            "[ERROR] Runtime-Error in Continuous-Module {}. The module is no longer executed.\n".format(
                                module.__name__
                            )
                        )
                        del self.core.continuous_modules[module.__name__]
                        self.continuous_modules.remove(module)
            self.local_storage["module_counter"] += 1
            time.sleep(0.05)
        self.continuous_threads_running -= 1

    def stop_continuous(self) -> None:
        # Stops the thread in which the continuous_modules are executed at the end of the run.
        # But gives the modules another opportunity to clean up afterwards...
        if self.continuous_threads_running > 0:
            logging.info("------ Modules are terminated...")
            self.continuous_stopped = True
            # Wait until all threads have returned
            while self.continuous_threads_running > 0:
                print("waiting...", end="\r")
                time.sleep(0.05)
            self.continuous_stopped = False
            # Call the stop() function of each module, if present
            no_stopped_modules: bool = True
            for module in self.continuous_modules:
                try:
                    module.stop(
                        self.core.continuous_modules[module.__name__],
                        self.core.local_storage,
                    )
                    logging.info("[ACTION] Modul {} terminated".format(module.__name__))
                    no_stopped_modules = False
                except Exception:
                    continue
            # clean up
            self.core.continuous_modules = {}
            if no_stopped_modules:
                logging.info("-- (None to finish)")
        return
