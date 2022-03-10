from __future__ import annotations      # compatibility for < 3.10

import json
import logging

# from src.speechassistant.core import Core
import traceback

from src.speechassistant.resources.intent.AI import GenericAssistant


class IntentWrapper:
    def __init__(self, core, path='/resources/intent') -> None:
        self.core = core
        # with open(core.path + "/resources/intent/mappings.json", 'r') as mapping_file:
        with open(core.path + path + '/mappings.json', 'r') as mapping_file:
            mappings = json.loads(mapping_file.read())
            self.ai = GenericAssistant('intents.json', core.path + '/resources/intent/', intent_methods=mappings)
            try:
                self.ai.load_model()
                logging.info("Model loaded successfully")
                print("try done")
            except FileNotFoundError as e:
                logging.info("Couldn't find a model, so train a new one... ")
                self.core.audio_output.say(
                    "Meine Inteligenz wurde leider noch nicht trainiert. Ich werde das schnell erledigen, habe bitte etwas Geduld! Dieser Vorgang dauert etwa 3 Stunden.")
                self.ai.train_model(7500)
                logging.info("Model trained successfully")
                self.ai.save_model()
                logging.info("Model saved sucessfully")
                try:
                    self.ai.load_model()
                    logging.info("Model loaded successfully")
                except:
                    logging.critical("Fatal error in AI: Couldn't load model!")
        logging.info("AI initialized successfully!")

    def proceed_with_user_input(self, user_input: str) -> dict | str:
        return self.ai.request(user_input)

    def test_module(self, user_input: str) -> dict | str:
        response: dict | str = self.ai.test_request(user_input)
        if type(response) is type(""):
            return response
        elif type(response) is type({}):
            return response["intent"]

    def train_model(self) -> None:
        logging.info("Start training model")
        self.ai.train_model(1000)
        logging.info("Training done")
        self.ai.save_model()
        self.ai.load_model()

    def test_model(self):
        with open('validation_data.json', 'r', encoding='UTF-8') as file:
            validation_data = json.load(file)
            for item in validation_data["validation"].keys():
                try:
                    response = self.test_module(item)
                except Exception:
                    print(f'No entry for {item}')
                if response is None:
                    print(f'Couldn\'t find a matching value for {item}')
                elif type(response) is str and response != validation_data["validation"][item]:
                    print(f'Got wrong response for "{item}": {response}')
                #else:
                #    print(f'{item} worked...')

if __name__ == "__main__":
    class Core:
        def __init__(self) -> None:
            self.path: str = "C:\\Users\\Jakob\\PycharmProjects\\Jarvis\\src\\speechassistant"
            self.audio_output = Audio()

    class Audio:
        def __init__(self):
            pass

        def say(self, text):
            print(text)


    iw = IntentWrapper(Core(), path='\\resources\\intent')

    iw.test_model()

    while True:
        print('Enter something')
        print(iw.proceed_with_user_input(input()))


