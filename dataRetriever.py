import configure as config
import csv
from binance.client import Client



def retrieve_data(crypto, timeframe, start_date, end_date = None):

    client = Client(config.API_KEY,config.API_SECRET)
    file  = "../data/"+crypto+timeframe+".csv"
    csv_file = open(file,'w',newline='')
    candlestick_writer = csv.writer(csv_file)



    if (timeframe == "1m"):
        binance_timeframe = Client.KLINE_INTERVAL_1MINUTE
    elif (timeframe == "5m"):
        binance_timeframe = Client.KLINE_INTERVAL_5MINUTE
    elif (timeframe == "15m"):
        binance_timeframe = Client.KLINE_INTERVAL_15MINUTE
    elif (timeframe == "1h"):
        binance_timeframe = Client.KLINE_INTERVAL_1HOUR
    elif (timeframe == "2h"):
        binance_timeframe = Client.KLINE_INTERVAL_2HOUR


    binance_crypto = crypto.upper()+"USDT"

    if(end_date):
        candlesticks = client.get_historical_klines(binance_crypto, binance_timeframe, start_date, end_date)
    else:
        candlesticks = client.get_historical_klines(binance_crypto, binance_timeframe, start_date)

    for candlestick in candlesticks:
        candlestick_writer.writerow(candlestick)

    csv_file.close()

if(__name__ == "__main__"):
    date = "21 Feb, 2021"
    date2 = "25 Dec, 2020"
    retrieve_data('eth','1m',date)