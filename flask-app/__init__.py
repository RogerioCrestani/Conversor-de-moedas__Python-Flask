import os
from . import api
from flask import Flask, render_template, request, redirect, url_for, flash

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
                
    @app.route('/', methods=('GET', 'POST'))
    def index():
        #coins = None
        #value_coin = None

        value_coin = {
            'coin_1': '',
                'coin_2': '',
                'quantity_coin_1': '',
                'quantity_coin_2':  ''
            }

        coins = {}

        try:
            value_coin = 0
            if request.method == 'POST':
                quantity_coin_1 = request.form['quantity_coin_1']
                coins_comb = request.form['coins']
            else:
                quantity_coin_1 = 1
                coins_comb = 'USD-BRL'

            coin_name = api.request_coin_value(coins_comb)['name']
            coin_1 = coin_name[:coin_name.find('/')]
            coin_2 = coin_name[coin_name.find('/')+1:]

            coin_bid = api.request_coin_value(coins_comb)['bid']
            quantity_coin_2 = round((float(coin_bid) * float(quantity_coin_1)), 2)

            value_coin = {
                'coin_1': coin_1,
                'coin_2': coin_2,
                'quantity_coin_1': quantity_coin_1,
                'quantity_coin_2':  quantity_coin_2
            }

            coins = api.request_coins()
        except Exception as error:
            flash(f'Ocorreu um erro inesperado. Por gentileza recarregue a pagina! Erro: {error} ')

        return render_template('main/index.html', coins=coins, value_coin=value_coin)

    return app