from flask import Flask, render_template, request, session, redirect, app
import time
import json
import socket
import requests
import binance_kernel
import sqlite3
from datetime import datetime
import time

app = Flask(__name__)

app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
)


def check_login():
    if session.get("logged_in"):
        return(True)
    return(False)


@app.route('/logout')
def logout():
    session.clear()
    return("logout")


@app.route('/getpump/<coinname>')
def getpump(coinname):
    x = binance_kernel.getPump(coinname)
    return(x)


@app.route('/cancel_order/<asset>/<orderid>')
def cancel_order(asset, orderid):
    x = binance_kernel.order_cancel(symbol=asset, orderId=orderid)
    print(x)
    return(x)


@app.route('/login', methods=('GET', 'POST'))
def login():
    # return("LOGIN")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin":
            print("USER NAME OK")
            session.clear()
            session['logged_in'] = True
            return redirect('/')

    return render_template('login.html')

# -------------------------------------------------------------------- > INDEX


@app.route('/')
def index():
    if check_login() == False:
        return render_template('login.html')
    # print(session['logged_in'])
    # return(binance_kernel.client.get_exchange_info())

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    # orders = client.get_all_orders(symbol="MDABTC")
    orders = binance_kernel.client.get_open_orders()
    print(orders)
    info = binance_kernel.client.get_account()
    # print(info)
    # print(info['balances'])
    # return("X")
    balances = []
    BTCUSDT = float(binance_kernel.client.get_avg_price(
        symbol='BTCUSDT')['price'])
    SUMBTC = 0.0
    for b in info['balances']:
        try:
            if float(b['free']) != 0:
                print(b)
                if b['asset'] == "BTC":
                    b['BTC'] = 1
                elif b['asset'] == 'USDT':
                    b['BTC'] = '{:0.0{}f}'.format(1/BTCUSDT, 8)
                else:
                    b['BTC'] = binance_kernel.client.get_avg_price(
                        symbol=b['asset']+'BTC')['price']

                totalbtc = float(b['free'])*float(b['BTC'])
                b['totalBTC'] = '{:0.0{}f}'.format(totalbtc, 8)
                SUMBTC += totalbtc
                balances.append(b)
        except:
            print("ERROR")

    SUMBTC = '{:0.0{}f}'.format(SUMBTC, 8)
    print(balances)
    for idx, a in enumerate(orders):
        ts = int(orders[idx]['time'])
        print(ts)
        #orders[idx]['time'] = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    return render_template('index.html', title='miniPumper', my_balances=balances, my_orders=orders, email=binance_kernel.config.EMAIL, BTCUSDT=BTCUSDT, SUMBTC=SUMBTC, local_ip=local_ip)


@app.route('/listwatch')
def listwatch():
    if check_login() == False:
        return render_template('login.html')
    db = sqlite3.connect("mydb.db")
    cur = db.cursor()
    cur.execute("select * from tbl_listwatch")
    row = cur.fetchall()
    db.close()

    return render_template('listwatch.html', row=row)


@app.route('/signal')
def fn_signal():
    # print(binance_kernel.client.get_ticker(symbol="BTCUSDT"))
    print(fn_save_asset_signal())
    return render_template('signal.html')


def fn_save_asset_signal():
    x = binance_kernel.client.get_ticker(symbol="SKLUSDT")
    return(x)


@app.route('/sell/<asset>/<amount>')
def sell(asset, amount):
    return (binance_kernel.sell(asset.upper(), amount))

# ---------------------------------------------------------------------- > BUY


@app.route('/buy/<asset>/<amount>')
def buy(asset, amount):
    return (binance_kernel.buy(asset.upper(), amount))

# -------------------------------------------------------**************************************************** TEST


@app.route('/test')
def test():
    # if check_login()==False :
    #     return render_template('login.html')
    return(binance_kernel.test())
