from src.database.connection import RoutineInterface
from src.models.user import User
from src.modules import Skills, ModuleWrapper
from src.services.light_systems.phue import PhilipsWrapper


def handle(text: dict, wrapper: ModuleWrapper, skills: Skills):
    ton: str = text.get("Ton")
    user: User = text.get("User")
    path: str = str(wrapper.path.joinpath("modules", "resources", "alarm", ton))
    
    __turn_on_lights(wrapper)

    __ring(wrapper, path)

    wrapper.say(__get_output_for_greeting_user(user))

    __start_after_alarm_routines(wrapper)


def __start_after_alarm_routines(wrapper):
    for routine in RoutineInterface().get_all_after_alarm():
        wrapper.start_module(name="start_routine", text=routine, user=wrapper.user)


def __turn_on_lights(wrapper):
    if wrapper.config["services"]["philips-hue"]["Bridge-IP"]:
        pw: PhilipsWrapper = PhilipsWrapper(wrapper.config["services"]["philips-hue"]["Bridge-IP"])
        pw.light_change_color(pw.light_names, "weiß")


def __ring(wrapper, path):
    try:
        wrapper.play(path=path, as_next=True)
    except FileNotFoundError:
        wrapper.say("Alarm! Alarm! Alarm! Aufstehen! Klingeling!")


def __get_output_for_greeting_user(user: User) -> str:
    user_announce: str = "" if not user else f" {user.first_name}"
    return f"Guten Morgen{user_announce}! Ich hoffe du hast gut geschlafen und wünsche dir einen tollen Tag"


def isValid(text):
    return False
