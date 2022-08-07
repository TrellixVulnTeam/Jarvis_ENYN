from pathlib import Path

import toml

from src.speechassistant.core import Core

if __name__ == "__main__":
    relPath: str = str(Path(__file__).parent)
    with open(relPath.join("config.toml"), "r") as config_file:
        config_data: dict[str, any] = toml.load(config_file)
    core = Core.get_instance()
