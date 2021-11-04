import json
import logging

from AI import GenericAssistant


class IntentWrapper:
    def __init__(self, core):
        self.core = core
        with open("mappings.json", 'r') as mapping_file:
            mappings = json.loads(mapping_file.read())
            self.ai = GenericAssistant('intents.json', intent_methods=mappings)
            try:
                self.ai.load_model()
            except FileNotFoundError:
                self.core.Audio_Output.say("Meine Inteligenz wurde leider noch nicht trainiert. Ich werde das schnell erledigen, habe bitte etwas Geduld! Dieser Vorgang dauert etwa 3 Stunden.")
                self.ai.train_model()
                self.ai.save_model()
                try:
                    self.ai.load_model()
                except:
                    logging.critical("Fatal error in AI: Couldn't load model!")

    def proceed_with_user_input(self, user_input):
        response = self.ai.test_request(user_input)
        if type(response) is type(""):
            return response
        elif type(response) is type({}):
            return response

    def test_module(self, user_input):
        response = self.ai.test_request(user_input)
        if type(response) is type(""):
            return response
        elif type(response) is type({}):
            return response["intent"]

    def train_model(self):
        self.ai.train_model(800)
        print("Training done")
        self.ai.save_model()
        self.ai.load_model()
