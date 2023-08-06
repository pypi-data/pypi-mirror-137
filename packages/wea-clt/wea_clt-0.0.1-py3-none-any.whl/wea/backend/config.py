import json
import os
from difflib import get_close_matches
from pick import pick
from functools import lru_cache
from pprint import pprint
from wea.frontend import translations
from wea.backend import nominatim

ROOT = os.path.abspath(os.path.dirname(__file__))


@lru_cache(maxsize=1)
def get_user_config():
    """
    Returns user's configuration or creates its file if not found.

    :rtype: dict
    :except FileNotFoundError: if configuration file doesn't exist.
    """

    try:
        with open(os.path.join(ROOT, 'user_config.json'), 'r') as config_file:
            return json.loads(config_file.read())
    except FileNotFoundError:
        create_config_file()
        print('Configuration file created. Don\'t forget to set a location!')
        exit()


def get_set_location():
    return get_user_config()['Location']


def show_config():
    """
    Shows configuration file's path and content.
    """

    config = get_user_config()
    print('Path:', os.path.join(ROOT, 'user_config.json'))
    print('Configuration:')
    pprint(config)


def create_config_file():
    """
    Creates a default configuration file.
    """

    default_display = {'temp': True,
                       'wind': True,
                       'pressure': True,
                       'humidity': True,
                       'visibility': True}
    config = {'API': {'api_key': ''},
              'Location': {},
              'Conditions display': default_display,
              'Preferences': {'lang': 'en', 'units': 'metric'}}
    with open(os.path.join(ROOT, 'user_config.json'), 'w') as config_file:
        json.dump(config, config_file, indent=4)


def add_config(new_config):
    """
    Updates user configuration.

    :param new_config: must be of the form { 'section': {'config element': 'new config'} }
    :type new_config: dict
    """

    config = get_user_config()

    for section in new_config:
        for key in new_config[section]:
            config[section][key] = new_config[section][key]

    with open(os.path.join(ROOT, 'user_config.json'), 'w') as config_file:
        json.dump(config, config_file, indent=4)


def set_location(location_in):
    """
    Lets user choose a location to update the configuration file.

    :param location_in: a textual description of the location.
    :type location_in: str
    """

    # Gets places from Nominatim
    possible_places = nominatim.get_places(location_in)
    places_names = list(possible_places.keys())

    config = get_user_config()
    lang = config['Preferences']['lang'][0:2]

    try:
        if not possible_places:
            raise ValueError(f'{translations.unknown_location[lang]}')
        else:
            # Shows options
            option, chosen = pick(places_names, 'Choose a location: ')

        # Updates location
        location_name = places_names[chosen]

        add_config({'Location': possible_places[location_name]})
        print(f'{translations.location[lang]}: {places_names[chosen]}')

    except ValueError:
        print(ValueError)


def set_unit_system(system):
    systems = ['default', 'metric', 'imperial']
    if system not in systems:
        print('Invalid unit system (available: default, metric, imperial).')
    else:
        new_config = {'Preferences': {'units': system}}
        add_config(new_config)
        print(f'New unit system: {system}.')


def set_language(lang):
    lang = lang.lower()
    config = get_user_config()
    current_lang = config['Preferences']['lang']
    location_name = config['Location']['full_name']
    if lang not in translations.lang_codes.keys():
        close_matches = get_close_matches(lang, translations.lang_codes.keys(), n=1)
        print('Invalid language' + (f', did you mean "{close_matches[0]}"?' if close_matches else '.'))
    elif current_lang not in [lang, translations.lang_codes[lang]]:
        new_config = {'Preferences': {'lang': translations.lang_codes[lang]}}
        add_config(new_config)
        location_new_language = nominatim.get_geocoding_response(location_name)[0]
        location_new_language = nominatim.format_location(location_new_language)
        add_config({'Location': location_new_language})

        print(f'New language: {lang}.')
    else:
        print('This language is already set.')


def set_api_key(api_key):
    new_config = {'API': {'api_key': api_key}}
    add_config(new_config)
    print('API key set.')
