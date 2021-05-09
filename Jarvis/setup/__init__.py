import subprocess
from pathlib import Path


path = '/' + str(Path(__file__).parent).strip("Jarvis/setup")
print(path)
subprocess.run(('sudo chmod 777 -R ' + path).split(' '))
subprocess.run("sudo apt-get install xvfb -y".split(' '))
subprocess.run("sudo pip3 install SpeechRecognition PyVirtualDisplay selenium".split(' '))
