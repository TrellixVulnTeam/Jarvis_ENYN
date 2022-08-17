from src import log
from src.core import Core

if __name__ == "__main__":
    log.configure_log()

    core = Core.get_instance()
