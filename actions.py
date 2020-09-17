import requests
import json
import re
import random


class Action():
    def __init__(self, telegram_uri, chat_id, message):
        self.uri = telegram_uri
        self.chat_id = chat_id
        self.message = str(message).lower()
        self.matching_filters = [
            {'regex': r'buon\s*giorno|guten\s*morgen|ciao', 'function': 'good_morning'},
            {'regex': r'buona\s*notte|gute\s*nacht', 'function': 'good_night'},
            {'regex': r'hallo|ciao|hey', 'function': 'say_hello'}
        ]
        print(f'Received message: {message} in chat {chat_id}')

    def evaluate(self):
        # splitted_message = self.message.split().__dict__
        for filter in self.matching_filters:
            regex = filter['regex']
            function = getattr(self, filter['function'])
            if re.match(regex, self.message):
                function()
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
        text = u'Buongiorno a tutti \U0001F600'  # 1F600 = grinning smiley unicode
        self._send_message(text)
        return 'Good morning message sent.'

    def good_night(self):
        text = u'Buona Notte \U0001F634'
        self._send_message(text)
        return 'Good night message sent.'

    def say_hello(self):
        texts = [u'Hello, may I introduce myself? My name is CrivBot\U0001F600', u'This is CrivBot!\U0001F600', u'Yo, sup \U0001F60E']
        random.seed()
        text = random.choice(texts)
        self._send_message(text)
        return 'Greeting sent.'
