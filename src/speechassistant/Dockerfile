FROM ubuntu:22.04

WORKDIR /home/jarvis
COPY requirements.txt requirements.txt


RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y libatlas-base-dev
RUN apt-get install -y portaudio19-dev
RUN apt-get install -y sox
RUN apt-get install -y flac
RUN apt-get install -y chromium-chromedriver
RUN apt-get install -y sqlite3

CMD [ "pip3", "install", "-r", "requirements.txt" ]

COPY . /home/jarvis

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]