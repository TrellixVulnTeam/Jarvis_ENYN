import json
from pathlib import Path

import core

if __name__ == "__main__":
    relPath = str(Path(__file__).parent) + "/"
    with open(relPath + "config.json", "r") as config_file:
        config_data = json.load(config_file)
    with open(relPath + "resources/alias/correct_output.json", "r") as correct_output:
        # dont log loading file, because it is a config too
        config_data["correct_output"] = json.load(correct_output)
    webThr = None
    core.relPath = relPath
    core.config_data = config_data
    core.start(config_data)
