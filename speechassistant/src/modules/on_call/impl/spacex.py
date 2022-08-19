#!/usr/bin/env python3

from spacex_py import launches

from src.modules import ModuleWrapper, skills


def is_valid(text):
    hit_list = ["rakete", "spacex"]
    if any((hit for hit in hit_list if hit in text.lower())) is True:
        return True
    else:
        return False


def handle(text: str, wrapper: ModuleWrapper) -> None:
    hit_list = ["wann", "when"]

    if any((hit for hit in hit_list if hit in text.lower())) is True:
        # Get the launches launch
        got_launches, header = launches.get_launches()

        if wrapper.messenger_call is True:
            return_string = ""
            return_string += (
                    f"Time (UTC): " + got_launches[-1]["launch_date_utc"] + "\n"
            )
            wrapper.say(return_string)
            return

        else:
            day = got_launches[-1]["launch_date_utc"][8:10]
            month = got_launches[-1]["launch_date_utc"][5:7]
            minute = got_launches[-1]["launch_date_utc"][14:16]
            hour = got_launches[-1]["launch_date_utc"][11:13]

            return_string = ""
            return_string += f"Der nächste Start ist am {skills.Statics.numb_to_day_numb[day]} {skills.Statics.numb_to_day_numb[month]} "
            return_string += f"um {skills.Statics.numb_to_hour[hour]} Uhr {skills.Statics.numb_to_minute[minute]} U T C\n"
            wrapper.say(return_string)
            return

    hit_list1 = ["info", "info", "information"]
    hit1 = any((hit for hit in hit_list1 if hit in text.lower()))

    hit_list2 = ["nächste", "next"]  # klappt mit zum nächsten und nächster
    hit2 = any((hit for hit in hit_list2 if hit in text.lower()))

    if hit1 and hit2:
        got_launches, header = launches.get_launches()

        if wrapper.messenger_call:

            return_string = ""

            return_string += "Nächster start: \n"
            return_string += f"Mission ID: " + got_launches[-1]["mission_id"][0] + "\n"
            return_string += (
                    f"Launch site: "
                    + got_launches[-1]["launch_site"]["site_name_long"]
                    + "\n"
            )
            return_string += got_launches[-1]["rocket"]["rocket_name"] + "\n"
            return_string += (
                    f"Time (UTC): " + got_launches[-1]["launch_date_utc"] + "\n"
            )
            return_string += (
                    f"Telemetry: " + got_launches[-1]["telemetry"]["flight_club"] + "\n"
            )

            return_string += "\n\nDetails:\n"
            return_string += got_launches[-1]["details"] + "\n"

            return_string += "\n\nLinks:\n"
            return_string += got_launches[-1]["links"]["wikipedia"] + "\n"

            wrapper.say(return_string)
            return
        else:
            wrapper.say(
                wrapper.translate(got_launches[-1]["details"])
            )
            return

    hit_list = ["link", "links", "artikel"]
    hit1 = any((hit for hit in hit_list1 if hit in text.lower()))

    hit_list2 = ["nächster", "next"]
    hit2 = any((hit for hit in hit_list2 if hit in text.lower()))

    if hit1 is True and hit2 is True:
        got_launches, header = launches.get_launches()

        links = got_launches[-1]["links"]

        return_string = ""
        for key, value in links.items():
            return_string += f"{value}\n"

        wrapper.say(return_string)
        return
