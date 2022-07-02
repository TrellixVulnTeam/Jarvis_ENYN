FROM ubuntu:latest

RUN apt-get update -y \
    && apt-get install -y python3 \
    && apt-get install -y python3-pip \
    && apt-get install -y libatlas-base-dev \
    && apt-get install -y portaudio19-dev \
    && apt-get install -y sox \
    && apt-get install -y flac \
    && apt-get install -y chromium-chromedriver \
    && apt-get install -y sqlite3 \
    && apt-get install -y vlc \
    && apt-get install -y xvfb

WORKDIR /home/jarvis

COPY requirements.txt requirements.txt
COPY . /home/jarvis

RUN pip install -r requirements.txt

CMD [ "python3", "main.py" ]