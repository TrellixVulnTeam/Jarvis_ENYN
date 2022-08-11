import logging
from datetime import datetime
from pyicloud import PyiCloudService


class CloudService:
    def __init__(self, username, password, core):
        self.connected = True
        self.api = self.login(username, password)
        self.core = core

    def login(self, username, password):
        api = PyiCloudService(username, password)
        if api.requires_2fa:
            logging.info(
                f"ICloud with mail {username} required Two-factor authentication!"
            )
            result = api.validate_2fa_code(self.__get_2fa_code())

            if not result:
                logging.critical(
                    f"Failed to verify security code of ICloud-Account with mail {username}"
                )
                self.connected = False

            if not api.is_trusted_session:
                logging.info(
                    f"Session for mail, {username} is not trusted. Requesting trust..."
                )
                result = api.trust_session()
                print(f"Session trust for mail {username} result '{result}'")

                if not result:
                    logging.critical(
                        "Failed to request trust. You will likely be prompted for the code again in the coming weeks!"
                    )
                    self.connected = False
        elif api.requires_2sa:
            import click

            devices = api.trusted_devices
            for i, device in enumerate(devices):
                print(
                    "  %s: %s"
                    % (
                        i,
                        device.get(
                            "deviceName", "SMS to %s" % device.get("phoneNumber")
                        ),
                    )
                )

            device = click.prompt("Which device would you like to use?", default=0)
            device = devices[device]
            if not api.send_verification_code(device):
                logging.critical("Failed to send verification code")
            code = click.prompt("Please enter validation code")

            if not api.validate_verification_code(device, code):
                logging.critical("Failed to verify verification code!")
                self.connected = False

        return api

    def __get_2fa_code(self):
        return int(input("Enter 2fa code"))

    def get_devices(self):
        devices = self.api.devices
        return devices

    def get_phone(self):
        return self.api.iphone

    def get_phones_last_position(self):
        return self.api.iphone.location()

    def get_phone_status(self):
        return self.api.iphone.status()

    def get_calendar_events(self):
        from_dt = datetime(2021, 12, 1)
        to_dt = datetime(2021, 12, 5)
        return self.api.calendar.events(from_dt, to_dt)

    def play_sound_on_phone(self):
        self.api.iphone.play_sound()

    def enable_lost_phone_mode(self, number, message):
        self.api.iphone.lost_device(number, message)
