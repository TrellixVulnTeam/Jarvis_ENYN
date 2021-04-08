import requests

class SignalBot:
    def __init__(self, core, api_key):
        self.core = core
        self.api_key = api_key

    def send_message(self, message, user):
        phone_number = user.get("phone-number")
        req = f'https://api.callmebot.com/signal/send.php?phone={phone_number}&apikey={self.api_key}&text={message}'
        requests.request(req)