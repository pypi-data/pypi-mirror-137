from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import time
from colorama import init, deinit
from wea.backend.openweather import get_urls, get_response_content
from wea.frontend.translations import location_prologue
from wea.backend.config import get_user_config
import wea.frontend.ui as ui

MORNING = [7, 8, 9]
NOON = [11, 12, 13]
EVENING = [17, 18, 19]
NIGHT = [21, 22, 23]
PARTS_OF_DAY = MORNING + NOON + EVENING + NIGHT


class Weather:
    """
    Class containing raw and formatted OpenWeather's API response.

    Basic usage::

        >>> weather = Weather(location, 'current')
        >>> weather.get_weather_response()
        >>> weather.print_weather()
        Weather forecast for: Buenos Aires
           .-.     Light rain
          (   ).   24(24) °C
         (___(__)  →  3 km/h
        ‚‘‚‘‚‘‚‘   1006 hPa
        ‚’‚’‚’‚    81
                   10.0 km

    Attributes

    •response_list : list
        a list of JSON responses from OpenWeather, converted to dicts.
    •current : dict
        a formatted weather element.
    •forecast : list
        a list of formatted weather elements with weather conditions for the next 5 days.
    •city : dict
        OpenWeather's info about the location requested, containing sunrise and sunset hour.
    •weather_type : str
        must be either 'current' or 'forecast'. Otherwise, both reports are generated.
    """

    response_list = []
    current = {}
    forecast = []
    weather_type = ''
    city = {}

    def __init__(self, location):
        """
        Generates an empty Weather object.

        The location parameter must be a dict of the form
        { 'coord': [-34.6075682, -58.4370894], 'name': 'Buenos Aires', 'timezone_offset': -10800.0 }

        :param location: a dict containing the location's name, coordinates and timezone offset.
        :type location: dict
        """
        self.location = location
        config = get_user_config()
        self.lang = config['Preferences']['lang']
        self.units = config['Preferences']['units']
        self.api_key = config['API']['api_key']

    def get_weather_response(self):
        """
        Initializes self.response_list with the OpenWeather API\'s response.

        :raises ValueError: if the location provided is invalid or the API key is not set.
        """
        config = get_user_config()
        api_key = config['API']['api_key']

        if 'coord' not in self.location:
            raise ValueError('Please, set a location using wea.py -l {location} or provide one as an argument: '
                             'wea {location}')
        elif not api_key:
            raise ValueError('Please, provide your OpenWeather API key. You can get one for free with an OpenWeather '
                             'account: https://home.openweathermap.org/api_keys')
        else:
            timemachine_url1, timemachine_url2, forecast_url = get_urls(self.location)
            urls = [timemachine_url2, forecast_url]
            if timemachine_url1 != timemachine_url2:
                urls = [timemachine_url1] + urls

            if self.weather_type == 'current':
                self.response_list = [get_response_content(timemachine_url2)]
            else:
                with ThreadPoolExecutor(max_workers=3) as pool:
                    self.response_list = list(pool.map(get_response_content, urls))

    def handle_response(self):
        """ Initializes self.current and self.forecast if API\'s response exists. """

        if not self.response_list:
            raise ValueError('Could not find API\'s response. Did you use Weather.get_weather_response()?')

        timemachine_list = self.response_list[0]['hourly'] + (
            self.response_list[1]['hourly'] if len(self.response_list) > 3 else [])
        if self.weather_type == 'current' or not self.weather_type:
            self.current = self.response_list[0]['current']
        if self.weather_type == 'forecast' or not self.weather_type:
            self.forecast = timemachine_list + self.response_list[-1]['list']
            self.city = self.response_list[-1]['city']

        if self.current:
            self.handle_current()

        if self.forecast:
            self.handle_forecast()

    def print_weather(self):
        """ Prints existing weather reports. """

        init()
        if not self.current and not self.forecast:
            raise ValueError('Could not find any weather report to print. Did you use Weather.handle_response()?')

        print(location_prologue[self.lang], self.location['name'].title())
        if self.current:
            print(*ui.get_weather_card(self.current), sep='\n')
        if self.forecast:
            ui.print_forecast(self.forecast)
        deinit()

    def handle_current(self):
        timezone = self.location['timezone_offset']
        self.current['timezone_offset'] = self.location['timezone_offset']  # ¿inútil?
        self.current['sunrise_hour'] = int(
            datetime.utcfromtimestamp(self.current['sunrise'] + timezone).strftime('%H'))
        self.current['sunset_hour'] = int(
            datetime.utcfromtimestamp(self.current['sunset'] + timezone).strftime('%H'))

        self.current = ui.format_weather_elem(self.current)

    def handle_forecast(self):
        timezone = self.location['timezone_offset']
        uncovered_pod = [NIGHT, EVENING, NOON, MORNING]
        first_forecast = next(elem.copy() for elem in self.forecast if 'main' in elem)
        first_forecast_hour = int(datetime.utcfromtimestamp(first_forecast['dt'] + timezone).strftime('%H'))

        new_list = []
        # Filters forecast elements
        for elem in self.forecast:
            elem['timezone_offset'] = timezone
            elem['lang'] = self.lang
            elem['sunrise_hour'] = int(datetime.utcfromtimestamp(self.city['sunrise'] + timezone).strftime('%H'))
            elem['sunset_hour'] = int(datetime.utcfromtimestamp(self.city['sunset'] + timezone).strftime('%H'))

            elem_date = datetime.utcfromtimestamp(elem['dt'] + timezone).date()
            elem_hour = int(datetime.utcfromtimestamp(elem['dt'] + timezone).strftime('%H'))
            local_date = datetime.utcfromtimestamp(time() + timezone).date()

            if elem_date == local_date:
                # Covering today's weather with data from timemachine's API
                if uncovered_pod and elem_hour in uncovered_pod[-1]:
                    new_list.append(ui.format_weather_elem(elem))
                    uncovered_pod.pop()

            elif elem_date > local_date:
                # Fills possible gap between timemachine and forecast responses
                if uncovered_pod and first_forecast_hour not in uncovered_pod[-1]:
                    new_list.append(self.current)
                    uncovered_pod.clear()

                # Default control logic for self.ther elem
                elif elem_hour in PARTS_OF_DAY:
                    new_list.append(ui.format_weather_elem(elem))

        self.forecast = new_list
