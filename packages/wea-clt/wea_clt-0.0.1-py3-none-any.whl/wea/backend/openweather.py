from requests import get
from datetime import datetime
from time import time
from wea.backend.config import get_user_config

BASE_URL_FORECAST = 'https://api.openweathermap.org/data/2.5/forecast?'
BASE_URL_TIMEMACHINE = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?'


def get_urls(location):
    """
    Returns a list of OpenWeather urls for the specified configuration.

    The location parameter must be a dict of the form
    { 'coord': [-34.6075682, -58.4370894], 'timezone_offset': -10800.0 }

    :param location: must contain the location's coordinates and timezone offset.
    :type location: dict
    """

    config = get_user_config()
    lat = location['coord'][0]
    lon = location['coord'][1]
    units = config['Preferences']['units']
    lang = config['Preferences']['lang'][0:2]
    api_key = config['API']['api_key']
    timezone = location['timezone_offset']

    current_time = int(time() - 1)
    utc_day = datetime.utcfromtimestamp(int(current_time)).strftime('%d')
    local_date = datetime.utcfromtimestamp(int(current_time) + timezone).strftime('%d')

    if local_date != utc_day and timezone < 0:
        request_time = int(current_time + timezone)
    else:
        request_time = current_time

    return [f'{BASE_URL_TIMEMACHINE}lat={lat}&lon={lon}&units={units}&lang={lang}&dt={request_time}&appid={api_key}',
            f'{BASE_URL_TIMEMACHINE}lat={lat}&lon={lon}&units={units}&lang={lang}&dt={current_time}&appid={api_key}',
            f'{BASE_URL_FORECAST}lat={lat}&lon={lon}&units={units}&lang={lang}&appid={api_key}']


def get_response_content(url):
    """
    Converts the response of the GET method to a dictionary.

    :param url: must provide json-encoded content when requested.
    :rtype: dict
    """

    response = get(url)
    if not response.ok:
        raise ValueError(response.json()['message'])
    return response.json()
