import requests
# from main import write_json
# import tenv
# from tenv import name
from tenv import coinmarketcap_token as c_token
from tenv import coinmarketcap_url as c_url
import re

headers = { #coinmarketcap
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': c_token,
}

def parse_text(text):
    pattern = r'(?<=/price\s)[a-z-]+'
    p = re.search(pattern, text)
    if p: return p.group(0)

def test():
    url = c_url + 'v1/key/info'
    r = requests.get(url, headers=headers)
    write_json(r.json(), 'answer_test.json')

def coin_map():
    url = c_url + 'v1/cryptocurrency/map'
    params = {
        'start': 1,
        'limit': 4,
        'symbol': 'TUBE'
    }
    r = requests.get(url, params=params, headers=headers)
    write_json(r.json(), 'answer_map.json')

def coin_info(coin):
    url = c_url + 'v1/cryptocurrency/info'
    params = {
        'slug': coin,
    }
    r = requests.get(url, params=params, headers=headers)
    write_json(r.json(), 'answer_info.json')
    print(list(r.json()['data'].keys())[0])

def get_price(coin_slug, coin_err='This coin does not exist!'):
    url = c_url + 'v1/cryptocurrency/quotes/latest'
    params = {
        'slug': coin_slug
    }
    r = requests.get(url, params=params, headers=headers)
    # write_json(r.json(), 'answer_c.json')
    # print(r)
    if 'data' in r.json().keys():
        id = list(r.json()['data'].keys())[0]
        price = r.json()['data'][id]['quote']['USD']['price']
        return price
    else:
        return coin_err

def main():
    # coin_info('ethereum')
    # get_price()
    # test()
    # get_price(parse_text('/price bit-tube text'))
    # coin_map()
    message = 'sfs /price litecoin'
    if '/price' in message.split():
        print(get_price(parse_text(message)))


if __name__ == '__main__':
    main()
