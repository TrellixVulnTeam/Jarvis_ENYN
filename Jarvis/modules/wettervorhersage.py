

def handle(text, core, skills):
    if core.analysis['town'] != None:
        output = __prepare_output(core.analysis['town'], core.weather)


def __prepare_output(city, weather):
    weather_id = weather["weather"]["0"]["id"]
    weather_description = "Es gab leider ein Problem in der Analyse der Wetterdaten. Bitte versuche es zu einem späteren Zeitpunkt erneut!"
    temp_inf = f'bei einer Höchsttemperatur von {int(weather["temp"]["max"])}°C und einer Tiefsttemperatur von {int(weather["temp"]["max"])}°C'
    if weather_id in will_be_description_map.keys():
        weather_description = f'In {city} wird es {will_be_description_map.get(weather_id)} {temp_inf} geben'
    elif weather_id in give_description_map.keys():
        weather_description = f'In {city} gibt es {give_description_map.get(weather_id)} {temp_inf}'
    elif weather_id in will_description_map.keys():
        weather_description = f'In {city} wird es {will_description_map.get(weather_id)} {temp_inf}'
    return weather_description


# wird es ... geben
will_be_description_map = {
    200: "ein Gewitter bei leichtem Regen",
    201: "ein regnerisches Gewitter",
    202: "ein Gewitter mit starkem Regen",
    210: "ein leichtes Gewitter geben",
    211: "ein stürmisches Gewitter geben",
    212: "ein starkes Gewitter geben",
    221: "ein sehr starkes Gewitter",
    230: "ein Gewitter mit leichtem Nieselregen",
    231: "ein Gewitter mit Nieselregen",
    232: "ein Gewitter mit starkem Nieselregen",
    300: "leichten Nieselregen",
    301: "Nieselregen",
    302: "starken Nieselregen",
    310: "Nieselregen",
    311: "Nieselregen",
    312: "starken Nieselregen",
    313: "Schauerregen",
    314: "starke Schauerregen",
    321: "Nieselschauer"
}

#gibt es
give_description_map = {
    500: "leichten Regen",
    501: "mäßigen Regen",
    502: "starken Regen",
    503: "sehr starken Regen",
    504: "extremen Regen",
    511: "Eisregen",
    520: "leichte Regenschauer",
    521: "Regenschauer",
    522: "starke Regenschauer",
    531: "Regenschauer",
    600: "leichten Schnee",
    601: "Schnee",
    602: "starken Schnee",
    611: "Schneeregen",
    612: "Schneeregen",
    613: "Schneeregen",
    615: "leichten Regen und Schnee",
    616: "Regen und Schnee",
    620: "leichte Schneeschauer",
    621: "Schneeschauer",
    622: "starke Schneeschauer",
    731: "Staubaufwirbelungen",
    762: "Vulkanasche in der Luft",
    771: "Sturmböen",
    781: "einen Tornado",
    801: "ein paar Wolken",
    802: "vereinzelte Wolken",
    803: "vereinzelte Wolken"
}

# wird es
will_description_map = {
    701: "neblig",
    711: "verraucht",
    721: "trüb",
    741: "neblig",
    751: "sandig",
    761: "staubig",
    804: "bewölkt"
}

if __name__ == "__main__":
    from Jarvis.resources.Weather import Weather
    weather = Weather()
    print(__prepare_output("Würzburg", weather))