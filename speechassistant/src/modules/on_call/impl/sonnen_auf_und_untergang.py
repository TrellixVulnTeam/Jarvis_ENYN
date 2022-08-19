#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import json
import math
import random

import requests

from src.modules import ModuleWrapper


# toDo: use service

def handle(text: str, wrapper: ModuleWrapper) -> None:
    text = text.lower()
    if wrapper.analysis["town"] == "None" or wrapper.analysis["town"] == None:
        place = wrapper.local_storage.get("home_location")
    else:
        place = wrapper.analysis["town"]

    # Call Nominatim-API
    place = place.replace(" ", "+")
    r = requests.get(
        "https://nominatim.openstreetmap.org/search?q={0}&format=json".format(place)
    )
    if r.status_code == 200:
        try:
            response = json.loads(r.text)
            placeData = response[0]

            placeName = placeData["display_name"].split(", ")[0]
            lat = float(placeData["lat"])
            lon = float(placeData["lon"])

            if lat > 66.5 or lat < -66.5:
                wrapper.say(
                    speechVariation(
                        "Es ist mir etwas peinlich, aber für diesen Ort kann ich "
                        "leider den Sonnen auf beziehungsweise Untergang nicht "
                        "berechnen. Dafür ist mein hinterlegter Algorithmus nicht "
                        "ausgelegt worden."
                    )
                )
            else:
                datetimeTemp = wrapper.analysis["datetime"]

                datestr = datetimeTemp.strftime("%Y%m%d")
                day_of_year = int(datetimeTemp.strftime("%j"))
                if 88 < day_of_year < 298:
                    timezone = 2
                else:
                    timezone = 1
                sT = sunsetTimes(lat, lon, day_of_year, timezone)
                sunrise, sunset = sT.converted
                wrapper.say(
                    speechVariation(
                        "In {0} geht die Sonne [nach meinen Berechnungen|] um "
                        " {1} Uhr {2} auf und um {3} Uhr {4} wieder unter. Du "
                        "kannst also volle {5} Stunden und {6} Minuten "
                        "Tageslicht genießen.".format(
                            placeName,
                            round(sunrise // 60),
                            round(sunrise % 60),
                            round(sunset // 60),
                            round(sunrise % 60),
                            round((sunset - sunrise) // 60),
                            round((sunset - sunrise) % 60),
                        )
                    )
                )
        except IndexError:
            wrapper.say(
                speechVariation(
                    "Oh je, ich konnte zu [deinem angefragten Ort|] {0} leider keine"
                    "Position[sdaten|] finden. Vielleicht willst du es mit einer"
                    "anderen Aussprache-Variante ausprobieren?".format(place)
                )
            )
    else:
        wrapper.say(
            speechVariation(
                "Oh, ich habe gerade [Probleme|Schwierigkeiten], "
                "[an die Koordinaten zu kommen|die Koordinaten zu übersetzen]. "
                "Vielleicht probierst du es einfach später nochmal[, okay|]?"
            )
        )


def is_valid(text):
    text = text.lower()
    if "sonne" in text and ("auf" in text or "unter" in text):
        return True
    else:
        return False
