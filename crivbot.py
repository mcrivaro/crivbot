from flask import Flask, request
from actions import Action
import requests
import os
import json

app = Flask(__name__)
telegram_token = os.getenv('TELEGRAM_TOKEN')
bot_name = os.getenv('BOT_NAME')
try:
    port = os.getenv('PORT')
except:
    port = 5000

telegram_uri = f'https://api.telegram.org/bot{telegram_token}/sendMessage'


@app.route('/')
def hello_world():
    return 'This is CrivBot!'


@app.route('/new-message', methods=['POST'])
def new_message():
    message_complete_data = json.loads(request.data)
    print(message_complete_data)
    try:
        action = Action(bot_name, telegram_uri, message_complete_data)
        action.evaluate()
        return 'Action has been executed'
    except:
        return 'Error excecuting action'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
