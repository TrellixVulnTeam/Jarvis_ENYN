import base64
import json
import os
import subprocess
import time
import traceback
from pathlib import Path
from Crypto import Random
import speech_recognition as sr
from tts import Text_to_Speech
from pygame import mixer as audio
import main


class FirstStart:
    def __init__(self):
        relPath = str(Path(__file__).parent) + "/"
        with open(relPath + "config.json", "r") as config_file:
            self.config_data = json.load(config_file)

        self.Audio = InstallationAudio()
        self.telegram = False
        time.sleep(2)
        self.run()

    def run(self):
        self.say(
            "Hallo, ich bin Jarvis dein neuer Sprachassistent. Ich werde jetzt zusammen mit dir die Einrichtung durchführen")
        self.set_voice_gender()
        self.set_home_location()
        self.set_telegram()

        self.say("Wir sind fast fertig. Wir richten nur noch ein paar meiner Module ein.")
        print("\n[STEP-INFO] Switched to setting up the modules...")
        self.set_phillips_hue()
        self.say(
            "Zum Schluss werde ich noch ein paar Dinge erledigen und anschließend automatisch starten. Das kann etwas dauern.")
        self.set_Network_Key()

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
        desired_words = ["ja", "bitte", "gerne"]
        for item in desired_words:
            if item in text:
                return True
        return False

    def add_user(self):
        user_name = self.ask_with_answer("Zunächst einmal, wie heißt du?")
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

    def set_telegram(self):
        use_telegram = self.ask_with_answer(
            "Möchtest du Telegram verwenden? Bedenke, dass für die Sicherheit des Messengers nicht gesorgt ist.")
        if self.is_desired(use_telegram):
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
                        telegram_number = self.listen()
                        self.config_data["telegram_key"] = int(telegram_number)
                        print("[INFO] Telegram Key fixed: ", self.config_data["telegram_key"])
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
        DETECT_DONG = os.path.join(TOP_DIR, "resources/bling.wav")

        with open(DETECT_DONG, "rb") as wavfile:
            input_wav = wavfile.read()
            audio.music.load(input_wav)
            audio.music.play()


def install_packeges():
    # install drivers which are needed for the installation wizard
    subprocess.run("sudo apt-get install xvfb -y".split(" "))
    subprocess.run("sudo pip3 install SpeechRecognition PyVirtualDisplay selenium")

if __name__ == "__main__":
    installation = FirstStart()
    installation.run()

    core = main