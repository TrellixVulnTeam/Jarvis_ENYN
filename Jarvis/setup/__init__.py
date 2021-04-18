import subprocess


def __init__():
    subprocess.run("sudo apt-get install xvfb -y".split(" "))
    subprocess.run("sudo pip3 install SpeechRecognition PyVirtualDisplay selenium".split(" "))
