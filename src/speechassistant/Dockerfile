FROM python:3.10.5

RUN apt -y update \
    && apt install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y \
    && apt install -y python3-dev sqlite3 vlc build-essential

WORKDIR /usr/app

COPY requirements.txt .
COPY . .

RUN pip3 install -r requirements.txt

CMD [ "python3.10", "main.py" ]