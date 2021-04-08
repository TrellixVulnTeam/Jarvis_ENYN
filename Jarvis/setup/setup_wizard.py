import base64
import json
import os
import subprocess
import time
import traceback
from pathlib import Path
from Crypto import Random
import speech_recognition as sr
from Jarvis.resources.tts import Text_to_Speech
from pygame import mixer as audio


class FirstStart:
    def __init__(self, Audio):
        self.relPath = str(Path(__file__).parent) + "/"
        with open(self.relPath + "config.json", "r") as config_file:
            self.config_data = json.load(config_file)

        self.Audio = Audio
        self.messenger = False
        time.sleep(2)
        self.run()

        json.dump(self.config_data, config_file)

    def run(self):
        self.say(
            "Hallo, ich bin Jarvis dein neuer Sprachassistent. Ich werde jetzt zusammen mit dir die Einrichtung durchführen.")
        self.say("Wir beginnen mit der Einrichtung deiner Nutzerrepräsentation.")
        self.add_user()
        self.set_voice_gender()
        self.set_home_location()
        self.set_messenger()

        self.say("Wir sind fast fertig. Wir richten nur noch ein paar Module ein.")
        print("\n[STEP-INFO] Switched to setting up the modules...")
        self.set_phillips_hue()
        self.set_phillips_tv()
        self.say(
            "Zum Schluss werde ich noch ein paar Dinge erledigen und anschließend automatisch starten. Das kann etwas dauern.")
        self.set_Network_Key()
        subprocess.run(('sudo chmod 777 -R ' + self.relPath).split(' '))

    def say(self, text):
        self.Audio.say(text)

    def listen(self):
        _input = self.Audio.recognize_input()
        while _input == "Audio konnte nicht aufgenommen werden":
            self.say("Leider habe ich das nicht verstanden, bitte wiederhole deine Eingabe:")
            _input = self.Audio.recognize_input()
        return _input

    def ask_with_answer(self, text):
        print("ask with answer: ", text)
        self.say(text)
        return self.listen()

    def is_desired(self, text):
        desired_words = ["ja", "bitte", "gerne", "jetzt"]
        for item in desired_words:
            if item in text:
                return True
        return False

    def add_user(self):
        user_name = self.ask_with_answer("Wie heißt du?")
        user_age = self.ask_with_answer("Wie alt bist du?")
        user = {
            "name": user_name,
            "age": user_age
        }
        self.config_data["Local_storage"]["user"] = user_name
        self.config_data["Local_storage"]["users"][user_name] = user

    def set_home_location(self):
        home_location = self.ask_with_answer("Wo wohnst du?")
        if home_location.startswith("in "):
            home_location.replace("in ", "")
        self.config_data["Local_storage"]["home_location"] = home_location
        print("[INFO] Place of residence fixed: ", self.config_data["Local_storage"]["home_location"])

    def set_voice_gender(self):
        gender = "female"
        voice_gender = self.ask_with_answer("Zunächst einmal soll ich männlich oder weiblich sein?")
        if "männlich" in voice_gender or "mann" in voice_gender:
            gender = "male"
        self.config_data["voice"] = gender
        self.Audio.tts.select_voice(gender)
        print("[INFO] voice gender fixed: ", self.config_data["voice"])

    def set_phillips_hue(self):
        use_phillip_hue = True if self.is_desired(self.ask_with_answer("Besitzt du ein Phillips Hue System und möchtest es über Jarvis steuern?")) else False
        if use_phillip_hue:
            self.say("Alles klar. Bitte such die Bridch EI PI heraus. Diese findest du in der Phillips Hue App. Ich gebe "
                     "dir 30 Sekunden Zeit und spiel dann ein Signalton ab. Bitte sag danach die IP laut und "
                     "deutlich. Die Punkte müssen auch genannt werden.")
            time.sleep(30)
            self.Audio.play_bling_sound()
            self.config_data["Local_storage"]["module_storage"]["Bridge-IP"] = self.listen()
            print("[INFO] Phillips HUE --> BridgeIP fixed: ",
                  self.config_data["Local_storage"]["module_storage"]["Bridge-IP"])
        else:
            print("[INFO] Phillips HUE not wanted.")

    def set_messenger(self):
        use_messenger = self.ask_with_answer(
            "Möchtest du Telegram verwenden? Bedenke, dass für die Sicherheit des Messengers nicht gesorgt ist.")
        if self.is_desired(use_messenger):
            now = self.ask_with_answer(
                "Alles klar. Möchtest du den benötigten Schlüssel jetzt diktieren oder später selber eingeben")
            if "jetzt" in now:
                self.say("Bitte suche deine Bot-ID heraus. Diese findest du, indem du den "
                         "Bot-father auf Telegram anschreibst und dann släsh start eingibst. Ich warte 30 "
                         "Sekunden und gebe dir dann ein Signalton. Bitte diktiere danach deutlich die Bot-ID.")
                time.sleep(30)
                while True:
                    try:
                        self.Audio.play_bling_sound()
                        token = self.listen()
                        self.set_messenger_tokens(self.config_data["Local_storage"]["user"], token)
                        print("[INFO] Telegram Key fixed: ", self.config_data["messenger_key"])
                        break
                    except:
                        self.say("Tut mir leid, es gab ein Problem, bitte versuche es erneut!")
                        continue
            else:
                self.say("Alles klar. Dann verschieben wir das auf später.")
                print("[INFO] Telegram is desired, but will be entered later by the user.")
        else:
            self.say("Alles klar. Telegram wird nicht eingerichtet.")
            print("[INFO] Telegram not wanted.")

    def set_phillips_tv(self):
        self.say("Ich weiß leider noch nicht, wie ich die Nutzung eines Phillips-Fernsehers einrichten soll. Schau "
                 "dafür einfach mal in die Program-Dokumentation oder frag einfach Jakob.")
        """
        response = self.ask_with_answer('Besitzt du einen Phillips-Fernseher und möchtest diesen über mich steuern?')
        if self.is_desired(response):
            self.say('Okay, bitte schalte den Fernseher jetzt an. Sobald ein Code auf diesem angezeigt wird, '
                     'sag ihn bitte sofort. Bis dahin sollte Ruhe herrschen, damit ich nicht auf Falsches reagiere.')
            time.sleep(5)
            subprocess.call('sudo pip3 install pycryptodome requests paho-mqtt'.split(' '))
            subprocess.call(('python3 ' + self.relPath + 'modules/resources/pylips.py').split(' '))
        """

    def set_Network_Key(self):
        key = Random.get_random_bytes(32)
        key_encoded = base64.b64encode(key)
        key_string = key_encoded.decode('utf-8')
        self.config_data["Network_Key"] = key_string
        print("[INFO] Network Key fixed: ", key_string)


class InstallationAudio:
    def __init__(self):
        self.speech_engine = sr.Recognizer()
        self.speech_engine.pause_threshold = 0.5
        with sr.Microphone(device_index=None) as source:
            self.speech_engine.adjust_for_ambient_noise(source)
        self.tts = Text_to_Speech()
        self.tts.start('male')
        audio.init()

    def recognize_input(self):
        #self.play_bling_sound()
        try:
            with sr.Microphone(device_index=None) as source:
                audio = self.speech_engine.listen(source, timeout=5, phrase_time_limit=5)
                try:
                    text = self.speech_engine.recognize_google(audio, language="de-DE")
                    print(text)
                except:
                    text = "Audio konnte nicht aufgenommen werden"
            return text
        except:
            traceback.print_exc()
            print("[WARNING] Text konnte nicht übersetzt werden...")
            return "Das habe ich leider nicht verstanden."

    def say(self, text):
        self.tts.say(text)

    def play_bling_sound(self):
        TOP_DIR = os.path.dirname(os.path.abspath(__file__))
        DETECT_DONG = os.path.join(TOP_DIR, "../resources/sounds/bling.wav")

        with open(DETECT_DONG, "rb") as wavfile:
            input_wav = wavfile.read()
            audio.music.load(input_wav)
            audio.music.play()


def install_packeges():
    with open('../versions.json', 'r') as version_file:
        versions = json.load(version_file)
    for version in versions.get('last versions'):
        for command in version.get('shellcommands for update'):
            subprocess.run(command.split(' '))
    for command in versions.get('shellcommands for update'):
        subprocess.run(command.split(' '))

if __name__ == "__main__":
    installation = FirstStart(InstallationAudio())
    installation.run()

    core = main