from src.core import Core
from src.resources.MyLogger import configure_logging

if __name__ == "__main__":
    configure_logging()

    core = Core.get_instance()
