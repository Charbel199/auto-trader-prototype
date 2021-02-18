from binance.client import Client
import configure as config

client = Client(config.API_KEY2,config.API_SECRET2)
balances = client.get_account()['balances']
for balance in balances:
    if(float(balance['free']) == 0):
        continue
    print(balance)

print(client.get_asset_balance('USDT'))
bitcoinorders = client.get_all_orders(symbol="INJUSDT")
for order in bitcoinorders:
    print(order)


#client.order_market_buy(symbol='INJUSDT', quantity=1.15)