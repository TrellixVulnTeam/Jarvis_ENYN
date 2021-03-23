# Jarvis

## Intention
When I started with a precursor to this project, I was keen to control my Phillips HUE lamps via voice. Since I don't trust Alexa and co., I looked into how to program an alternative myself. The whole project has become a much bigger one.

## Choice of programming language
Since I also wanted to use the project as an opportunity to further my education, I used Python - a language I was not familiar with until then - to learn it. Since I did not have much idea at the beginning and the code was not yet 100% revised, it is partly still very habituation and cumbersome. Optimization is therefore very welcome.

## Choice of the required services
Since anonymity is and has been paramount, I have tried (and still do) to find options that are a **useful** alternative to the voice assistants on the market, but also offer the highest possible level of privacy. 

### Text to Speech
To convert the text to speech, I use a website that converts the entered text to spoken using Amazon AWS. Now, you might think that this is not really privacy compliant, but this website is accessed by several thousand users every day, making it difficult for Amazon to create an accurate profile.  Furthermore, there is not really a viable alternative that runs on the system itself or is open source. My hopes for the future lie here [in a project by Mozilla](https://github.com/mozilla/TTS).

### Speech to Text
Here I have to admit that I value performance/quality more than privacy: here I decided to use Google's SpeechRecognition. Again with the background, as there is currently no **usable** alternative. Anyone who finds a better alternative is welcome to implement it.

### Wakewordengine
For this I use "procupine", which in itself is very reliable, but in the free version you are more limited in the choice of the word itself. I have chosen "Jarvis", but this can be changed in the Audio.py in the class AudioInput(). 

## Installation
The system consists of a Raspi (4 - but should also run on older ones), on which the operating system Debian runs. You can find enough instructions on the internet oder einen Blick auf den Punkt "Why a Raspberry pi" werfen. (A detailed justification and a recommendation for further required hardware components follows below in the README )
For all further steps, a setup wizard is currently in work, but it will take some time. Therefore here still in detail and manually:

(P.S. all commands are executed in the shell).

1. first it never hurts to bring everything up to date. 
`sudo apt-get update`
`sudo apt-get upgrade`

2. Then install the applications:
- `sudo apt-get installpython3.5-dev python3.4-dev libatlas-base-dev`.
- Also the following if remote desktop control is desired
    `sudo apt-get install xvfb -y`

3. after that we install all the packages we work with:
- `sudo pip3 install pywhatkit pafy youtube-dl SpeechRecognition PyVirtualDisplay selenium androidtv wikipedia googlemapsspacex_pyhtml5lib python_dateutilpytube3`
- `sudo pip install phue xycolor`

4. Once that's all done, you can take a look at config.json and fill in everything you know. In the part the following points should be entered: 
- "home_location"
- "server_name"
- "system_name"
- telegram true, if you use it, otherwise false. If you use it, you must also set the "telegram_key". You can find the setup of a telegram-bot on the internet. Just search for Bot-Father
- if you want to use Phillips-Hue, you also have to enter the "Bridge IP" and press the button of the bridge when you call it for the first time


## Why a Raspberry pi
For Jarvis, I recommend a Raspberry Pi: it is inexpensive and at the same time brings enough power.  I decided on a Raspi 4, because it is the most powerful. However, I would reconsider the purchase, since this one - unlike its predecessors - gets very warm due to the high performance and you therefore need a fan. This is at least audible when sleeping.  Therefore, if the server is not the same as the client, I would go for a Raspi 3B+.With a Raspi 4, a case must also be purchased.  Here I can recommend the following model: 
- [Case 1](https://www.amazon.de/LABISTS-Geh%C3%A4use-Raspberry-Netzteil-K%C3%BChlk%C3%B6rper/dp/B082XV8PTY/ref=sr_1_15?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=raspberry+pi+4+geh%C3%A4use&qid=1596057512&s=ce-de&sr=1-15)
- [Case 2](https://www.amazon.de/dp/B08BKYSZS3/ref=sr_1_35?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3AQH6GBOBVF4V&dchild=1&keywords=raspberry+pi+4+geh%C3%A4use&qid=1596056942&s=ce-de&sprefix=rasp%2Celectronics%2C186&sr=1-35)
In addition, a Raspi makes sense, because it not only brings WLAN and Bluetooth, but also has the GPIO pins, to which later smart home devices can be connected.The installation of "Debian Buster" (the operating system) is very simple. I use a graphical user interface, because I work on new modules all the time and save a lot of time. I also want to make the project more or less beginner friendly, so it only makes sense to use an operating system with a GUI. To install, first download the balenaEtcher program.  Open it and select your micro SD card in the first field and the ISO file in the installation folder in the second field.   Then wait until the program has run. Then remove the SD card from the PC and insert it into the Raspi. There you perform the setup.  The question if the new updates should be installed, I would answer in the affirmative. The microphone and the box must of course also be connected.  As a box I use my anyway in the room existing sound system, as a microphone a 10€ part.  The only thing to keep in mind when buying a microphone is that it must be omni-directional. This is usually fulfilled by the so-called "conference microphones". For the speakers, I would go for a model with its own power supply, since the Raspi only provides a very limited voltage for the audio output. Note that a USB port connected to the Raspi also takes power from it, so that can also cause problems. If you are using the operating version with GUI, you can simply look if you get a lightning symbol on the top right.   If yes, then use speakers that are NOT connected to the Raspi. Also, I recommend a soundstick, such as [this one](https://www.amazon.de/gp/product/B00C7LXUDY/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1). This is due to the fact that the audio board of the Raspi has been saved and the sound via jack is therefore not so good. In addition, there is not permanently on this voltage, so that the Raspi consumes less power.  However, if a sound is played, the full power comes, which leads to a crackling sound. (NOT ALWAYS!!!)
  