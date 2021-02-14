import configure as config
import csv
from binance.client import Client





client = Client(config.API_KEY,config.API_SECRET)
csvfile = open('data/ltc5m.csv','w',newline='')
candlestick_writer = csv.writer(csvfile)
date = "12 Feb, 2021"
date2 = "25 Dec, 2020"


candlesticks = client.get_historical_klines("LTCUSDT", Client.KLINE_INTERVAL_5MINUTE,date)
#candlesticks = client.get_historical_klines("XRPUSDT", Client.KLINE_INTERVAL_1MINUTE,date,date2)

for candlestick in candlesticks:
    candlestick_writer.writerow(candlestick)

csvfile.close()