"""
example plugin for weather
"""

import plugins
import requests
import json
import emoji
from datetime import datetime, timezone

api_key=''
_internal = {}
openweather_base_url='https://api.openweathermap.org/data/2.5/'


def _initialise(bot):
    api_key = bot.get_config_option('openweathermap_apikey')
    if api_key:
        _internal['openweathermap_apikey'] = api_key
    plugins.register_user_command(["wz"])
    plugins.register_user_command(["forecast"])
    plugins.register_user_command(["fullforecast"])
    
def fullforecast(bot, event, *args):
    conv_1on1 = yield from bot.get_1to1(event.user.id_.chat_id)
    forecast_string = get_fullforecast(args[0])
    yield from bot.coro_send_message(conv_1on1, _(forecast_string))

def forecast(bot, event, *args):
    """
    /bot/forecast 
    """
    forecast_string=get_forecast(args[0])
    yield from bot.coro_send_message(
        event.conv,
        _("{}").format(
            forecast_string, 'yay'))

def get_fullforecast(zipcode, country='us'):
    url = openweather_base_url+'forecast?zip='+zipcode+','+country+'&appid='+_internal['openweathermap_apikey']+'&units=imperial'
    result = requests.get(url).json()
    forecast_string = ''
    for day in result['list']:    
        ts = int(day['dt'])           
        utc_time = datetime.fromtimestamp(ts, timezone.utc)
        local_time = utc_time.astimezone() 
        high = day['main']['temp_max']
        low = day['main']['temp_min']
        forecast_date = local_time.strftime("%m/%d %-I %p")
        description = day['weather'][0]['description']
        icon = emoji_weather_icon(day['weather'][0]['description'])
        forecast_string += f"{icon} {forecast_date}: High: {high} Low: {low} {description}\n"
    return forecast_string    


def get_forecast(zipcode, country='us'):
    url = openweather_base_url+'forecast/daily?zip='+zipcode+','+country+'&appid='+_internal['openweathermap_apikey']+'&units=imperial&cnt=3'
    result = requests.get(url).json()
    forecast_string = ''
    for day in result['list']:    
        ts = int(day['dt'])           
        utc_time = datetime.fromtimestamp(ts, timezone.utc)
        local_time = utc_time.astimezone() 
        high = day['temp']['max']
        low = day['temp']['min']
        forecast_date = local_time.strftime("%m/%d")
        description = day['weather'][0]['description']
        icon = emoji_weather_icon(day['weather'][0]['description'])
        forecast_string += f"{icon} {forecast_date}: High: {high} Low: {low} {description}\n"
    return forecast_string    

def get_current_weather(zipcode, country='us'):
    url=openweather_base_url+'weather?'+'zip='+zipcode+','+country+'&appid='+_internal['openweathermap_apikey']+'&units=imperial'
    result = requests.get(url).json()
    return result
def wz(bot, event, *args):
    """
    /bot drewski to call
    """
    weather_data = ''
    print(event.user.__dict__)
    if len(args)==1:
        result = get_current_weather(args[0])
        print(type(result))
        print(result)
        gust = 'N/A'
        icon = emoji_weather_icon(result['weather'][0]['description'])
        if 'gust' in result['wind']:
            gust = result['wind']['gust']
        weather_data = "{} Sky: {}\nTemp: {} F\n Wind Speed: {} mph\n Wind Gusts: {} mph\n".format(
		icon,
                result['weather'][0]['description'],
                result['main']['temp'],
                result['wind']['speed'], 
		gust)
    yield from bot.coro_send_message(
        event.conv,
        _("{}").format(
            weather_data, 'yay'))


def emoji_weather_icon(description):
    if 'clear' in description:
        return emoji.emojize(':sun:')
    elif 'broken clouds' in description:
        return emoji.emojize(':sun_behind_large_cloud:')
    elif 'scattered clouds' in description:
        return emoji.emojize(':sun_behind_small_cloud:')
    elif 'few clouds' in description:
        return emoji.emojize(':sun_behind_small_cloud:')
    elif 'overcast clouds' in description:
        return emoji.emojize(':cloud:')
    elif 'light rain' in description:
        return emoji.emojize(':cloud_with_rain:')
    elif 'moderate rain' in description:
        return emoji.emojize(':cloud_with_rain:')
    elif 'rain' in description:
        return emoji.emojize(':cloud_with_rain:')
    elif 'thunder' in description:
        return emoji.emojize(':cloud_with_lightning:')
    elif 'snow' in description:
        return emoji.emojize(':cloud_with_snow:')

