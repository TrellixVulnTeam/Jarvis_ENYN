from __future__ import annotations  # compatibility for < 3.10

import json

from src import log
from src.resources.intent.ai import GenericAssistant


class IntentWrapper:
    def __init__(self, path="/resources/intent") -> None:
        from core import Core

        self.core = Core.get_instance()
        # with open(core.path + "/resources/intent/mappings.json", 'r') as mapping_file:
        with open(self.core.path + path + "/mappings.json", "r") as mapping_file:
            mappings = json.loads(mapping_file.read())
            # toDo: i think intents.json should be mappings
            self.ai = GenericAssistant(
                "intents.json",
                self.core.path + "/resources/intent/",
                intent_methods=mappings,
            )
            try:
                self.ai.load_model()
                log.info("[SUCCESS] Model loaded successfully")
            except FileNotFoundError:
                log.warning("Could not find a model for AI. Disable AI-function...")
                self.core.use_ai = False
                log.info("AI-function disabled.")
                return

        log.info("AI initialized successfully!")

    def proceed_with_user_input(self, user_input: str) -> dict | str:
        return self.ai.request(user_input)

    def test_module(self, user_input: str) -> dict | str:
        response: dict | str = self.ai.test_request(user_input)
        if type(response) is str:
            return response
        elif type(response) is dict:
            return response["intent"]

    def train_model(self) -> None:
        log.action("Start with training model for AI...")
        self.ai.train_model(5000)
        log.info("Training of AI done!")
        self.ai.save_model()
        self.ai.load_model()

    def test_model(self):
        with open("validation_data.json", "r", encoding="UTF-8") as file:
            validation_data = json.load(file)
            for item in validation_data["validation"].keys():
                try:
                    response = self.test_module(item)
                except Exception:
                    print(f"No entry for {item}")
                if response is None:
                    print(f"Couldn't find a matching value for {item}")
                elif (
                        type(response) is str
                        and response != validation_data["validation"][item]
                ):
                    print(f'Got wrong response for "{item}": {response}')
                # else:
                #    print(f'{item} worked...')


if __name__ == "__main__":

    class Core:
        def __init__(self) -> None:
            self.path: str = (
                "C:\\Users\\Jakob\\PycharmProjects\\Jarvis\\src\\speechassistant"
            )
            self.audio_output = Audio()


    class Audio:
        def __init__(self):
            pass

        def say(self, text):
            print(text)


    iw = IntentWrapper(path="\\resources\\intent")
    iw.train_model()
    iw.test_model()

    while True:
        print("Enter something")
        print(iw.proceed_with_user_input(input()))
