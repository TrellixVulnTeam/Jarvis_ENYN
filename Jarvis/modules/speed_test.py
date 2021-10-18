import traceback

import pyspeedtest


def isValid(text):
    text = text.lower()
    if "speedtest" in text or ("geschwindigkeit" in text and "internet" in text) or (
            "schnell" in text and "verbindung" in text):
        return True
    elif "besteht" in text and "verbindung" in text and "internet" in text:
        return True
    else:
        return False


def handle(text, core, skills):
    text = text.lower()
    if "speedtest" in text or ("geschwindigkeit" in text and "internet" in text) or (
            "schnell" in text and "verbindung" in text):
        run_speedtest(core)
    elif "besteht" in text and "verbindung" in text and "internet" in text:
        internet_availability(core)


def run_speedtest(core):
    """
    Run an internet speed test. Speed test will show
    1) Download Speed
    2) Upload Speed
    3) Ping
    """
    try:
        core.say("Bitte warte einen Moment. Der Speedtest wird gestartet")
        st = pyspeedtest.SpeedTest(host='www.speedtest.net')

        downlink_bps = st.download()
        uplink_bps = st.upload()
        ping = st.ping() / 1000
        up_mbps = uplink_bps / 1000000
        down_mbps = downlink_bps / 1000000

        core.say("Der Ping beträgt %s ms,\n"
                 "der Upload %0.2f Mbps\n"
                 "un der Download %0.2f Mbps" % (ping, up_mbps, down_mbps)
                 )

    except Exception:
        traceback.print_exc()
        core.say("Es gab ein Problem beim Starten des Speedtests. Bitte versuche es zu einem späteren Zeitpunkt "
                 "erneut oder melde den Fehler.")


def internet_availability(core):
    """
    Tells to the user is the internet is available or not.
    """
    if internet_connectivity_check():
        core.say("Es besteht eine Verbindung zum Internet.")
    else:
        core.say("Derzeit besteht keine Verbingung zum Internet.")


def internet_connectivity_check(url='https://www.google.com/', timeout=2):
    """
    Checks for internet connection availability based on google page.
    """
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False
