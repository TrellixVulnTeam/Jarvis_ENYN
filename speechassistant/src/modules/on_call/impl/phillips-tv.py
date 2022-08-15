from src.services.philips_tv.philips_tv import Pylips

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


def isValid(text):
    text = text.lower()
    if "fernseh" in text:
        return True


def handle(text, core, skills):
    text = text.lower()

    if "hdmi" in text:
        core.say("Diese Funktion ist leider noch in der Entwicklung.")  # ToDo
    elif "mach" in text and "lauter" in text:
        core.say("Diese Funktion ist leider noch in der Entwicklung.")  # ToDo
    elif ("schalte" in text or "mach" in text) and "aus" in text:
        # it is not really "switch off" but "stand by"
        run_command("standby", core)

    elif ("schalte" in text or "mach" in text) and "an" in text:
        run_command("power_on", core)

    elif "mute" in text or ("schalte" in text and "stumm" in text):
        run_command("mute", core)

    elif "schalte" in text:
        if "hoch" in text:
            run_command("channel_up", core)
        elif "runter" in text:
            run_command("channel_down", core)
        else:
            core.say("Ich habe leider nicht verstanden, wohin ich schalten soll.")

    elif "play" in text:
        run_command("play", core)

    elif "pause" in text:
        run_command("pause", core)

    elif "stop" in text:
        run_command("stop", core)

    elif "spul" in text:
        if "vor" in text:
            run_command("fast_forward", core)
        elif "zurück" in text:
            run_command("rewind", core)
        else:
            core.say("Ich habe leider nicht verstanden, wohin ich spulen soll.")

    elif "bestätige" in text or "stimme zu" in text:
        run_command("confirm", core)

    elif "home" in text or "übersicht" in text:
        run_command("home", core)

    elif "einstellung" in text:
        run_command("options", core)

    elif ("nimm" in text and "auf" in text) or "record" in text:
        run_command("record", core)

    elif "ambilight" in text or "hintergrundbeleuchtung" in text:
        if "an" in text:
            run_command("ambilight_on", core)
        elif "aus" in text:
            run_command("ambilight_off", core)
        elif any(color_in_hsb.keys()) in text:
            for color in color_in_hsb.keys():
                if color in text:
                    color_inf = color_in_hsb.get(color)
                    run_command(
                        "ambilight_color",
                        core,
                        body={
                            "hue": color_inf[0],
                            "saturation": color_inf[1],
                            "brightness": color_inf[2],
                        },
                    )
        elif "video" in text:
            run_command("ambilight_video_standard", core)
        elif "natur" in text:
            run_command("ambilight_color_fresh_nature", core)

    elif "ist" in text and "an" in text:
        if get_powerstate(core):
            core.say("Ja.")
        else:
            core.say("Nein, soll ich ihn einschalten?")
            if skills.is_desired(core.listen()):
                run_command("power_on", core)

    elif "hdmi" in text:
        if "1" in text:
            run_command("input_hdmi_1", core)
        elif "2" in text:
            run_command("input_hdmi_2", core)
        elif "3" in text:
            run_command("input_hdmi_3", core)
        elif "4" in text:
            run_command("input_hdmi_4", core)

    elif "öffne" in text or "start" in text:
        if "netflix" in text:
            launch_app("netflix", core)
        elif "amazon" in text and "prime" in text:
            launch_app("amazon_prime", core)
        elif "youtube" in text:
            launch_app("youtube", core)
        elif "kodi" in text:
            launch_app("kodi", core)
        elif "playstore" in text or "appcenter" in text:
            launch_app("playstore", core)
        elif "twitch" in text:
            launch_app("twitch", core)
        elif "aufnehmen" in text or "guide" in text:
            launch_app("tv_guide", core)
        elif "disney" in text:
            launch_app("disney+", core)
        elif "mediathek" in text:
            if "zdf" in text or "zweite" in text:
                launch_app("zdf_mediathek", core)
            elif "erste" in text or "ard" in text:
                launch_app("erste_mediathek", core)
        elif "internet" in text or "browser" in text:
            launch_app("web", core)
        elif "fernsehen" in text or "tv" in text:
            run_command("watch_tv", core)

    else:
        run_command("google_assistant", core, body={"query": text})


def run_command(command, core, body=None):
    print("--------------------->> run")
    inf = core.module_storage("philips-tv")
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


def switch_hdmi(input_number, core):
    run_command("input_hdmi_" + str(input_number), core)


def send_digit(digit, core):
    run_command("digit_" + digit, core)


def send_color_key(color, core):
    run_command(color, core)


def get_powerstate(core):
    return run_command("powerstate", core)


def get_current_channel(core):
    return run_command("current_channel", core)


def get_current_app(core):
    return run_command("current_app", core)


def launch_app(name, core):
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
    run_command("launch_app", core, body=body)
