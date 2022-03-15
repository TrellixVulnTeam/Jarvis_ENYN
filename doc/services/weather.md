!!! This document is only a rough overview of all functions of the weather service that can be used from the outside.    
    For more detailed info, look directly into the file, the functions were documented in detail                      !!!

### Weather
| Function                                                                                                                          | Usage                                                         |
|-----------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------|
 | get_sunrise_sunset(self, city_name: str = None, lat: int = None, lon: int = None, day_offset: int = 0) -> set[datetime, datetime] | Returns sunrise and sunset of a city as datetime objects      |
 | get_current_weather(self, city_name: str = None, lat: int = None, lon: int = None) -> dict                                        | Returns current weather data                                  |
 | get_forcast_of_one_day(self, day_offset, city_name=None, lat=None, lon=None) -> dict                                              | Returns forecast of one day                                   |
 | get_current_weather_string(self, city=None, lat=None, lon=None) -> str                                                            | Returns current weather data as a string in german speech     |
 | get_hourly_forecast_string(self, city: str = None, lat: float = None, lon: float = None, offset: int = 1) -> str                  | Returns forecast of one hour in <offset> hours                |
 | get_daily_forecast_string(self, city: str = None, lat: float = None, lon: float = None, offset: int = 1) -> str                   | Returns forecast of one day in <offset> days                  |
 | get_weather_conditions(self) -> str                                                                                               | Returns indications of future weather development             |
 | get_offset_minutes(self) -> int                                                                                                   | Returns the time since the last update of the data in minutes |
 | get_offset_hours(self) -> int                                                                                                     | Returns the time since the last update of the data in hours   |