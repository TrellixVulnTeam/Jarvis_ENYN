A new version of a better README is planed. For Questions, you can reach me at jakob.priesner@outlook.de

# Jarvis

This repo is a voice assistant that pays attention to privacy and security. It should be able to be integrated as well
as possible into the home automation system.

## Choice of programming language

Since I also wanted to use the project as an opportunity to further my education, I used Python - a language I was not
familiar with until then - to learn it. Since I did not have much idea at the beginning and the code was not yet 100%
revised, it is partly still very habituation and cumbersome. Optimization is therefore very welcome.

## Choice of the required services

Since anonymity is and has been paramount, I have tried (and still do) to find options that are a **useful** alternative
to the voice assistants on the market, but also offer the highest possible level of privacy.

### Text to Speech

To convert the text to speech, I use a website that converts the entered text to spoken using Amazon AWS. Now, you might
think that this is not really privacy compliant, but this website is accessed by several thousand users every day,
making it difficult for Amazon to create an accurate profile. Furthermore, there is not really a viable alternative that
runs on the system itself or is open source. My hopes for the future lie
here [in a project by Mozilla](https://github.com/mozilla/TTS).

### Speech to Text

Here I have to admit that I value performance/quality more than privacy: here I decided to use Google's
SpeechRecognition. Again with the background, as there is currently no **usable** alternative. Anyone who finds a better
alternative is welcome to implement it.

### Wakewordengine

For this I use "procupine", which in itself is very reliable, but in the free version you are more limited in the choice
of the word itself. I have chosen "Jarvis", but this can be changed in the Audio.py in the class AudioInput().

## Installation

The system consists of a Raspi (4 - but should also run on older ones), on which the operating system Debian runs. You
can find enough instructions on the internet or have a look on "Why a Raspberry pi". (A detailed justification and a
recommendation for further required hardware components follows below in the README )
For all further steps, a setup wizard is currently in work, but it will take some time. Therefore, here still in detail
and manually:

(P.S. all commands are executed in the shell).

1. first it never hurts to bring everything up to date.
   `sudo apt-get update`
   `sudo apt-get upgrade`

2. Then install the applications:

- `sudo apt-get install git libatlas-base-dev portaudio19-dev sox flac chromium-chromedriver sqlite3 xvfb`.

3. after that we install all the packages we work with:

- `sudo pip3 install pvporcupine pyaudio SpeechRecognition pyvirtualdisplay selenium phue pywhatkit pafy youtube-dl SpeechRecognition PyVirtualDisplay selenium androidtv wikipedia googlemaps spacex_py html5lib python_dateutil pytube3 gevent youtube-dl pafy python-vlc pyperclip gevent flask pafy python-vlc pygame pyperclip geopy nltk qrcode speedtest-cli pydub matplotlib tensorflow uvicorn fastapi sqlalchemy humps toml`
    - `pip3 install pyperclip3`
- `sudo pip install phue xycolor`

4. Once that's all done, you can take a look at config.json and fill in everything you know. In the part the following
   points should be entered:

- "home_location"
- "server_name"
- "system_name"
- messenger true, if you use it, otherwise false. If you use it, you must also set the "messenger_key". You can find the
  setup of a messenger-bot on the internet. Just search for Bot-Father
- if you want to use Phillips-Hue, you also have to enter the "Bridge IP" and press the button of the bridge when you
  call it for the first time

5. Remote desktop setup(only possible with GUI)

- `sudo apt-get install xrdp`

Only if there are errors in the connection:

- `sudo apt-get remove xrdp vnc4server tightvncserver --yes`
- `sudo apt-get install tightvncserver --yes`
- `sudo apt-get install xrdp –yes`

## Why a Raspberry pi

For Jarvis, I recommend a Raspberry Pi: it is inexpensive and at the same time brings enough power. I decided on a Raspi
4, because it is the most powerful. However, I would reconsider the purchase, since this one - unlike its predecessors -
gets very warm due to the high performance, and you therefore need a fan. This is at least audible when sleeping.
Therefore, if the server is not the same as the client, I would go for a Raspi 3B+.With a Raspi 4, a case must also be
purchased.

In addition, a Raspi makes sense, because it not only brings WLAN and Bluetooth, but also has the GPIO pins, to which
later smart home devices can be connected.The installation of "Debian Buster" (the operating system) is very simple. I
use a graphical user interface, because I work on new modules all the time and save a lot of time. I also want to make
the project more or less friendly for beginner, so it only makes sense to use an operating system with a GUI. To
install, first download the balenaEtcher program. Open it and select your micro SD card in the first field and the ISO
file in the installation folder in the second field. Then wait until the program has run. Then remove the SD card from
the PC and insert it into the Raspi. There you perform the setup. The question if the new updates should be installed, I
would answer in the affirmative. The microphone and the box must of course also be connected. As a box I use my anyway
in the room existing sound system, as a microphone a 10 € part. The only thing to keep in mind when buying a microphone
is that it must be omni-directional. This is usually fulfilled by the so-called "conference microphones". For the
speakers, I would go for a model with its own power supply, since the Raspi only provides a very limited voltage for the
audio output. Note that a USB port connected to the Raspi also takes power from it, so that can also cause problems. If
you are using the operating version with GUI, you can simply look if you get a lightning symbol on the top right. If
yes, then use speakers that are NOT connected to the Raspi. Also, I recommend a soundstick, such
as [this one](https://www.amazon.de/gp/product/B00C7LXUDY/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1). This is due
to the fact that the audio board of the Raspi has been saved and the sound via jack is therefore not so good. In
addition, there is not permanently on this voltage, so that the Raspi consumes less power. However, if a sound is
played, the full power comes, which leads to a crackling sound. (NOT ALWAYS!!!)

## How can I develop "modules

First of all, you need to consider whether you want your module to be called only on command, or to be called in a
certain time interval. 1.In a certain time interval:Continuous modules run permanently in the background in Core and are
called in a fixed time interval. This is specified in seconds. Try to keep this time interval as long as possible, so
that it is called as seldom as possible. This may save some of the
needed computing power. For this you use a so called continuous _module. The structure looks like this:

```
INTERVALL = 2

def run(core (in older modules core), skills):
    .
    .
    .
```

Here the `INTERVALL` describes the time interval and `def run` describes the method that should be called.
Skills represents the module_skills, which provide useful functions. You can find them in the resources folder

In "normal modules":

```
PRIORITY= -1
def is_valid(text):
    text = text.lower()
    if ‚Example word‘ in text:
        return True
    elif ‚other example word‘ in text:
        return True
    else:
        return False

def handle(text, core, profile):
    .
    .
    .
```

`PRIORITY` defines the priority in which the modules are called. If this is not set, the value 0 is automatically
assigned. The modules are ordered lexically in the respective priority level. Since LUNA cannot know what your module
can do, the modules must decide in a first rough run whether they can do something with the text. For this the
method `is_valid()` is used, which returns True if this is the case. This function only checks if a keyword is included
in the command or not. Your word selection should be well considered. If this is the case, the method `handle()`
or `run()` is called.

For all other core (or core) calls, you can look into the `module wrapper` class in main.py
