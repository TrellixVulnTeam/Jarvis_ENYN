import logging
import time
import traceback

from src.core import Core

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        filename="speechassistant.log",
        encoding="utf-8",
        level=logging.DEBUG,
    )
    logging.getLogger().addHandler(logging.StreamHandler())

    core = Core.get_instance()

    while True:
        try:
            time.sleep(10)
        except Exception:
            traceback.print_exc()
            break
