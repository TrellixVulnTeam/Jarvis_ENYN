import requests
import speedtest

def isValid(text):
    text = text.lower()
    if "speedtest" in text or ("geschwindigkeit" in text and "internet" in text) or ("schnell" in text and "verbindung" in text):
        return True
    elif "besteht" in text and "verbindung" in text and "internet" in text:
        return True
    else:
        return False

def handle(text, luna, skills):
    text = text.lower()
    if "speedtest" in text or ("geschwindigkeit" in text and "internet" in text) or ("schnell" in text and "verbindung" in text):
        run_speedtest(luna)
    elif "besteht" in text and "verbindung" in text and "internet" in text:
        internet_availability(luna)

def run_speedtest(luna):
    """
    Run an internet speed test. Speed test will show
    1) Download Speed
    2) Upload Speed
    3) Ping
    """
    try:
        luna.say("Bitte warte einen Moment. Der Speedtest wird gestartet")
        st = speedtest.Speedtest()
        server_names = []
        st.get_servers(server_names)

        downlink_bps = st.download()
        uplink_bps = st.upload()
        ping = st.results.ping /1000
        up_mbps = uplink_bps / 1000000
        down_mbps = downlink_bps / 1000000

        luna.say("Der Ping beträgt %s ms,\n"
                 "der Upload %0.2f Mbps\n"
                "un der Download %0.2f Mbps" % (ping, up_mbps, down_mbps)
                )

    except Exception as e:
        luna.say("Der Speedtest konnte nicht gestartet werden.")


def internet_availability(luna):
    """
    Tells to the user is the internet is available or not.
    """
    if internet_connectivity_check():
        luna.say("Es besteht eine Verbindung zum Internet.")
    else:
        luna.say("Derzeit besteht keine Verbingung zum Internet.")

def internet_connectivity_check(url='http://www.google.com/', timeout=2):
    """
    Checks for internet connection availability based on google page.
    """
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False