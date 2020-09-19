import requests
import os
import json

WEATHER_ICONS = {
    'clear': u'☀️',
    'clouds': u'☁️',
    'rain': u'🌧️',
    'thunderstorm': u'⛈️',
    'snow': u'🌨️',
    'mist': u'🌫️',
}


class WeatherPlugin():
    def __init__(self):
        try:
            api_key = os.getenv("WEATHER_API_KEY")
        except:
            raise Exception('API Key not specified. Please check environment variables.')
        self._base_url = 'http://api.openweathermap.org/data/2.5/'
        self._url_trailer = f'&appid={api_key}&lang=de&units=metric'
        # self._weather_icons_url = 'http://openweathermap.org/img/wn/{code}@2x.png'

    def query_current_weather(self, city):
        query = f'weather?q={city}'
        url = f'{self._base_url}{query}{self._url_trailer}'
        res = requests.get(url)
        response_data = json.loads(res.text)
        weather_description = str(response_data['weather'][0]['description'])
        weather_icon_name = str(response_data['weather'][0]['main']).lower()
        weather_icon = WEATHER_ICONS.get(weather_icon_name, None)
        temperature = str(response_data['main']['temp'])
        message_text = f'Hallo, Marco. Hier ist das Wetter für heute in {city}.\n {weather_icon} {temperature} Grad, {weather_description}.'
        return message_text
