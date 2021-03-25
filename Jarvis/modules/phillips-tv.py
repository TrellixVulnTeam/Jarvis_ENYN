import subprocess

user = ''
password = ''
path = ''

def isValid(text):
    text = text.lower()
    if 'fernseh' in text:
        return True

def handle(text, core, skills):
    text = text.lower()

    if "hdmi" in text:
        pass
    elif "schalte" in text and "aus" in text:
        # it is not really "switch off" but "stand by"
        run_command('standby', core)

    elif ("schalte" in text or 'mach' in text) and "an" in text:
        run_command('power_on', core)

    elif "mute" in text or ("schalte" in text and "stumm" in text):
        run_command('mute', core)

    elif "schalte" in text:
        if "hoch" in text:
            run_command('channel_up', core)
        elif "runter" in text:
            run_command('channel_down', core)
        else:
            core.say("Ich habe leider nicht verstanden, wohin ich schalten soll.")

    elif "play" in text:
        run_command('play', core)

    elif "pause" in text:
        run_command('pause', core)

    elif "stop" in text:
        run_command('stop', core)

    elif "spul" in text:
        if "vor" in text:
            run_command('fast_forward', core)
        elif "zurück" in text:
            run_command('rewind', core)
        else:
            core.say("Ich habe leider nicht verstanden, wohin ich spulen soll.")

    elif 'bestätige' in text or 'stimme zu' in text:
        run_command('confirm', core)

    elif 'home' in text or 'übersicht' in text:
        run_command('home', core)

    elif 'einstellung' in text:
        run_command('options', core)

    elif ('nimm' in text and 'auf' in text) or 'record' in text:
        run_command('record', core)

    elif 'ambilight' in text or 'hintergrundbeleuchtung' in text:
        if 'an' in text:
            run_command('ambilight_on', core)
        elif 'aus' in text:
            run_command('ambilight_off', core)

    elif 'ist' in text and 'an' in text:
        if get_powerstate(core):
            core.say('Ja.')
        else:
            core.say('Nein.')

    elif 'öffne' in text:
        if 'netflix' in text:
            launch_app('netflix', core)
        elif 'amazon' in text and 'prime' in text:
            launch_app('amazon_prime', core)
        elif 'youtube' in text:
            launch_app('youtube', core)
        elif 'kodi' in text:
            launch_app('kodi', core)
        elif 'playstore' in text or 'appcenter' in text:
            launch_app('playstore', core)
        elif 'twitch' in text:
            launch_app('twitch', core)
        elif 'aufnehmen' in text or 'guide' in text:
            launch_app('tv_guide', core)
        elif 'disney' in text:
            launch_app('disney+', core)
        elif 'mediathek' in text:
            if 'zdf' in text or 'zweite' in text:
                launch_app('zdf_mediathek', core)
            elif 'erste' in text or 'ard' in text:
                launch_app('erste_mediathek', core)
        elif 'internet' in text or 'browser' in text:
            launch_app('web', core)
        elif 'fernsehen' in text or 'tv' in text:
            run_command('watch_tv', core)


def run_command(command, core):
    inf = core.module_storage('philips-tv')
    user = inf.get('user')
    password = inf.get('pass')
    path = core.path + '/modules/resources/tv/'
    print(f"user {user}, password {password}")
    base_command = f'python3 {path}phillips_wrapper.py --verbose False --user {user} --pass {password} --command ' + command
    subprocess.call(base_command.split(' '))


def switch_hdmi(input_number, core):
    run_command('input_hdmi_' + str(input_number), core)


def send_digit(digit, core):
    run_command('digit_' + digit, core)


def send_color_key(color, core):
    run_command(color, core)


def get_powerstate(core):
    return run_command('powerstate', core)

def get_current_channel(core):
    return run_command('current_channel', core)


def get_current_app(core):
    return run_command('current_app', core)


def launch_app(name, core):
    body = '--body '
    if name == 'netflix':
        body += "'" + '{\n"label":"Netflix","intent":{"component":{"packageName":"com.netflix.ninja","className":"com.netflix.ninja.MainActivity"},"action":"Intent{act=android.intent.action.MAINcat=[android.intent.category.LAUNCHER]flg=0x10000000pkg=com.netflix.ninjacmp=com.netflix.ninja/.MainActivity}"},"order":0,"id":"com.netflix.ninja.MainActivity-com.netflix.ninja","type":"app"}' + "'"
    elif name == 'youtube':
        body += '{"id":"com.google.android.apps.youtube.tv.activity.ShellActivity-com.google.android.youtube.tv",' \
                '"order":0,"intent":{"action":"Intent { act=android.intent.action.MAIN cat=[' \
                'android.intent.category.LAUNCHER] flg=0x10000000 pkg=com.google.android.youtube.tv ' \
                'cmp=com.google.android.youtube.tv/com.google.android.apps.youtube.tv.activity.ShellActivity }",' \
                '"component":{"packageName":"com.google.android.youtube.tv",' \
                '"className":"com.google.android.apps.youtube.tv.activity.ShellActivity"}},"label":"YouTube", "type":"app"}'
    elif name == 'amazon_prime':
        body += '{"id":"com.amazon.amazonvideo.livingroom","order":0,"intent":{"action":"Intent{' \
                'act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] flg=0x10000000 ' \
                'pkg=com.amazon.amazonvideo.livingroom }","component":{' \
                '"packageName":"com.amazon.amazonvideo.livingroom",' \
                '"className":"com.amazon.ignition.IgnitionActivity"}},"label":"Prime Video", "type":"app"}'
    elif name == 'kodi':
        body += '{"id":"org.xbmc.kodi","order":0,"intent":{"action":"Intent{act=android.intent.action.MAIN cat=[' \
                'android.intent.category.LAUNCHER] flg=0x10000000 pkg=org.xbmc.kodi }","component":{' \
                '"packageName":"org.xbmc.kodi","className":"org.xbmc.kodi.Splash"}},"label":"Kodi", "type":"app"}'
    elif name == 'playstore':
        body += '{"id":"com.google.android.finsky.tvmainactivity.TvMainActivity-com.android.vending",' \
                '"order":0,' \
                '"intent":{"action":"android.intent.action.MAIN"},' \
                '"component":{' \
                '"packageName":"com.android.vending",' \
                '"className":"com.google.android.finsky.tvmainactivity.TvMainActivity"}},' \
                '"label":"Play Store", "type":"app"}'
    elif name == 'twitch':
        body += '{"id":"com.fgl27.twitch.PlayerActivity-com.fgl27.twitch",' \
                '"order":0,' \
                '"intent":{"action":"android.intent.action.MAIN"},' \
                '"component":{' \
                '"packageName":"com.fgl27.twitch",' \
                '"className":"com.fgl27.twitch.PlayerActivity"}},' \
                '"label":"SmartTV Client for Twitch", "type":"app"}'
    elif name == "tv_guide":
        body += '{"id":"org.droidtv.channels.ChannelsActivity-org.droidtv.channels",' \
                '"order":0,' \
                '"intent":{"action":"android.intent.action.MAIN"},' \
                '"component":{' \
                '"packageName":"org.droidtv.channels",' \
                '"className":"org.droidtv.channels.ChannelsActivity"}},' \
                '"label":"SmartTV Client for Twitch", "type":"app"}'
    elif name == "disney+":
        body += '{"id":"com.bamtechmedia.dominguez.main.MainActivity-com.disney.disneyplus",' \
                '"order":0,' \
                '"intent":{"action":"android.intent.action.MAIN"},' \
                '"component":{' \
                '"packageName":"com.disney.disneyplus",' \
                '"className":"com.bamtechmedia.dominguez.main.MainActivity"}},' \
                '"label":"Disney+", "type":"app"}'
    elif name == "zdf_mediathek":
        body += '{"id":"com.zdf.android.mediathek.ui.splash.SplashActivity-com.zdf.android.mediathek",' \
                '"order":0,' \
                '"intent":{"action":"empty"},' \
                '"component":{' \
                '"packageName":"com.zdf.android.mediathek",' \
                '"className":"com.zdf.android.mediathek.ui.splash.SplashActivity"}},' \
                '"label":"ZDFmediathek", "type":"app"}'
    elif name == "erste_mediathek":
        body += '{"id":"com.daserste.daserste.MainActivity-de.daserste.apps.androidtv",' \
                '"order":0,' \
                '"intent":{"action":"empty"},' \
                '"component":{' \
                '"packageName":"de.daserste.apps.androidtv",' \
                '"className":"com.daserste.daserste.MainActivity"}},' \
                '"label":"Das Erste Mediathek", "type":"app"}'
    elif name == "web":
        body += '{"id":"jp.co.rarity.tvweb.MainActivity-jp.co.rarity.tvweb",' \
                '"order":0,' \
                '"intent":{"action":"empty"},' \
                '"component":{' \
                '"packageName":"jp.co.rarity.tvweb",' \
                '"className":"jp.co.rarity.tvweb.MainActivity"}},' \
                '"label":"TVWeb", "type":"app"}'
    print('----->launch_app ' + body)
    run_command('launch_app ' + body, core)
