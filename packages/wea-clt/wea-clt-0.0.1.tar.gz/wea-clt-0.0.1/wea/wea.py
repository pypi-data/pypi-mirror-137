#!/usr/bin/env python3
import argparse
from sys import argv, exit
from wea.backend.weather import Weather
from wea.backend.config import set_location, set_unit_system, set_language, get_set_location, show_config, set_api_key
from wea.backend.nominatim import get_geocoding_response, format_location


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('-c', '--current', action='store_true',
                   help='Shows current weather for the set location.')
group.add_argument('-f', '--forecast', action='store_true',
                   help='Shows weather forecast for the set location.')
group.add_argument('-l', '--location', metavar='', type=str, action='store', nargs='+',
                   help='Sets a location.')
group.add_argument('-u', '--units', metavar='[default | metric | imperial]', action='store',
                   help='Changes unit system')
group.add_argument('--lang', metavar='', action='store', help='Sets new language.')
group.add_argument('-k', '--key', metavar='', action='store', help='Sets the OpenWeather API key.')
group.add_argument('--config', action='store_true', help='Shows current user configuration path and content.')

args, unknown = parser.parse_known_args()


def main():

    try:
        # User configuration
        if args.location:
            set_location(' '.join(args.location))
        elif args.units:
            set_unit_system(args.units)
        elif args.lang:
            set_language(args.lang)
        elif args.config:
            show_config()
        elif args.key:
            set_api_key(args.key)
        else:
            # Gets location if provided as an argument
            location = list(filter(lambda elem: elem[0] != '-', argv[1:]))
            location = ' '.join(location)

            if not location:
                location = get_set_location()
            else:
                location = get_geocoding_response(location)[0]
                location = format_location(location)

            # Gets weather data and displays it
            weather = Weather(location)
            if args.current:
                weather.weather_type = 'current'
            elif args.forecast:
                weather.weather_type = 'forecast'
            weather.get_weather_response()
            weather.handle_response()
            weather.print_weather()

    except KeyboardInterrupt:
        print('Aborted by user.')
        exit()

    except ValueError as error:
        for arg in error.args:
            print(arg)
        exit()


if __name__ == '__main__':
    main()
