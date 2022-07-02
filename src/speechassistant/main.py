import json
from pathlib import Path

from core import Core

if __name__ == "__main__":
    relPath: str = str(Path(__file__).parent) + "/"
    with open(relPath + "config.json", "r") as config_file:
        config_data: dict = json.load(config_file)
    with open(relPath + "resources/alias/correct_output.json", "r") as correct_output:
        # don't log loading file, because it is a config too
        config_data["correct_output"]: dict = json.load(correct_output)
    core = Core.get_instance()
