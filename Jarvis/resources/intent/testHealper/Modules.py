import logging
import os
import pkgutil
import random
import time
import traceback
from threading import Thread

from Modulewrapper import Test_Modulewrapper as Modulewrapper


class Test_Modules:
    def __init__(self, core, local_storage):
        logging.getLogger().setLevel(logging.INFO)
        self.core = core
        self.local_storage = local_storage
        self.modules = []
        self.continuous_modules = []

        self.module_wrapper = Modulewrapper

        self.continuous_stopped = False
        self.continuous_threads_running = 0

        self.load_modules()

    def load_modules(self):
        self.local_storage["modules"] = {}
        time.sleep(1)
        print('---------- MODULES...  ----------')
        self.modules = self.get_modules('modules')
        if self.modules is []:
            print('[INFO] -- (None present)')
        print('\n----- Continuous MODULES... -----')
        self.continuous_modules = self.get_modules('modules/continuous', continuous=True)
        if self.continuous_modules is []:
            print('[INFO] -- (None present)')

    def get_modules(self, directory, continuous=False):
        dirname = os.path.dirname(os.path.abspath(__file__))
        locations = [os.path.join(dirname, directory)]
        modules = []
        if "modules" not in self.local_storage:
            self.local_storage["modules"] = {}
        for finder, name, ispkg in pkgutil.walk_packages(locations):
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)
                self.local_storage["modules"][name] = {"name": name, "status": "loaded"}
            except:
                traceback.print_exc()
                self.local_storage["modules"][name] = {"name": name, "status": "error"}
                print('[WARNING] Modul {} is incorrect and was skipped!'.format(name))
                continue
            else:
                if continuous:
                    print('[INFO] Continuous module {} loaded'.format(name))
                    modules.append(mod)
                else:
                    print('[INFO] Modul {} loaded'.format(name))
                    modules.append(mod)
        modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY') else 0, reverse=True)
        return modules

    def query_threaded(self, name, text, user, messenger=False):
        mod_skill = self.core.skills
        if text is None:
            # generate a random text
            text = random.randint(0, 1000000000)
            analysis = {}
        else:
            # else there is a valid text -> analyze
            try:
                analysis = self.core.analyzer.analyze(str(text))
            except:
                traceback.print_exc()
                print('[ERROR] Sentence analysis failed!')
                analysis = {}
        if name is not None:
            # Module was called via start_module
            for module in self.modules:
                if module.__name__ == name:
                    self.core.active_modules[str(text)] = self.module_wrapper(self.core, text, analysis, messenger, user)
                    mt = Thread(target=self.run_threaded_module, args=(text, module, mod_skill))
                    mt.daemon = True
                    mt.start()
                    return True
            print('[ERROR] Modul {} could not be found!'.format(name))
        elif text is not None:
            # Search the modules normally
            for module in self.modules:
                try:
                    if module.isValid(str(text).lower()):
                        self.core.active_modules[str(text)] = self.module_wrapper(self.core, text, analysis, messenger,
                                                                                  user)
                        mt = Thread(target=self.run_threaded_module, args=(text, module, mod_skill))
                        mt.daemon = True
                        mt.start()
                        return True
                except:
                    traceback.print_exc()
                    print('[ERROR] Modul {} could not be queried!'.format(module.__name__))
        return False

    def start_module(self, user=None, text=None, name=None, messenger=False):
        # self.query_threaded(name, text, direct, messenger=messenger)
        mod_skill = self.core.skills
        analysis = {}
        if text is None:
            text = str(random.randint(0, 1000000000))
        else:
            try:
                analysis = self.core.analyzer.analyze(str(text))
                # logging.info('Analysis: ' + str(analysis))
            except:
                traceback.print_exc()
                logging.warning('[WARNING] Sentence analysis failed!', conv_id=str(text))

        if name is not None:
            for module in self.modules:
                if module.__name__ == name:
                    logging.info('[ACTION] --Modul {} was called directly (Parameter: {})--'.format(name, text))
                    self.core.active_modules[str(text)] = self.module_wrapper(self.core, text, analysis, messenger,
                                                                              user)
                    mt = Thread(target=self.run_threaded_module, args=(text, module, mod_skill))
                    mt.daemon = True
                    mt.start()
                    break
        else:
            try:
                analysis = self.core.analyzer.analyze(str(text))
            except:
                traceback.print_exc()
                print('[ERROR] Sentence analysis failed!')
                analysis = {}
            for module in self.modules:
                try:
                    if module.isValid(text.lower()):
                        self.core.active_modules[str(text)] = self.module_wrapper(self.core, text, analysis, messenger,
                                                                                  user)
                        mt = Thread(target=self.run_threaded_module, args=(text, module, mod_skill))
                        mt.daemon = True
                        mt.start()
                        mt.join()  # wait until Module is done...
                        self.start_module(user=user, name='wartende_benachrichtigung')
                        break
                except:
                    traceback.print_exc()
                    print('[ERROR] Modul {} could not be queried!'.format(module.__name__))
        return False

    def run_threaded_module(self, text, module, mod_skill):
        try:
            module.handle(text, self.core.active_modules[str(text)], mod_skill)
        except:
            traceback.print_exc()
            print('[ERROR] Runtime error in module {}. The module was terminated.\n'.format(module.__name__))
            self.core.active_modules[str(text)].say(
                'Entschuldige, es gab ein Problem mit dem Modul {}.'.format(module.__name__))
        finally:
            try:
                del self.core.active_modules[str(text)]

            except:
                pass
            return

    def run_module(self, text, module_wrapper, mod_skill):
        for module in self.modules:
            if module.isValid(text):
                module.handle(text, module_wrapper, mod_skill)