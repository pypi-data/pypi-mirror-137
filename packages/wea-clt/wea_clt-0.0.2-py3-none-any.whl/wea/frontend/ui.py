import re
from datetime import datetime
from babel.dates import format_date
from colorama import Style, Fore
from wea.frontend.art import ASCII_ART, BRIGHTYELLOW
from wea.backend.config import get_user_config
from wea.frontend.translations import parts_of_day

WEATHER_UNITS = {
    'default': {
        'temp': 'K',
        'wind': 'km/h',
        'visibility': 'km'
    },
    'metric': {
        'temp': '°C',
        'wind': 'km/h',
        'visibility': 'km'
    },
    'imperial': {
        'temp': '°F',
        'wind': 'mph',
        'visibility': 'mi.'
    }
}


class Temperature:
    """ Formats temperature data. """

    def __init__(self, temp, feels_like, unit):
        self.temp = temp
        self.feels_like = feels_like
        self.unit = unit

    def __str__(self):
        return f'{self.get_intensitiy_color(self.temp)}{self.temp}{Style.RESET_ALL}' \
               f'({self.get_intensitiy_color(self.feels_like)}{self.feels_like}{Style.RESET_ALL}) {self.unit}'

    def get_intensitiy_color(self, temp):
        if self.unit == WEATHER_UNITS['default']['temp']:
            temp = temp - 273.15
        elif self.unit == WEATHER_UNITS['imperial']['temp']:
            temp = int((temp - 32) * 5 / 9)

        if temp < -15:
            return Fore.LIGHTBLUE_EX
        if temp < 0:
            return Fore.LIGHTMAGENTA_EX
        if temp < 6:
            return Fore.LIGHTWHITE_EX
        if temp < 16:
            return Style.RESET_ALL
        if temp < 26:
            return BRIGHTYELLOW
        if temp < 33:
            return Fore.LIGHTGREEN_EX
        else:
            return Fore.RED


class Wind:
    """ Formats wind data. """

    def __init__(self, deg, speed, unit):
        self.deg = deg
        self.speed = int(speed * (3.6 if unit != WEATHER_UNITS['imperial']['wind'] else 1))
        self.unit = unit

    def __str__(self):
        return f'{self.get_wind_direction()}  ' \
               f'{self.get_intensitiy_color(self.speed)}{self.speed}{Style.RESET_ALL} {self.unit}'

    def get_wind_direction(self):
        deg = self.deg
        if 340 <= deg or deg < 20:
            return '↓'
        elif 20 <= deg < 70:
            return '↙'
        elif 70 <= deg < 110:
            return '←'
        elif 110 <= deg < 160:
            return '↖'
        elif 160 <= deg < 200:
            return '↑'
        elif 200 <= deg < 250:
            return '↗'
        elif 250 <= deg < 290:
            return '→'
        elif 290 <= deg < 340:
            return '↘'

    def get_intensitiy_color(self, speed):
        if self.unit == WEATHER_UNITS['imperial']['wind']:
            speed = speed * 1.609
        speed = int(speed)

        if 5 <= speed < 16:
            return BRIGHTYELLOW
        if 16 <= speed < 25:
            return Fore.LIGHTGREEN_EX
        if 25 <= speed < 30:
            return Fore.GREEN
        if 30 <= speed:
            return Fore.RED
        else:
            return ''


def format_weather_elem(weather_elem):
    """
    Formats weather conditions to make them printable.

    :param weather_elem: a dictionary with relevant weather conditions.
    :type weather_elem: dict
    """

    config = get_user_config()
    units = config['Preferences']['units']

    # Reorganizes fields
    if 'main' in weather_elem:
        for prop in weather_elem['main']:
            weather_elem[prop] = weather_elem['main'][prop]
        weather_elem['wind_speed'] = weather_elem['wind']['speed']
        weather_elem['wind_deg'] = weather_elem['wind']['deg']

    # Sets temperature
    temp = Temperature(int(weather_elem['temp']), int(weather_elem['feels_like']), WEATHER_UNITS[units]['temp'])
    weather_elem['temp'] = temp.__str__()
    temp_width = len(weather_elem['temp']) - get_escapes_length(weather_elem['temp'])

    # Sets pressure
    weather_elem['pressure'] = f'{weather_elem["pressure"]} hPa'
    pressure_width = len(weather_elem['pressure'])

    # Sets rain data
    rainfall_rate = 0
    if 'rain' in weather_elem:
        if '1h' in weather_elem['rain']:
            rainfall_rate = weather_elem['rain']['1h']
        elif '3h' in weather_elem['rain']:
            rainfall_rate = weather_elem['rain']['3h']
    weather_elem['rain'] = f'{rainfall_rate} mm'
    if 'pop' in weather_elem:
        weather_elem['rain'] += f' | {int(weather_elem["pop"] * 100)}%'
    rain_width = len(weather_elem['rain'])

    # Sets wind data
    wind = Wind(weather_elem['wind_deg'], weather_elem['wind_speed'], WEATHER_UNITS[units]['wind'])
    weather_elem['wind'] = wind.__str__()
    wind_width = len(weather_elem['wind']) - get_escapes_length(weather_elem['wind'])

    # Sets visibility data
    conversion_factor_km2mi = 1.609
    visibility_km = weather_elem['visibility'] / 1000
    visibility_km = visibility_km if units != 'imperial' else visibility_km / conversion_factor_km2mi
    visibility_km = round(visibility_km, 1)
    weather_elem['visibility'] = str(visibility_km) + ' ' + WEATHER_UNITS[units]['visibility']

    description_width = len(weather_elem['weather'][0]['description'])
    weather_elem['max_width'] = max(description_width, temp_width, pressure_width, rain_width, wind_width)

    return weather_elem


def print_forecast(forecast):
    """
    Prints weather forecast to terminal.

    :param forecast: a list of formatted weather elements with weather conditions for the next 5 days.
    :type forecast: list
    """

    timezone = forecast[0]['timezone_offset']
    lang = forecast[0]['lang']

    forecast_day = []
    for elem in forecast:
        date = format_date(datetime.utcfromtimestamp(elem['dt'] + timezone), 'EEE d MMM', locale=lang)
        if len(date) > 13:
            date = format_date(date, format='short', locale=lang)

        weather_card = get_weather_card(elem)
        format_card(weather_card, len(forecast_day) == 3)
        forecast_day.append(weather_card)

        if len(forecast_day) == 4:
            forecast_day_display = get_weather_day(forecast_day, date)
            print(forecast_day_display)
            forecast_day.clear()


def get_weather_card(weather_state):
    """
    Generates a printable version of a weather element.

    For convenience, the weather card is not a string but a list of strings, each one representing a line of the
    actual card.
    """
    config = get_user_config()
    conditions_display = config['Conditions display']
    art = get_art(weather_state)

    max_width = weather_state['max_width']
    description = weather_state['weather'][0]['description']
    description = description.capitalize() + ' ' * (max_width - len(description))
    weather_conditions = [description]

    for prop in conditions_display:
        if conditions_display[prop]:
            weather_state[prop] = str(weather_state[prop])
            weather_state[prop] += ' ' * (max_width - len(weather_state[prop]) +
                                          get_escapes_length(weather_state[prop]))
            weather_conditions.append(weather_state[prop])

    return get_weather_card_content(weather_conditions, art)


def get_weather_card_content(weather_conditions, art_name):
    """
    Adds ascii art to a weather element card.

    :param weather_conditions: a list containing a description and formatted weather conditions.
    :type weather_conditions: list[str]
    :param art_name: name of the ascii icon to be used from art.py.
    :type art_name: str
    """
    art = ASCII_ART[art_name]

    art_length = len(art[0]) - get_escapes_length(art[0])
    art_rows = len(art)
    weather_rows = len(weather_conditions)
    weather_length = len(weather_conditions[0])

    rows = max(art_rows, weather_rows)
    blank_rows_top_art = int((rows - art_rows) / 2)

    if art_rows < weather_rows:
        art = [' ' * art_length] * blank_rows_top_art + \
              art + \
              [' ' * art_length] * (weather_rows - blank_rows_top_art - art_rows)
    elif art_rows > weather_rows:
        weather_conditions += [' ' * weather_length] * (art_rows - blank_rows_top_art - weather_rows)

    return list(map('  '.join, zip(art, weather_conditions)))


def get_weather_day(forecast_day, date):
    """
    Generates printable weather report for a whole day.

    :param forecast_day: a list of weather cards.
    :type forecast_day: list[list[str]]
    :param date: formatted date with a maximum length of 13 characters.
    :type date: str
    """
    config = get_user_config()
    lang = config['Preferences']['lang']
    pod = [center_word(parts_of_day[lang][i], 14) for i in range(0, 4)]

    date = center_word(date, 13)
    res = f'                                                       ┌─────────────┐                                                       \n' \
          f'┌──────────────────────────────┬───────────────────────│{    date   }│───────────────────────┬──────────────────────────────┐\n' \
          f'│        {   pod[0]   }        │        {   pod[1]   } └──────┬──────┘ {   pod[2]   }        │        {   pod[3]   }        │\n' \
          f'├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤\n' \

    forecast_content = list(map(''.join, zip(*forecast_day)))
    res += ''.join(forecast_content)
    res += (f'└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘')
    return res


def format_card(card, is_last):
    """
    Gives final format to a weather card.

    :param card: a weather card.
    :type card: list[str]
    :param is_last: if True, '│\n' will be added to the end of each line.
    :type is_last: bool
    """

    for i, line in enumerate(card):
        line = '│' + center_word(line, 30)
        escapes_length = get_escapes_length(line)
        line_width = len(line) - escapes_length
        if line_width > 31:
            line = line[0:30 + escapes_length] + ('…' if i == 0 else ' ')
        if is_last:
            line += '│\n'
        card[i] = line


def center_word(word, line_length):
    """
    Adds lateral spaces to center a word to fit in line of 
    :param word: 
    :param line_length: 
    :return: 
    """
    extra_spaces = line_length - len(word) + get_escapes_length(word)
    return ' ' * int((extra_spaces + 1) / 2) + word + ' ' * int(extra_spaces / 2)


def get_escapes_length(text):
    """ Returns that ANSI escapes code take in a string """
    escape_codes = re.findall(r'\x1b\[\d+;?\d?m', text)
    return sum(map(len, escape_codes))


def get_art(weather_state):
    codes = {
        2: 'thunderstorm',
        3: 'drizzle',
        5: 'rain',
        6: 'snow',
        7: 'mist',
        800: 'clear',
        801: 'partial',
        802: 'partial',
        803: 'partial',
        804: 'clouds'
    }
    code = int(weather_state['weather'][0]['id'])
    if str(code)[0] != '8':
        code = int(str(code)[0])
    condition = codes[code]
    if str(code)[0] != '7':
        local_hour = int(
            datetime.utcfromtimestamp(weather_state['dt'] + weather_state['timezone_offset']).strftime('%H'))
        if weather_state['sunset_hour'] < local_hour or local_hour < weather_state['sunrise_hour']:
            condition = 'night-' + condition
        else:
            condition = 'day-' + condition
    return condition
