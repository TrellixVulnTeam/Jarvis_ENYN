import io
import json
import logging
import urllib
from urllib.request import Request, urlopen


class Test_Modulewrapper:
    def __init__(self, core, text, analysis, messenger, user):
        self.text = text
        self.analysis = analysis
        # toDo: down below
        # self.analysis['town'] = core.local_storage['home_location'] if self.analysis['town'] is None else None

        self.audio_output = core.audio_output
        self.audio_input = core.audio_input

        self.messenger_call = messenger

        self.room = "messenger" if messenger else "raum"
        self.messenger = core.messenger

        self.core = core
        self.skills = core.skills
        self.Analyzer = core.analyzer
        self.local_storage = core.local_storage
        self.system_name = core.system_name
        self.path = core.path
        self.user = user

    def say(self, text, output='auto'):
        text = self.speechVariation(text)
        if output == 'auto':
            if self.messenger_call:
                output = 'messenger'
        if 'messenger' in output.lower() or self.messenger_call:
            self.messenger_say(text)
        else:
            text = self.correct_output_automate(text)
            self.Audio_Output.say(text)

    def messenger_say(self, text):
        try:
            self.messenger.say(text, self.user['telegram_id'])
        except KeyError:
            logging.warning(
                '[WARNING] Sending message "{}" to messenger failed, because there is no Telegram-ID for this user '
                '({}) '.format(text, self.user["name"]))
        except AttributeError:
            logging.info('[WARNING] Sending message to messenger failed,  because there is no key for it!')
        return

    def play(self, path=None, audiofile=None, next=False, notification=False):
        if path is not None:
            with open(path, "rb") as wav_file:
                input_wav = wav_file.read()
        if audiofile is not None:
            with open(audiofile, "rb"):
                input_wav = wav_file.read()
        data = io.BytesIO(input_wav)
        if notification:
            self.Audio_Output.play_notification(data, next)
        else:
            self.Audio_Output.play_playback(data, next)

    def play_music(self, by_name=None, url=None, path=None, next=None, now=None, playlist=None, announce=None):
        if by_name is not None:
            by_name = "'" + by_name + "'"
        # simply forward information
        self.Audio_Output.music_player.play(by_name=by_name, url=url, path=path, next=next, now=now, playlist=playlist,
                                            announce=announce)

    def listen(self, text=None, messenger=None):
        if messenger is None:
            messenger = self.messenger_call
        if text is not None:
            self.say(text)
        if messenger:
            return self.core.messenger_listen(self.user["first_name"].lower())
        else:
            return self.Audio_Input.recognize_input(listen=True)

    def recognize(self, audio_file):
        return self.Audio_Input.recognize_file(audio_file)

    @staticmethod
    def words_in_text(words, text):
        for word in words:
            if word not in text:
                return False
        return True

    def start_module(self, name=None, text=None, user=None):
        self.core.start_module(text, name, user, messenger=self.messenger)

    def start_module_and_confirm(self, name=None, text=None, user=None):
        return self.core.start_module(text, name, user)

    def module_storage(self, module_name=None):
        module_storage = self.core.local_storage.get("module_storage")
        if module_name is None:
            return module_storage
        # I am now just so free and lazy and assume that a module name is passed from a module that actually exists.
        else:
            return module_storage[module_name]

    @staticmethod
    def translate(text, target_lang='de'):
        try:
            request = Request(
                'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=' + urllib.parse.quote(
                    target_lang) + '&dt=t&q=' + urllib.parse.quote(
                    text))
            response = urlopen(request)
            answer = json.loads(response.read())
            return answer[0][0][0]
        except:
            return text

    def correct_output(self, core_array, messenger_array):
        if self.messenger_call is True:
            return messenger_array
        else:
            return core_array

    def correct_output_automate(self, text):
        text = text.strip()
        # This function is to correct words that should always be corrected right away,
        # so that correct_output doesn't have to be called every time and corrected manually
        # must be corrected
        if self.messenger_call:
            pass
        else:
            correct_output = self.core.config_data["correct_output"]
            for item in correct_output:
                text = text.replace(item, correct_output[item])
        return text

    def start_hotword_detection(self):
        self.Audio_Input.start()

    def stopp_hotword_detection(self):
        self.Audio_Input.stop()

    def speechVariation(self, userInput):
        """
        if not isinstance(input, str):
            parse = random.choice(userInput)
        else:
            parse = userInput
        while "[" in parse and "]" in parse:
            sp0 = parse.split("[", 1)
            front = sp0[0]
            sp1 = sp0[1].split("]", 1)
            middle = sp1[0].split("|", 1)
            end = sp1[1]
            parse = front + random.choice(middle) + end
            """
        #toDo
        return userInput