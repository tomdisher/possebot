"""
example plugin for weather
"""


import plugins
import requests
import json
import emoji
import geopandas
import geopy
from datetime import datetime, timezone
from geopy.geocoders import Nominatim

api_key=''
_internal = {}
openweather_base_url='https://api.openweathermap.org/data/2.5/'


def _initialise(bot):
    api_key = bot.get_config_option('openweathermap_apikey')
    if api_key:
        _internal['openweathermap_apikey'] = api_key
    plugins.register_user_command(["wz"])
    plugins.register_user_command(["forecast"])

def get_lat_long(location):
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(location)
    coordinates = {}
    if location != None:
        coordinates['latitude'] = location.latitude
        coordinates['longitude'] = location.longitude
    return coordinates

def get_forecast(location, country='us'):
    url = f"https://api.weather.gov/points/{location['latitude']},{location['longitude']}"
    print(f"url: {url}")
    forecast_url = requests.get(url).json()['properties']['forecast']
    print(f"forecast_url: {forecast_url}")
    forecast = requests.get(forecast_url).json()
    print(f"forecast is: {forecast}")
    forecast_string = ''
    for day in forecast['properties']['periods'][: -4]:
        temperature = day['temperature']
        forecast_date = day['name']
        description = day['shortForecast']
        wind = day['windSpeed']
        winddir = day['windDirection']
        shortForecast = day['shortForecast']
        icon = emoji_weather_icon(day['shortForecast'].lower())
        forecast_string += f"{icon} {forecast_date}: Temp: {temperature}\n Wind: {wind} {winddir}\n{shortForecast}\n"
    return forecast_string

def get_current_weather(location, country='us'):
    location = get_lat_long(location)
    result = get_forecast(location)
    return result

def wz(bot, event, *args):
    """
    /bot drewski to call
    """
    weather_data = ''
    print(event.user.__dict__)
    if len(args)==1:
        result = get_current_weather(args[0])
    yield from bot.coro_send_message(
        event.conv,
        _("{}").format(
            result, 'yay'))
def forecast(bot, event, *args):
    """
    /bot drewski to call
    """
    weather_data = ''
    print(event.user.__dict__)
    if len(args)==1:
        result = get_current_weather(args[0])
    yield from bot.coro_send_message(
        event.conv,
        _("{}").format(
            result, 'yay'))



def emoji_weather_icon(description):
    if 'clear' in description:
        return emoji.emojize(':sun:')
    elif 'mostly sunny' in description:
        return emoji.emojize(':sun_behind_large_cloud:')
    elif 'scattered clouds' in description:
        return emoji.emojize(':sun_behind_small_cloud:')
    elif 'few clouds' in description:
        return emoji.emojize(':sun_behind_small_cloud:')
    elif 'overcast clouds' in description:
        return emoji.emojize(':cloud:')
    elif 'light rain' in description:
        return emoji.emojize(':cloud_with_rain:')
    elif 'heavy rain' in description:
        return emoji.emojize(':cloud_with_rain:')
    elif 'rain' in description:
        return emoji.emojize(':cloud_with_rain:')
    elif 'thunderstorms' in description:
        return emoji.emojize(':cloud_with_lightning:')
    elif 'snow' in description:
        return emoji.emojize(':cloud_with_snow:')


