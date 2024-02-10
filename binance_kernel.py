import config
import json
from binance.client import Client
from binance.enums import *
from datetime import timedelta, datetime

client = Client(config.API_KEY, config.API_SECRET)


def hello():
    return("my name is vahid")


# ---------------------------------------------------------------------------- > SELL
def sell(asset, amount):
    # if check_login()==False :
    #     return render_template('login.html')
    asset = asset.upper()
    price = float(client.get_order_book(symbol=asset)['bids'][0][0])

    # price=float(avg_price['price'])
    # price_add=0.00000002
    # price=price+price_add

    # BIT=0.00053
    price_str = '{:0.0{}f}'.format(price, 8)

    # return("SELL")
    # return('ENDSELL '+asset + " - " + price_str +"-"+qt )
    order_sell = client.create_order(
        symbol=asset,
        side=SIDE_SELL,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=amount,
        price=price_str)
    # order_sell = client.order_market_sell(symbol=asset, quantity=amount)# ====================== > MARKET
    print(order_sell)
    out_str = "SELL - > " + str(asset) + " AMOUNT:" + \
        str(amount) + " PRICESTR:" + price_str + \
        " ORDERSELL:" + json.dumps(order_sell)
    print(out_str)
    return(out_str)


# -------------------------------------------------------------------------- > BUY 2 API

def order_cancel(symbol, orderId):
    result = client.cancel_order(symbol=symbol, orderId=orderId)
    return(result)


def getPump(coin):
    # return '{"name":"Bob"}'
    # TODO Need change ---------------------------
    # 1- get price in this hour
    # 2- get percent of changed price just now
    # 3- if percent grows is mine of 100 BUY
    # 4- sel unitl percent is 100%
    # ------------------------------------------
    # startTime=1618160400000, endTime=1618160402000    #------> for 21:30:00

    myasset = coin.upper()+"BTC"

    a = client.get_aggregate_trades(
        symbol=myasset, startTime=1618160400000, endTime=1618160402000)  # 21:30:
    first_pric = float(a[0]['p'])  # price ra dar saniye 0 migirad

    mybit = 0.00995223  # 0.01174143
    darsad_kharid = mybit*90/100  # percent of my BTC

    # asset=request.args.get('asset').upper()+request.args.get("asset2").upper()
    # mybit=request.args.get('mybit',default=0,type=float)
    # mybit = float(mybit)
    # price = client.get_avg_price(symbol=asset)
    price_BUY = float(client.get_order_book(symbol=myasset)['asks'][1][0])

    darsad_roshd = (price_BUY-first_pric)/first_pric * \
        100  # mizan darsad rosh ra neshan midahad

    if darsad_roshd <= 100:  # yani hanooz 100%rosh nakarde ast

        amount = int(darsad_kharid/price_BUY)
        price_BUY_str = '{:0.0{}f}'.format(price_BUY, 8)

        order_BUY = client.order_market_buy(symbol=myasset, quantity=amount)

        BTC_balance = float(client.get_asset_balance(asset="BTC")['free'])
        COIN_balance = float(client.get_asset_balance(asset=coin)['free'])

        price_avarage = (mybit-BTC_balance)/COIN_balance

        # percent for TAKE PROFIT of SELL ORDER
        # price_SELL = price_avarage + (price_avarage*50/100)
        price_SELL = price_avarage + (price_avarage*(100-darsad_roshd)/100)

        print(price_SELL)

        price_SELL_str = '{:0.0{}f}'.format(price_SELL, 8)
        price_avarage_str = '{:0.0{}f}'.format(price_avarage, 8)

        order_SELL = client.create_order(
            symbol=myasset,
            side=SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=COIN_balance,
            price=price_SELL_str)

        print(order_BUY)

    out_str = " ASSET:" + myasset + " PRICEBUY:" + price_BUY_str + " AMOUNT:" + str(amount) +\
        " BTCFORBUY:"+str(darsad_kharid) + "\n" +\
        " ORDERBUY:"+json.dumps(order_BUY) + "\n" +\
        " BTCBALANCE:"+str(BTC_balance) + " darsadRosh:" + str(darsad_kharid) + " COINBALANCE:" + str(COIN_balance) + " PRICESELL:" + price_SELL_str + " PRICEAVARAGE:" + price_avarage_str + "\n" +\
        " ORDERSELL:" + json.dumps(order_SELL)

    f = open("out.txt", "a")
    f.write(out_str)
    f.close()

    # ==================================================================== END
    return(out_str)

# ---------------------------------------------------------------------------- > buy


def buy(asset, amount):
    # if check_login()==False :
    #     return render_template('login.html')
    asset = asset.upper()
    price = float(client.get_order_book(symbol=asset)['ask'][0][0])

    # price=float(avg_price['price'])
    # price_add=0.00000002
    # price=price+price_add

    # BIT=0.00053
    price_str = '{:0.0{}f}'.format(price, 8)

    # return("SELL")
    # return('ENDSELL '+asset + " - " + price_str +"-"+qt )
    order_buy = client.create_order(
        symbol=asset,
        side=SIDE_SELL,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=amount,
        price=price_str)
    # order_sell = client.order_market_sell(symbol=asset, quantity=amount)# ====================== > MARKET
    print(order_buy)
    out_str = "SELL - > " + str(asset) + " AMOUNT:" + \
        str(amount) + " PRICESTR:" + price_str + \
        " ORDERSELL:" + json.dumps(order_buy)
    print(out_str)
    return(out_str)

# ------------------------------------------------------------------------- TEST


def test():
    #details = client.get_products()
    # x = []
    # TI = client.get_ticker()  # market cap c*cs
    # for i in TI:
    #     sym = i['symbol']
    #     vol = i['volume']
    #     # print(sym)
    #     x.append({'symbol': sym, 'volume': vol})

    # # print("X")
    # # print(x)
    # # print(TI)
    # return(str(x))

    details = client.get_products()  # market cap c*cs
    txt="<table border='1'>"
    txt+="<tr><th>asset</th><th>volume</th><th>cs</th><th>c</th><th>M-CAP</th><th>Moment</th></tr>"
    for ar in details['data']:
        c = ar['c']
        cs = ar['cs']
        if cs is None:
            cs = 0
        if c is None:
            c = 0
        mcap=c*cs
        moment=mcap/float(ar['qv'])
        # print(ar['an'], c*cs)
        if moment>0 :#"{:,}".format(1000000)
            myclass=""
            if moment<5:
                myclass=" style='background-color:yellow' "
            txt+="<tr "+myclass+">"
            txt+="<td>"+str(ar['s'])+"</td>"+"<td>"+"{:,}".format(round(ar['qv']))+" </td>"+"<td>"+"{:,}".format(cs)+"</td>"+"<td>"+"{:,}".format(c)+"</td>"+"<td>"+"{:,}".format(round(mcap))+"</td>"+"<td><strong>"+"{:,}".format(round(moment,1))+"</strong></td>"
            txt+="</tr>"
        # print(ar['s'],ar['qv'],ar['cs'],ar['c'])

    txt+="</table>"

    #details = client.get_ticker()
    # print(details)
    return(txt)
    #BTC_balance = client.get_asset_balance(asset="BTC")['free']
    # print(BTC_balance)
    # return(BTC_balance)
    # TG_Client.start()
    # TG_Client.run_until_disconnected()
    # print(client.get_account()['balances']['asset']=="BTC")
    # return(client.get_symbol_info("AXSBTC"))
    # print(client.get_orderbook_tickers())
    # data=client.get_aggregate_trades(symbol="MDABTC",fromId="1")
    # data=client.get_aggregate_trades(symbol="MDABTC",startTime=1612978200,endTime=1612978500,fromId="1")
    # print(client.get_server_time())
    # 20210307-20:30:00 - > 20:32:00
    #
    # startTime=1618160400000, endTime=1618160402000    #------> for 21:30:00
    #
    a = client.get_aggregate_trades(
        symbol='ADABTC', startTime=1618153200000, endTime=1618153203000)  # 19:30:
    # b = json.dumps(a[0])
    print(a[0]['p'])
    # a = client.get_aggregate_trades(symbol='STEEMBTC',startTime =1610989200000,endTime= 1610989320000)#20210118-20:31:24 - > 20:33:00
    # a = client.get_aggregate_trades(symbol='SNMBTC',startTime =1611162000000,endTime= 1611162180000)#20210120-20:31:24 - > 20:33:00
    # a = client.get_aggregate_trades(symbol='SKYBTC',startTime =1613235600000,endTime= 1613235660000)#20210213-20:30:05 - > 00:31:00
    # a = client.get_aggregate_trades(symbol='MDABTC',startTime =1612990800000,endTime= 1612990860000)#20210211-00:30:14 - > 00:31:00
    # a = client.get_aggregate_trades(symbol='NXSBTC',startTime =1613926800000,endTime= 1613926860000)#20210221-20:30:04 - > 20:31:00
    # 20210221-20:30:04 - > 20:31:00
    a = client.get_aggregate_trades(
        symbol='ADABTC', startTime=1619353800000, endTime=1619354400000)
    # a=client.get_recent_trades(symbol="NEBLBTC",limit=500)
    # b=client.get_historical_trades(symbol="NEBLBTC",limit=500)1613914204000
    # print(client.get_symbol_info("ADABTC"))
    print(a)
    fa = open("exportTrader/ADDDDDDD.csv", "a")
    head = "a,p,q,f,l,T,m,M\n"
    fa.write(str(head))
    for trade in a:
        line = str(trade['a'])+","+str(trade['p'])+","+str(trade['q'])+","+str(trade['f'])+","+str(
            trade['l'])+","+str(datetime.fromtimestamp(trade['T']//1000))+","+str(trade['m'])+","+str(trade['M'])
        fa.write(str(line)+"\n")
    fa.close

    return("endtest")
    # bid=book['agg_trade_list']
    # print(trades)
    # return render_template('login.html')

    return("info")
    print("---------------------------------------------------------------------")
    #info = client.get_account_status()
    #info = client.get_asset_balance(asset='USDT')
    a = [{'asset': 'BTC', 'free': '0.00025455', 'locked': '0.00000000'},
         {'asset': 'ETH', 'free': '0.00000000', 'locked': '0.00000000'}]
    print(a)
    x = []
    for i in a:
        i["color"] = "XXXXXXXXXXXXXX"
        x.append(i)
        # print(i)

    print(x)
    return("info")
    return(info)
