import subprocess

if __name__ == "__main__":
    # install drivers which are needed for the installation wizard
    subprocess.run("sudo apt-get install xvfb -y".split(" "))
    subprocess.run("sudo pip3 install SpeechRecognition PyVirtualDisplay selenium".split(" "))