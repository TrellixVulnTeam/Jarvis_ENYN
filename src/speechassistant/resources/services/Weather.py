import logging
from threading import Thread
from datetime import datetime
from datetime import timedelta
import requests
import time


class Weather:
    def __init__(self, _api_key, _city, _skills):
        self.__api_key = _api_key
        self.__minutely_forecast = None
        self.__hourly_forecast = None
        self.__daily_forcast = None
        self.__sunrise_sunset = None
        self.__skills = _skills
        self.__geo_data = self.__skills.get_data_of_city(_city)
        self.__last_updated = datetime.now()
        self.city = _city
        self.old_weather_inf = []
        self.current_weather = None

        self.updating = True

    def start(self) -> None:
        logging.info("[ACTION] Starting weather module...")
        thr = Thread(target=self.run)
        thr.daemon = True
        thr.start()

    def run(self) -> None:
        while self.updating:
            self.__update_all()
            time.sleep(3600)

    """Returns sunrise and sunset of a city as datetime objects 
        Args:
            city_name   (string): name of searched city
            lat         (int)   : lat of searched city
            lon         (int)   : lon of searched city
            day_offset  (int)   : offset of day
            
        Returns:
            set                 : sunrise and sunset as each datetime.datetime() objects
        
        Exceptions:
            ValueError()        : raises if just one of lat and lon is given
    """
    def get_sunrise_sunset(self, city_name: str = None, lat: int = None, lon: int = None, day_offset: int = 0) -> set[datetime, datetime]:
        if city_name is None and lat is None and lon is None:
            # user has not specified any geo data, so use the position of the system
            data = self.__daily_forcast[day_offset]
        elif city_name is not None or (lat is not None and lon is not None):
            # at least one of both geo data is known
            data = self.get_forcast_of_one_day(day_offset, city_name, lat, lon)['sys']
        else:
            # if just one of lat and lon are known, the get_forecast_of_one_day() is going to throw an ValueError(),
            # which is further propagated by this function
            data = self.get_forcast_of_one_day(day_offset, city_name, lat, lon)['sys']

        return {datetime.fromtimestamp(data["sunrise"]), datetime.fromtimestamp(data["sunset"])}

    """Returns current weather data
        Args:
            city_name   (string): name of searched city
            lat         (int)   : lat of searched city
            lon         (int)   : lon of searched city

        Returns:
            dict                : returns dict with current weather data

        Exceptions:
            ValueError()        : raises if just one of lat and lon is given
    """
    def get_current_weather(self, city_name: str = None, lat: int = None, lon: int = None) -> dict:
        if city_name is None and lat is None and lon is None:
            self.__update_all()
            return self.current_weather
        if city_name is not None:
            return self.__get_current_weather(city_name)
        elif lat is not None and lon is not None:
            city_name = self.__skills.get_data_of_lat_lon(lat, lon)["city"]
            return self.__get_current_weather(city_name)
        else:
            raise ValueError('Got just one of lat and lon, but both are necessary!')

    """Returns forecast of one day
        Args:
            day_offset  (int)   : offset of day
            city_name   (string): name of searched city
            lat         (int)   : lat of searched city
            lon         (int)   : lon of searched city

        Returns:
            dict                 : forecast of day with offset

        Exceptions:
            None
    """
    def get_forcast_of_one_day(self, day_offset, city_name=None, lat=None, lon=None) -> dict:
        if day_offset > 7:
            raise ValueError("Day offset was higher than 7.")
        if city_name is None and lat is None and lon is None:
            return self.__daily_forcast[day_offset]
        else:
            if city_name is not None:
                geo_data = self.__skills.get_data_of_city(self.city)
                lat = geo_data["lat"]
                lon = geo_data["lon"]
            url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly&appid={self.__api_key}&lang=de&units=metric'
            data = requests.get(url).json()
            return data["daily"][day_offset]

    def get_forcast_of_range(self, from_offset, until_offset, lat=None, lon=None):
        pass

    """Returns current weather data as a string in german speech
        Args:
            city   (string): name of searched city
            lat         (int)   : lat of searched city
            lon         (int)   : lon of searched city

        Returns:
            str                 : current weather data in german speech

        Exceptions:
            None
    """
    def get_current_weather_string(self, city=None, lat=None, lon=None):
        _current_weather = self.get_current_weather(city, lat, lon)
        weather_id = _current_weather["weather"][0]["id"]
        weather_description = "Es gab leider ein Problem in der Analyse der Wetterdaten. Bitte versuche es zu einem " \
                              "späteren Zeitpunkt erneut! "
        temp_inf = f'bei {int(_current_weather["temp"])}°C'
        if city is None:
            city = self.city
        if weather_id in self.Statics.will_be_description_map.keys():
            weather_description = f'In {city} gibt es {self.Statics.will_be_description_map.get(weather_id)} {temp_inf}.'
        elif weather_id in self.Statics.give_description_map.keys():
            weather_description = f'In {city} gibt es {self.Statics.give_description_map.get(weather_id)} {temp_inf}.'
        elif weather_id in self.Statics.will_description_map.keys():
            weather_description = f'In {city} ist es {self.Statics.will_description_map.get(weather_id)} {temp_inf}.'
        return weather_description

    """Returns forecast of one hour in <offset> hours
        Args:
            city        (string): name of searched city
            lat         (int)   : lat of searched city
            lon         (int)   : lon of searched city
            offset      (int)   : offset of hours

        Returns:
            str                 : forecast of one hour in german speech

        Exceptions:
            ValueError()        : raises if just one of lat and lon is given
    """
    def get_hourly_forecast_string(self, city: str = None, lat: float = None, lon: float = None, offset: int = 1) -> str:
        if city is None and lat is None and lon is None:
            data_offset: int = offset + round(self.get_offset_hours())
            if data_offset > 47:
                self.__update_all()
                data_offset = offset
            _forecast = self.__hourly_forecast[data_offset]
        elif city is not None and city is not self.city:
            # since the data is retrieved anew, there is no "delay" of the data and
            # self.get_offset_hours() does not have to be observed
            if offset > 47:
                raise ValueError('Offset too big! Choose an offset between 0 and 47')
            geo_data: dict = self.__skills.get_data_of_city(city)
            url: str = f'https://api.openweathermap.org/data/2.5/onecall?lat={geo_data["lat"]}&lon={geo_data["lon"]}&units=metric&appid={self.__api_key}&lang=de '
            _forecast = requests.get(url).json()["hourly"][offset]
        elif lat is not None and lon is not None:
            # since the data is retrieved anew, there is no "delay" of the data and
            # self.get_offset_hours() does not have to be observed
            url: str = f'https://api.openweathermap.org/data/2.5/onecall?lat={"lat"}&lon={"lon"}&units=metric&appid={self.__api_key}&lang=de'
            city: str = self.__skills.get_data_of_lat_lon(lat, lon)['city']
            _forecast = requests.get(url).json()["hourly"][offset]
        else:
            raise ValueError()
        return self.__get_weather_string(_forecast, city, hours_offset=offset)

    """Returns forecast of one day in <offset> days
        Args:
            city        (string): name of searched city
            lat         (int)   : lat of searched city
            lon         (int)   : lon of searched city
            offset      (int)   : offset of days

        Returns:
            str                 : forecast of one day in german speech

        Exceptions:
            ValueError()        : raises if just one of lat and lon is given
    """
    def get_daily_forecast_string(self, city: str = None, lat: float = None, lon: float = None, offset: int = 1):
        temp_offset = self.get_offset_hours()
        offset += int(temp_offset / 24)

        if temp_offset > 18:
            offset += 1

        if city is None and lat is None and lon is None:
            # since the data is queried every hour, it should never happen that the data is so outdated.
            # For the sake of functional security, the offset is nevertheless checked so that future changes should
            # work as well
            data_offset = offset + round(self.get_offset_hours() / 24)
            if data_offset > 7:
                self.__update_all()
                data_offset = offset
            _forecast = self.__daily_forcast[data_offset]
        elif city is not None and city is not self.city:
            # since the data is retrieved anew, there is no "delay" of the data and
            # self.get_offset_ does not have to be observed
            if offset > 7:
                raise ValueError('Offset too big! Choose an offset between 0 and 7')
            geo_data: dict = self.__skills.get_data_of_city(city)
            url = f'https://api.openweathermap.org/data/2.5/onecall?lat={geo_data["lat"]}&lon={geo_data["lon"]}&units' \
                  f'=metric&appid={self.__api_key}&lang=de '
            _forecast = requests.get(url).json()["daily"][offset]
        elif lat is not None and lon is not None:
            # since the data is retrieved anew, there is no "delay" of the data and
            # self.get_offset_ does not have to be observed
            city = self.__skills.get_data_of_lat_lon(lat, lon)['city']
            url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&appid={self.__api_key}&lang=de '
            _forecast = requests.get(url).json()["daily"][offset]
        else:
            raise ValueError()
        if city is None:
            city = self.city
        return self.__get_weather_string(_forecast, city, days_offset=offset)

    """Returns indications of future weather development
        Args:
            None
        Returns:
            str:   indications of future weather development
        Exceptions:
            None
    """
    def get_weather_conditions(self) -> str:
        self.__update_all()
        now = datetime.now()
        output = ''
        if self.__minutely_forecast[0]['precipitation'] > 0:
            last_raining_index = 0
            for i in range(59):
                if self.__minutely_forecast[i]['precipitation'] > 0:
                    last_raining_index = i
            if last_raining_index < 15:
                output = f'Der Regen wird in etwa {last_raining_index} Minuten abgeklungen sein.'
            elif last_raining_index == 59:
                output = f'Nimm am besten einen Regenschirm mit. Der Regen dauert wahrscheinlich noch länger als eine Stunde an.'
        elif self.__minutely_forecast[0]['precipitation'] > 0:
            first_raining_index = 0
            for i in range(59):
                if self.__minutely_forecast[0]['precipitation'] > 0:
                    first_raining_index = i
                    break
            output = f'Es wird in etwa {first_raining_index} Minuten beginnen zu regnen. Nimm vielleicht einen Regenschirm mit.'

        max_uvi = 0

        for i in range(24 - now.hour):
            max_uvi = max(self.__hourly_forecast[i]['uvi'], max_uvi)

        if max_uvi >= 8:
            output += ' Creme dich unbedingt ein. Die Sonne scheint heute ziemlich stark.'
        elif max_uvi >= 6:
            output += ' Creme dich am besten ein. Die Sonne scheint heute stark.'
        elif max_uvi >= 4:
            output += ' Pass auf, die Sonne scheint heute mäßig stark. Villeicht solltest du dich eincremen.'

        return output

    """Returns the time since the last update of the data in minutes
        Args:
            None
        Returns:
            int:    time in minutes
        Exceptions:
            None
    """
    def get_offset_minutes(self) -> int:
        delta = datetime.now() - self.__last_updated
        return round(delta.seconds / 60)

    """Returns the time since the last update of the data in hours
        Args:
            None
        Returns:
            int:    time in hours
        Exceptions:
            None
    """
    def get_offset_hours(self) -> int:
        delta = datetime.now() - self.__last_updated
        offset: float = delta.seconds / 3600
        if delta.seconds % 3600 > 2700:
            offset += 1
        return round(offset)

    """Updates the current weather
            Args:
                city        (str)   : name of city, from which the prediction is
                lat         (int)   : lat of searched city
                lon         (int)   : lon of searched city
            Returns:
                dict                : current weather data              
            Exceptions:
                ValueError()        : raises if just one of lat and lon is given
        """

    def __get_current_weather(self, city: str = None, lat: int = None, lon: int = None) -> dict:
        if city is None and lat is None and lon is None:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={self.city}&units=metric&appid={self.__api_key}&lang=de'
            self.current_weather = requests.get(url).json()
            return self.current_weather

    """Returns the time since the last update of the data in minutes
        Args:
            _forecast   (dict): forecast, which is to be translated into a string
            city        (str) : name of city, from which the prediction is
            days_offset (int) : offset of days from the _forecast
            hours_offset(int) : offset of days from the _forecast
        Returns:
            str               : forecast in german speech                
        Exceptions:
            None
    """
    def __get_weather_string(self, _forecast: dict, city: str, days_offset: int = None, hours_offset: int = None) -> str:
        weather_id = _forecast["weather"][0]["id"]
        weather_description = "Es gab leider ein Problem in der Analyse der Wetterdaten. Bitte versuche es zu einem " \
                              "späteren Zeitpunkt erneut! "
        if type(_forecast["temp"]) is dict:
            temp_inf = f'bei {round(_forecast["temp"]["day"])}°C'
        else:
            temp_inf = f'bei {round(_forecast["temp"])}°C'
        if city is None:
            city = self.city
        if weather_id in self.Statics.will_be_description_map.keys():
            weather_description = f'In {city} wird es {self.__get_time_string(days_offset=days_offset, hours_offset=hours_offset)} {self.Statics.will_be_description_map.get(weather_id)} {temp_inf} geben. '
        elif weather_id in self.Statics.give_description_map.keys():
            weather_description = f'In {city} wird es {self.__get_time_string(days_offset=days_offset, hours_offset=hours_offset)} {self.Statics.give_description_map.get(weather_id)} {temp_inf} geben.'
        elif weather_id in self.Statics.will_description_map.keys():
            weather_description = f'In {city} wird es {self.__get_time_string(days_offset=days_offset, hours_offset=hours_offset)} {self.Statics.will_description_map.get(weather_id)} {temp_inf}.'
        return weather_description

    """Converts an offset (days, hours, minutes) into a time specification
            Args:
                days_offset     (int):      Number of days of the offset
                hours_offset    (int):      Number of hours of the offset
                minutes_offset  (int):      Number of minutes of the offset
            Returns:
                str:   indications of future weather development
            Exceptions:
                None
        """

    @staticmethod
    def __get_time_string(days_offset: int = None, hours_offset: int = None, minutes_offset: int = None):
        is_days_offset_none: bool = days_offset is None
        is_hours_offset_none: bool = hours_offset is None

        # normally you would write days_offset: int = 0, ... but if the user defines None for it, it crashes,
        # so I chose this way
        if days_offset is None:
            days_offset = 0
        if hours_offset is None:
            hours_offset = 0
        if minutes_offset is None:
            minutes_offset = 0

        time_delta: timedelta = timedelta(days=days_offset, hours=hours_offset, minutes=minutes_offset)

        if is_days_offset_none or time_delta.days == 0:
            time_string = 'heute'
        else:
            if time_delta.days == 1:
                time_string = 'morgen'
            elif time_delta.days == 2:
                time_string = 'übermorgen'
            else:
                return f'in {time_delta.days} Tagen'

        if not is_hours_offset_none:

            time_delta_hours = time_delta.seconds / 3600

            if time_delta_hours < 6:
                time_string += ' Nacht'
            elif time_delta_hours < 12:
                time_string += ' Früh'
            elif time_delta_hours < 17:
                time_string += ' Mittag'
            else:
                time_string += ' Abend'

        return time_string

    """Update all weather data
        Args:
            None
        Returns:
            None
        Exceptions:
            None
    """
    def __update_current_weather(self):
        url = f'https://api.openweathermap.org/data/2.5/weather?q={self.city}&units=metric&appid={self.__api_key}&lang=de'
        self.current_weather = requests.get(url).json()
        self.__last_updated = datetime.now()
        return self.current_weather

    """Update forecast data
        Args:
            None
        Returns:
            int:    time in minutes
        Exceptions:
            None
    """
    def __update_weather_forcast(self) -> dict:
        lat = self.__geo_data["lat"]
        lon = self.__geo_data["lon"]
        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&appid={self.__api_key}&lang=de'
        _forecast = requests.get(url).json()

        return _forecast

    """Updates all data from the API and stores the old ones into old_weather_inf
        Args:
            None
        Returns:
            None
        Exceptions:
            None
    """
    def __update_all(self):
        lat = self.__geo_data["lat"]
        lon = self.__geo_data["lon"]
        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&appid={self.__api_key}&lang=de'

        if len(self.old_weather_inf) >= 10 and self.old_weather_inf:
            self.old_weather_inf.pop(0)
        if self.__hourly_forecast:
            self.old_weather_inf.append(self.__hourly_forecast[0])

        try:
            weather_data = requests.get(url).json()
            self.current_weather = weather_data["current"]
            self.__minutely_forecast = weather_data["minutely"]
            self.__hourly_forecast = weather_data["hourly"]
            self.__daily_forcast = weather_data["daily"]
            self.__last_updated = datetime.now()
        except Exception as e:
            logging.warning(f'[WARNING] Problem when querying new data from Open-Weather-API: \n{str(e)}')

    class Statics:
        def __init__(self):
            pass

        # wird es ... geben
        will_be_description_map = {
            200: "ein Gewitter bei leichtem Regen",
            201: "ein regnerisches Gewitter",
            202: "ein Gewitter bei starkem Regen",
            210: "ein leichtes Gewitter",
            211: "ein stürmisches Gewitter",
            212: "ein starkes Gewitter",
            221: "ein sehr starkes Gewitter",
            230: "ein Gewitter bei leichtem Nieselregen",
            231: "ein Gewitter bei Nieselregen",
            232: "ein Gewitter bei starkem Nieselregen",
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

        # gibt es
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
            800: "klar",
            804: "bewölkt"
        }


if __name__ == "__main__":
    from src.speechassistant.resources.module_skills import Skills

    w = Weather('bd4d17c6eedcff6efc70b9cefda99082', 'Würzburg', Skills())
    th = Thread(target=w.run, args=())
    th.start()
    time.sleep(1)
    print(w.get_hourly_forecast_string(offset=0))
    print(w.get_hourly_forecast_string(city="Coburg", offset=0))
    print(w.get_hourly_forecast_string(offset=47))
    print(w.get_daily_forecast_string(offset=0))
    print(w.get_daily_forecast_string(city="Coburg", offset=0))
    print(w.get_daily_forecast_string(offset=7))

    print(w.get_sunrise_sunset())
    time.sleep(1)
    print(w.get_sunrise_sunset(day_offset=2))
