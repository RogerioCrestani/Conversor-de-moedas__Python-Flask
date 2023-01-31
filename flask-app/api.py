import requests, json

def request_coins():
    coins = requests.get('https://economia.awesomeapi.com.br/available').json()

    return coins

def request_coin_value(coins):
    coins = requests.get(f'http://economia.awesomeapi.com.br/json/last/{coins}').json()
    values = [*coins.values()]
    return values[0]