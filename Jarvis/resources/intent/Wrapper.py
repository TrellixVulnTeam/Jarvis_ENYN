import json
import logging

from AI import GenericAssistant


class IntentWrapper:
    def __init__(self, core):
        self.core = core
        core.path = "C:\\Users\\Jakob\\OneDrive\\Jarvis\\Jarvis"
        with open(core.path + "/resources/intent/mappings.json", 'r') as mapping_file:
            mappings = json.loads(mapping_file.read())
            self.ai = GenericAssistant('intents.json', core.path + '/resources/intent/', intent_methods=mappings)
            try:
                self.ai.load_model()
                logging.info("Model loaded successfully")
            except FileNotFoundError:
                logging.info("Couldn't find a model, so train a new one...")
                self.core.Audio_Output.say("Meine Inteligenz wurde leider noch nicht trainiert. Ich werde das schnell erledigen, habe bitte etwas Geduld! Dieser Vorgang dauert etwa 3 Stunden.")
                self.ai.train_model()
                logging.info("Model trained successfully")
                self.ai.save_model()
                logging.info("Model saved sucessfully")
                try:
                    self.ai.load_model()
                    logging.info("Model loaded successfully")
                except:
                    logging.critical("Fatal error in AI: Couldn't load model!")
        logging.info("AI initialized successfully!")

    def proceed_with_user_input(self, user_input):
        return self.ai.request(user_input)

    def test_module(self, user_input):
        response = self.ai.test_request(user_input)
        if type(response) is type(""):
            return response
        elif type(response) is type({}):
            return response["intent"]

    def train_model(self):
        logging.info("Start training model")
        self.ai.train_model(1000)
        logging.info("Training done")
        self.ai.save_model()
        self.ai.load_model()
