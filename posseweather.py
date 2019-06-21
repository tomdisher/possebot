"""
example plugin for weather
"""

import plugins
import requests
import json
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
    
def forecast(bot, event, *args):
    """
    /bot/forecast 
    """
    forecast_string=get_forecast(args[0])
    yield from bot.coro_send_message(
        event.conv,
        _("{}").format(
            forecast_string, 'yay'))


def get_forecast(zipcode, country='us'):
    url = openweather_base_url+'forecast/daily?zip='+zipcode+','+country+'&appid='+_internal['openweathermap_apikey']+'&units=imperial&cnt=3'
    result = requests.get(url).json()
    forecast_string = ''
    for day in result['list']:    
        ts = int(day['dt'])           
        utc_time = datetime.fromtimestamp(ts, timezone.utc)
        local_time = utc_time.astimezone() 
        high = day['temp']['day']
        low = day['temp']['night']
        forecast_date = local_time.strftime("%m/%d")
        description = day['weather'][0]['description']
        forecast_string += f"{forecast_date}: High: {high} Low: {low} {description}\n"
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
        if 'gust' in result['wind']:
            gust = result['wind']['gust']
        weather_data = "Sky: {}\nTemp: {} F\n Wind Speed: {} mph\n Wind Gusts: {} mph\n".format(
		result['weather'][0]['description'],
                result['main']['temp'],
                result['wind']['speed'], 
		gust)
    yield from bot.coro_send_message(
        event.conv,
        _("{}").format(
            weather_data, 'yay'))

