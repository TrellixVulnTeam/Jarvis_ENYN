from pathlib import Path

import toml

from src.speechassistant.core import Core


def __get_config_path() -> Path:
    return Path(__file__).parent.joinpath("src").joinpath("speechassistant").joinpath("config.toml").absolute()


if __name__ == "__main__":
    with open(__get_config_path(), "r") as config_file:
        config_data: dict[str, any] = toml.load(config_file)
    core = Core.get_instance()
