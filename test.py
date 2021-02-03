import configure as config
import csv
from binance.client import Client
import backtrader as bt
client = Client(config.API_KEY,config.API_SECRET)

prices = client.get_all_tickers()
print(client.get_account())
csvfile = open('dailyltc.csv','w',newline='')
candlestick_writer = csv.writer(csvfile)
candlesticks = client.get_historical_klines("LTCUSDT", Client.KLINE_INTERVAL_1DAY,"1 Jan, 2020","31 Dec, 2020")

for candlestick in candlesticks:
    candlestick[0] = candlestick[0]/1000
    candlestick_writer.writerow(candlestick)

csvfile.close()