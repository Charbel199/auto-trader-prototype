import configure as config
import csv
from binance.client import Client

client = Client(config.API_KEY,config.API_SECRET)
csvfile = open('data/ltc4h.csv','w',newline='')
candlestick_writer = csv.writer(csvfile)
candlesticks = client.get_historical_klines("LTCUSDT", Client.KLINE_INTERVAL_4HOUR,"1 Jan, 2021","2 Feb, 2021")

for candlestick in candlesticks:
    candlestick[0] = candlestick[0]/1000
    candlestick_writer.writerow(candlestick)

csvfile.close()