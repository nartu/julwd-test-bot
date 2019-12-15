import os
import sys
import requests
import tenv
from time import sleep

def get_updates_json(request):
    params = {'timeout': 100, 'offset': None}
    response = requests.get(request + 'getUpdates', data=params)
    return response.json()

def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id

def send_mess(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(tenv.url + 'sendMessage', data=params)
    return response

#print(tenv.url)
#chat_id = get_chat_id(last_update(get_updates_json(tenv.url)))
#send_mess(chat_id, 'Your message goes here')

def main():
    update_id = last_update(get_updates_json(tenv.url))['update_id']
    while True:
        if update_id == last_update(get_updates_json(tenv.url))['update_id']:
           message = 'Update ' + str(update_id)
           send_mess(get_chat_id(last_update(get_updates_json(tenv.url))), message)
           update_id += 1
        sleep(3)

if __name__ == '__main__':
    main()
