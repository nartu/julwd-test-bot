from flask import Flask
#from flask_sslify import SSLify
from flask import request
from flask import jsonify
from tenv import url as URL
from tenv import bot_path, webhook_url
import requests
import json
from parse_coin import get_price, parse_text


app = Flask(__name__)
sslify = SSLify(app)

def write_json(date, filename='answer.json'):
    with open(filename, 'w') as f:
        #writ in file
        json.dump(date, f, indent=2, ensure_ascii=False)

def get_updates():
    url = URL + 'getUpdates'
    r = requests.get(url)
    write_json(r.json(), 'answer.json')
    return r.json()

def send_message(chat_id, text='__HI__'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()

def main():
    # r = requests.get(URL + 'getMe')
    # write_json(r.json())
    r = get_updates()
    chat_id = r['result'][-1]['message']['chat']['id']
    # print(chat_id)
    send_message(chat_id)

def webhook(act = 'info'):
    params = {'url': webhook_url}
    if act == 'set':
        url = URL + 'setWebhook'
        r = requests.get(url, data=params)
    elif act == 'delete':
        url = URL + 'deleteWebhook'
        r = requests.get(url)
    else:
        url = URL + 'getWebhookInfo'
        r = requests.get(url, data=params)
    return r.json()

### View ###
@app.route(bot_path, methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json() # response
        write_json(r, 'answer2.json')
        chat_id = r['message']['chat']['id']
        message = r['message']['text']
        if '/price' in message.split():
            answer_of_bot = get_price(parse_text(message))
            send_message(chat_id, answer_of_bot)
        return jsonify(r)
    return '<h1>Bot</h1>'

@app.route(bot_path+'/wh', methods=['GET'])
def wh():
    return webhook(request.args['act'])

if (__name__ == '__main__'):
    # main()
    app.run()
