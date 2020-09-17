import requests
from flask import Flask, request
import os
import json

app = Flask(__name__)
telegram_token = os.getenv('TELEGRAM_TOKEN')
try:
    port = os.getenv('PORT')
except:
    port = 5000

telegram_uri = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
headers = {'content-type': 'application/json'}


@app.route('/')
def hello_world():
    return 'This is CrivBot!'


@app.route('/new-message', methods=['POST'])
def new_message():
    message = json.loads(request.data)['message']
    body = {
        'chat_id': message['chat']['id'],
        'text': 'Hi From CrivBot!'
    }
    try:
        test = json.dumps(body)
        res = requests.post(url=telegram_uri,
                            data=json.dumps(body), headers=headers)
        print(telegram_uri)
        print(res.text, res.status_code)
        print(f'message sent. status {res}')
    except:
        raise
        print('error while sending message')
    return message


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
