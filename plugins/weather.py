import requests
import os

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
        self._base_url = 'api.openweathermap.org/data/2.5/{query}&appid={api_key}&lang=de&units=metric'.format(api_key=api_key)
        # self._weather_icons_url = 'http://openweathermap.org/img/wn/{code}@2x.png'

    def query_current_weather(self, city='Bad Säckingen'):
        query = 'weather?q={city}'.format(city)
        url = self._base_url.format(query)
        res = requests.get(url)
        response_data = res.text()
        weather_description = str(response_data['weather']['description'])
        weather_icon_name = str(response_data['weather']['main']).lower()
        weather_icon = WEATHER_ICONS.get(weather_icon_name, None)
        temperature = str(response_data['main']['temp'])
        message_text = f'Hallo, Marco. Hier ist das Wetter für heute.\n {weather_icon} {temperature} Grad, {weather_description}.'
        return message_text
