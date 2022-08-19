from src.modules import ModuleWrapper, skills
from src.services.philips_tv.philips_tv import Pylips


# toDo: refactor

user = ""
password = ""
path = ""

color_in_hsb = {
    "blau": [240, 100, 100],
    "rot": [0, 100, 100],
    "gelb": [60, 100, 100],
    "grün": [120, 100, 100],
    "magenta": [300, 100, 100],
}


def isValid(text: str) -> bool:
    text = text.lower()
    if "fernseh" in text:
        return True


def handle(text: str, wrapper: ModuleWrapper) -> None:
    text = text.lower()

    if "hdmi" in text:
        wrapper.say("Diese Funktion ist leider noch in der Entwicklung.")  # ToDo
    elif "mach" in text and "lauter" in text:
        wrapper.say("Diese Funktion ist leider noch in der Entwicklung.")  # ToDo
    elif ("schalte" in text or "mach" in text) and "aus" in text:
        # it is not really "switch off" but "stand by"
        run_command("standby", wrapper)

    elif ("schalte" in text or "mach" in text) and "an" in text:
        run_command("power_on", wrapper)

    elif "mute" in text or ("schalte" in text and "stumm" in text):
        run_command("mute", wrapper)

    elif "schalte" in text:
        if "hoch" in text:
            run_command("channel_up", wrapper)
        elif "runter" in text:
            run_command("channel_down", wrapper)
        else:
            wrapper.say("Ich habe leider nicht verstanden, wohin ich schalten soll.")

    elif "play" in text:
        run_command("play", wrapper)

    elif "pause" in text:
        run_command("pause", wrapper)

    elif "stop" in text:
        run_command("stop", wrapper)

    elif "spul" in text:
        if "vor" in text:
            run_command("fast_forward", wrapper)
        elif "zurück" in text:
            run_command("rewind", wrapper)
        else:
            wrapper.say("Ich habe leider nicht verstanden, wohin ich spulen soll.")

    elif "bestätige" in text or "stimme zu" in text:
        run_command("confirm", wrapper)

    elif "home" in text or "übersicht" in text:
        run_command("home", wrapper)

    elif "einstellung" in text:
        run_command("options", wrapper)

    elif ("nimm" in text and "auf" in text) or "record" in text:
        run_command("record", wrapper)

    elif "ambilight" in text or "hintergrundbeleuchtung" in text:
        if "an" in text:
            run_command("ambilight_on", wrapper)
        elif "aus" in text:
            run_command("ambilight_off", wrapper)
        elif skills.match_any(text, color_in_hsb.keys()):
            for color in color_in_hsb.keys():
                if color in text:
                    color_inf = color_in_hsb.get(color)
                    run_command(
                        "ambilight_color",
                        wrapper,
                        body={
                            "hue": color_inf[0],
                            "saturation": color_inf[1],
                            "brightness": color_inf[2],
                        },
                    )
        elif "video" in text:
            run_command("ambilight_video_standard", wrapper)
        elif "natur" in text:
            run_command("ambilight_color_fresh_nature", wrapper)

    elif "ist" in text and "an" in text:
        if get_powerstate(wrapper):
            wrapper.say("Ja.")
        else:
            wrapper.say("Nein, soll ich ihn einschalten?")
            if skills.is_desired(wrapper.listen()):
                run_command("power_on", wrapper)

    elif "hdmi" in text:
        if "1" in text:
            run_command("input_hdmi_1", wrapper)
        elif "2" in text:
            run_command("input_hdmi_2", wrapper)
        elif "3" in text:
            run_command("input_hdmi_3", wrapper)
        elif "4" in text:
            run_command("input_hdmi_4", wrapper)

    elif "öffne" in text or "start" in text:
        if "netflix" in text:
            launch_app("netflix", wrapper)
        elif "amazon" in text and "prime" in text:
            launch_app("amazon_prime", wrapper)
        elif "youtube" in text:
            launch_app("youtube", wrapper)
        elif "kodi" in text:
            launch_app("kodi", wrapper)
        elif "playstore" in text or "appcenter" in text:
            launch_app("playstore", wrapper)
        elif "twitch" in text:
            launch_app("twitch", wrapper)
        elif "aufnehmen" in text or "guide" in text:
            launch_app("tv_guide", wrapper)
        elif "disney" in text:
            launch_app("disney+", wrapper)
        elif "mediathek" in text:
            if "zdf" in text or "zweite" in text:
                launch_app("zdf_mediathek", wrapper)
            elif "erste" in text or "ard" in text:
                launch_app("erste_mediathek", wrapper)
        elif "internet" in text or "browser" in text:
            launch_app("web", wrapper)
        elif "fernsehen" in text or "tv" in text:
            run_command("watch_tv", wrapper)

    else:
        run_command("google_assistant", wrapper, body={"query": text})


def run_command(command, wrapper, body=None):
    print("--------------------->> run")
    inf = wrapper.module_storage("philips-tv")
    user = inf.get("user")
    password = inf.get("pass")
    host = inf.get("host")
    apiv = inf.get("apiv")
    pl = Pylips()
    pl.run(
        host=host,
        user=user,
        password=password,
        body=body,
        command=command,
        verbose=True,
        apiv=apiv,
    )


def switch_hdmi(input_number, wrapper):
    run_command("input_hdmi_" + str(input_number), wrapper)


def send_digit(digit, wrapper):
    run_command("digit_" + digit, wrapper)


def send_color_key(color, wrapper):
    run_command(color, wrapper)


def get_powerstate(wrapper):
    return run_command("powerstate", wrapper)


def get_current_channel(wrapper):
    return run_command("current_channel", wrapper)


def get_current_app(wrapper):
    return run_command("current_app", wrapper)


def launch_app(name, wrapper):
    if name == "netflix":
        body = '{"label":"Netflix","intent":{"component":{"packageName":"com.netflix.ninja","className":"com.netflix.ninja.MainActivity"},"action":"Intent{act=android.intent.action.MAINcat=[android.intent.category.LAUNCHER]flg=0x10000000pkg=com.netflix.ninjacmp=com.netflix.ninja/.MainActivity}"},"order":0,"id":"com.netflix.ninja.MainActivity-com.netflix.ninja","type":"app"}'
    elif name == "youtube":
        body = '{"id":"com.google.android.apps.youtube.tv.activity.ShellActivity-com.google.android.youtube.tv","order":0,"intent":{"action":"Intent{act=android.intent.action.MAINcat=[android.intent.category.LAUNCHER]flg=0x10000000pkg=com.google.android.youtube.tvcmp=com.google.android.youtube.tv/com.google.android.apps.youtube.tv.activity.ShellActivity}}","component":{"packageName":"com.google.android.youtube.tv","className":"com.google.android.apps.youtube.tv.activity.ShellActivity"},"label":"YouTube"}}'
    elif name == "amazon_prime":
        body = '{"id":"com.amazon.amazonvideo.livingroom","order":0,"intent":{"action":"Intent{act=android.intent.action.MAINcat=[android.intent.category.LAUNCHER]flg=0x10000000pkg=com.amazon.amazonvideo.livingroom}","component":{"packageName":"com.amazon.amazonvideo.livingroom","className":"com.amazon.ignition.IgnitionActivity"}},"label":"PrimeVideo"}'
    elif name == "kodi":
        body = '{"id":"org.xbmc.kodi","order":0,"intent":{"action":"Intent{act=android.intent.action.MAINcat=[android.intent.category.LAUNCHER]flg=0x10000000pkg=org.xbmc.kodi}","component":{"packageName":"org.xbmc.kodi","className":"org.xbmc.kodi.Splash","label":"Kodi"}'
    elif name == "playstore":
        body = '{"label":"Play Store","intent": {"component":{"packageName":"com.android.vending","className":"com.google.android.finsky.tvmainactivity.TvMainActivity"},"action":"android.intent.action.MAIN"},"order":0,"id":"com.google.android.finsky.tvmainactivity.TvMainActivity-com.android.vending","type":"app"}'
    elif name == "twitch":
        body = '{"label":"SmartTV Client for Twitch","intent": {"component":{"packageName":"com.fgl27.twitch","className":"com.fgl27.twitch.PlayerActivity"},"action":"android.intent.action.MAIN"},"order":0,"id":"com.fgl27.twitch.PlayerActivity-com.fgl27.twitch","type":"app"}'
    elif name == "tv_guide":
        body = '{"id":"org.droidtv.channels.ChannelsActivity-org.droidtv.channels","order":0,"intent":{"action":"android.intent.action.MAIN"},"component":{"packageName":"org.droidtv.channels","className":"org.droidtv.channels.ChannelsActivity","label":"SmartTVClientforTwitch","type":"app"}'
    elif name == "disney+":
        body = '{"id":"com.bamtechmedia.dominguez.main.MainActivity-com.disney.disneyplus","order":0,"intent":{"action":"android.intent.action.MAIN"},"component":{"packageName":"com.disney.disneyplus","className":"com.bamtechmedia.dominguez.main.MainActivity","label":"Disney+","type":"app"}}'
    elif name == "zdf_mediathek":
        body = '{"id":"com.zdf.android.mediathek.ui.splash.SplashActivity-com.zdf.android.mediathek","order":0,"intent":{"action":"empty"},"component":{"packageName":"com.zdf.android.mediathek","className":"com.zdf.android.mediathek.ui.splash.SplashActivity","label":"ZDFmediathek","type":"app"}'
    elif name == "erste_mediathek":
        body = '{"id":"com.daserste.daserste.MainActivity-de.daserste.apps.androidtv","order":0,"intent":{"action":"empty"},"component":{"packageName":"de.daserste.apps.androidtv","className":"com.daserste.daserste.MainActivity""label":"DasErsteMediathek","type":"app"}'
    elif name == "web":
        body = '{"id":"jp.co.rarity.tvweb.MainActivity-jp.co.rarity.tvweb","order":0,"intent":{"action":"empty"},"component":{"packageName":"jp.co.rarity.tvweb","className":"jp.co.rarity.tvweb.MainActivity","label":"TVWeb","type":"app"}'
    else:
        body = ""
    run_command("launch_app", wrapper, body=body)
