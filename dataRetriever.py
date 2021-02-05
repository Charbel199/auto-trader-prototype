import configure as config
import csv
from binance.client import Client
import time
import datetime



unixtime= datetime.datetime.utcnow().timestamp()
print(unixtime)
old_unixtime = unixtime - 600

readabletime = datetime.datetime.fromtimestamp(old_unixtime).strftime("%d %b %Y %H:%M ")
print(readabletime)
client = Client(config.API_KEY,config.API_SECRET)
csvfile = open('data/test1m.csv','w',newline='')
candlestick_writer = csv.writer(csvfile)

candlesticks = client.get_historical_klines("LTCUSDT", Client.KLINE_INTERVAL_1MINUTE,readabletime)

for candlestick in candlesticks:
    candlestick_writer.writerow(candlestick)

csvfile.close()