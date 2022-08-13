import logging
import time
import traceback
from pathlib import Path

import toml

from src import Core


def __get_config_path() -> Path:
    return Path(__file__).parent.joinpath("src").joinpath("speechassistant").joinpath("config.toml").absolute()


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename='speechassistant.log', encoding='utf-8', level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())

    with open(__get_config_path(), "r") as config_file:
        config_data: dict[str, any] = toml.load(config_file)
    core = Core.get_instance()

    while True:
        try:
            time.sleep(10)
        except Exception:
            traceback.print_exc()
            break
