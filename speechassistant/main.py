import logging
import time
import traceback

from src.core import Core


def configure_logging():
    logging.basicConfig(
        format="%(asctime)-30s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        filename="speech-assistant.log",
        encoding="utf-8",
        level=logging.DEBUG,
    )
    logging.getLogger().addHandler(logging.StreamHandler())
    file_logger = logging.FileHandler("speech-assistant.log")
    file_logger.setLevel(logging.DEBUG)
    file_logger_formatting = logging.Formatter("%(asctime)-30s %(threadName)-12s %(levelname)-8s %(message)s")
    file_logger.setFormatter(file_logger_formatting)
    logging.getLogger().addHandler(file_logger)


if __name__ == "__main__":
    configure_logging()

    core = Core.get_instance()

    while True:
        try:
            time.sleep(10)
        except Exception:
            traceback.print_exc()
            break
