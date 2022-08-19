import traceback

import requests
import speedtest as speedtest

from src.modules import ModuleWrapper


def is_valid(text: str) -> bool:
    text = text.lower()
    if (
            "speedtest" in text
            or ("geschwindigkeit" in text and "internet" in text)
            or ("schnell" in text and "verbindung" in text)
    ):
        return True
    elif "besteht" in text and "verbindung" in text and "internet" in text:
        return True
    else:
        return False


def handle(text: str, wrapper: ModuleWrapper) -> None:
    text = text.lower()
    if (
            "speedtest" in text
            or ("geschwindigkeit" in text and "internet" in text)
            or ("schnell" in text and "verbindung" in text)
    ):
        run_speedtest(wrapper)
    elif "besteht" in text and "verbindung" in text and "internet" in text:
        internet_availability(wrapper)


def run_speedtest(wrapper):
    """
    Run an internet speed test. Speed test will show
    1) Download Speed
    2) Upload Speed
    3) Ping
    """
    try:
        wrapper.say("Bitte warte einen Moment. Der Speedtest wird gestartet")
        st = speedtest.Speedtest()

        downlink_bps = st.download()
        uplink_bps = st.upload()
        ping = st.ping() / 1000
        up_mbps = uplink_bps / 1000000
        down_mbps = downlink_bps / 1000000

        wrapper.say(
            "Der Ping beträgt %s ms,\n"
            "der Upload %0.2f Mbps\n"
            "un der Download %0.2f Mbps" % (ping, up_mbps, down_mbps)
        )

    except Exception:
        traceback.print_exc()
        wrapper.say(
            "Es gab ein Problem beim Starten des Speedtests. Bitte versuche es zu einem späteren Zeitpunkt "
            "erneut oder melde den Fehler."
        )


def internet_availability(wrapper):
    """
    Tells to the user is the internet is available or not.
    """
    if internet_connectivity_check():
        wrapper.say("Es besteht eine Verbindung zum Internet.")
    else:
        wrapper.say("Derzeit besteht keine Verbingung zum Internet.")


def internet_connectivity_check(url="https://www.google.com/", timeout=2):
    """
    Checks for internet connection availability based on google page.
    """
    try:
        requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


class wrapper:
    def __init__(self):
        pass

    def say(self, text):
        print(text)


if __name__ == "__main__":
    handle("starte Speedtest", wrapper(), None)
