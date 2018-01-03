import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine

############for grab#############
import requests
from bs4 import BeautifulSoup
from fsm import grab_all_title

API_TOKEN = '484840033:AAE3y63PM1OQJITBL1aV3HFQpeVWvVCxqg4'
WEBHOOK_URL ='https://4b5e1c4d.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'user',
        'intro',
        'username',
        'ability',
        'all',
        'one',
        'photo',
        'money',
        'teacher'
    ],
    transitions=[
        {
            'trigger': 'advance', ##the name of jump
            'source': 'user',
            'dest': 'intro',
            'conditions': 'is_going_to_intro'
        },
        {
            'trigger': 'advance',
            'source': 'intro',
            'dest': 'username',
            'conditions': 'is_going_to_username'
        },
        {
            'trigger': 'advance',
            'source': 'username',
            'dest': 'ability',
            'conditions': 'is_going_to_ability'
        },
        {
            'trigger': 'advance',
            'source': 'username',
            'dest': 'money',
            'conditions': 'is_going_to_money'
        },
        {
            'trigger': 'advance',
            'source': 'username',
            'dest': 'teacher',
            'conditions': 'is_going_to_teacher'
        },
        #功能區塊的state
        {
            'trigger': 'advance',
            'source': 'ability',
            'dest': 'all',
            'conditions': 'is_going_to_all'
        },
        {
            'trigger': 'advance',
            'source': 'ability',
            'dest': 'one',
            'conditions': 'is_going_to_one'
        },
        {
            'trigger': 'advance',
            'source': 'ability',
            'dest': 'photo',
            'conditions': 'is_going_to_photo'
        },
        
        #從all one photo跳回去, ability
        {
            'trigger': 'go_back',
            'source': [
                'all',
                'one',
                'photo',
                'money',
                'teacher'
            ],
            'dest': 'username'
        },
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')

@app.route('/hello')
def hello():
	print(request)
	return '!!!!!!!'


if __name__ == "__main__":
    _set_webhook()
    app.run()
