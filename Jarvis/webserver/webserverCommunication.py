import json
import os
import sys
from threading import Thread

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import main


class mThr():
    """
    the mThr-Class wraps around the main JARVIS-Server. JARVIS is started in a
    seperate Process and not a Thread - so you can kill them without modifying
    the JARVIS-Part. The communication runs via two memory-maps which can be
    accessed by both processes.
    """

    def __init__(self):
        self.thr = None
        self.core = main
        with open("../config.json", "r") as config_file:
            self.config_data = json.load(config_file)

    def start(self):
        self.thr = Thread(target=self.core.start(self.config_data))
        self.thr.start()

    def stop(self):
        self.core.stop(self.core.LUNA.local_storage, self.core.config_data)

    def status(self):
        if self.thr is not None:
            data = "running" if self.thr.is_alive() else "stopped"
        else:
            data = "unknown"
        return data

    def getFeed(self):
        return self.config_data
