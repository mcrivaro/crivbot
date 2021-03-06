from plugins import weather
import requests
import json
import re
import random


class Action():
    def __init__(self, bot_name, telegram_uri, message_complete_data):
        self.uri = telegram_uri
        self.message = message_complete_data['message']
        self.chat_id = self.message['chat']['id']
        self.text = str(self.message['text']).strip('/').lower() if 'text' in self.message else None
        self.sender_first_name = self.message['from']['first_name']
        self.matching_filters = [
            {'regex': r'buon\s*giorno|guten\s*morgen|ciao', 'function': 'good_morning'},
            {'regex': r'buona\s*notte|gute\s*nacht', 'function': 'good_night'},
            {'regex': r'hallo|ciao|hey|hi', 'function': 'say_hello'},
            {'regex': r'wetter\s*[in]*\s*([a-z\s]+[\u00C0-\u017Fa-z]+)*$', 'function': 'get_current_weather'}
        ]
        print(f'Received message: {self.text} in chat {self.chat_id}')

    def evaluate(self):
        for filter in self.matching_filters:
            regex = filter['regex']
            function = getattr(self, filter['function'])
            match = re.search(regex, self.text)
            if match:
                function_params = []
                for i in range(1, len(match.groups())+1):
                    if match.group(i) is not None:
                        function_params.append(match.group(i))
                function(*function_params)
        return 'No action found'

    def _send_message(self, text):
        text_msg_headers = {'content-type': 'application/json'}
        body = {
            'chat_id': self.chat_id,
            'text': text
        }
        res = requests.post(url=self.uri, data=json.dumps(body), headers=text_msg_headers)
        return res.text

    def good_morning(self):
        text = u'Buongiorno, {}\U0001F600'.format(self.sender_first_name)  # 1F600 = grinning smiley unicode
        self._send_message(text)
        return 'Good morning message sent.'

    def good_night(self):
        text = u'Buona notte, {}\U0001F634'.format(self.sender_first_name)
        self._send_message(text)
        return 'Good night message sent.'

    def say_hello(self):
        texts = [
            u'Hallo, {}\U0001F600'.format(self.sender_first_name),
            u'Yo, {}\U0001F60E'.format(self.sender_first_name),
            u'Ciao, {}\U0001F600'.format(self.sender_first_name)
        ]
        random.seed()
        text = random.choice(texts)
        self._send_message(text)
        return 'Greeting sent.'

    def get_current_weather(self, city='bad säckingen'):
        city = " ".join([name_part.capitalize() for name_part in city.split()])
        wp = weather.WeatherPlugin()
        header = f'Hallo, {self.sender_first_name}.'
        body = wp.query_current_weather(city)
        text = f'{header}{body}'
        self._send_message(text)
