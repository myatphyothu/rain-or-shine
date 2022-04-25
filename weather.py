
import sys
import argparse
import json
from urllib import error, request
from urllib.parse import quote
import pprint
from configparser import ConfigParser
from py_utils.str_utils import StrUtil
from py_utils.io_utils import py_console


# from venv_check import in_virtualenv
# print(in_virtualenv())

OPEN_WEATHER_API_KEY = 'bcb76387410354ab0f47c81f3a85b3f3'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
API_REQUEST_SAMPLE = 'api.openweathermap.org/data/2.5/weather?q=New York&appid=bcb76387410354ab0f47c81f3a85b3f3'
KEYS_FILE = 'keys.ini'

create_query_url = lambda city,api_key,units : (f'{BASE_URL}?q={quote(StrUtil.camel_case_to_phrase(city))}&units={units}&appid={api_key}')

printer = pprint.PrettyPrinter(indent=4)


def get_api_key():
    config = ConfigParser()
    config.read(KEYS_FILE)
    if 'openweather' in config.keys():
        if 'api_key' in config['openweather']:
            return config['openweather']['api_key']
    return None


def get_cli_args():
    parser = argparse.ArgumentParser(description='gets weather and temperature information for a city')
    parser.add_argument('city_list', nargs='+', type=str, help='enter city name')
    parser.add_argument('-i', '--imperial', action='store_true', help='display the temperature in imperial units')
    return parser.parse_args()


def get_weather_data(query_url):
    try:
        rsp = request.urlopen(query_url)
    except error.HTTPError as httperror:
        if httperror.code == 401:
            return 401, 'Access denied. Check your API key.'
        elif httperror.code == 404:
            return 404, 'Can\'t find weather data for this city.'
        else:
            return httperror.code, 'Something went wrong.'

    data = rsp.read()
    try:
        return 0, json.loads(data)
    except json.JSONDecodeError:
        return -1, 'Could not read server response.'


def display_weather_data(data, imperial):
    city, description, icon, temperature = data['name'],data['weather'][0]['description'], data['weather'][0]['icon'], data['main']['temp']
    units = '°F' if imperial is True else '°C'

    # py_console.print_colorfully(f'{city:>20}', 'cyan')
    print(f'{city:>20}', end='')
    print(f'\t{description.capitalize():<20}', end=' ')
    print(f'({temperature}{units})')


if __name__ == '__main__':
    args = get_cli_args()
    api_key = get_api_key()

    if api_key is None:
        print('Error reading api key! Terminating app..')
        exit()

    resp_list = []
    for city in args.city_list:
        query_url = create_query_url(city, api_key, 'imperial' if args.imperial else 'metric')

        resp = get_weather_data(query_url)
        if resp[0] == 0:
            resp_list.append(resp[1])
        else:
            print(resp[0], resp[1])

    for resp in resp_list:
        display_weather_data(resp, args.imperial)



