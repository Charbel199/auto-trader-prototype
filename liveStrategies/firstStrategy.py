from datetime import datetime
import math
import json
import configure as config
from binance.client import Client
import time


class testStrategy:
    candlesticks = []
    messages = []
    current_tick = None
    prev_tick = None

    ###Indicators
    ##Vwap indicator
    vwap_indicator = []
    VWAP_INDICATOR_LOOKBACK = 14
    volume_times_typicalprice = []

    ##MACD
    EMA_MULTIPLIER_PERIODS_1 = 12
    EMA_MULTIPLIER_PERIODS_2 = 26
    EMA_MULTIPLIER_PERIODS_3 = 9

    EMA_MULTIPLIER_1 = 2/(1+EMA_MULTIPLIER_PERIODS_1)
    EMA_MULTIPLIER_2 = 2/(1+EMA_MULTIPLIER_PERIODS_2)
    EMA_MULTIPLIER_3 = 2/(1+EMA_MULTIPLIER_PERIODS_3)

    ema_values_1 = []
    ema_values_2 = []
    macd_indicator = []
    ema_values_3 = []

    def __init__(self,timeframe):
        self.timeframe = timeframe


    def log(self, time, txt, dt=None):
        print('{} {}'.format(time, txt))

    ### Process tick by tick and store candlesticks
    def add_message(self,message):
        close = message['k']['c']
        open = message['k']['o']
        high = message['k']['h']
        low = message['k']['l']
        volume = message['k']['v']
        #Just last three digit
        time = datetime.utcfromtimestamp(math.floor(message['E']/1000)).strftime('%Y-%m-%d %H:%M')
        minute = datetime.utcfromtimestamp(math.floor(message['E']/1000)).strftime('%M')
        tick =  {
            "time": time,
            "minute": minute,
            "open": open,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume
        }

        if(not self.current_tick):
            self.current_tick = tick
        else:
            self.prev_tick = self.current_tick
            self.current_tick = tick

        ##If we have at least 2 ticks TODO: Change it to if not then continue
        if(self.current_tick and self.prev_tick):
            ###If one minute has passed then insert candlestick  TODO: Make it automatic
            if(self.prev_tick['minute'] != self.current_tick['minute']):
                self.log(time, self.prev_tick)
                self.log(time, self.current_tick)
                print("THERE IS CHANGE")
                self.candlesticks.append(self.prev_tick)

                ##VWAP processing
                self.volume_times_typicalprice.append(self.process_vwap_typicalprice_times_volume())
                self.process_vwap()

                ##MACD
                self.process_macd()
                self.end()

        ###If we have more than 3 candle sticks then we can start to process
        if(len(self.candlesticks)>3):
            self.process_candlesticks()





    ###VWAP indicator
    def process_vwap(self):

        if(len(self.volume_times_typicalprice)>self.VWAP_INDICATOR_LOOKBACK):
            #print('CAN GET VWAP')
            volumes = [float(candlestick['volume']) for candlestick in self.candlesticks]
            vwap = sum(self.volume_times_typicalprice[-self.VWAP_INDICATOR_LOOKBACK:]) / sum(volumes[-self.VWAP_INDICATOR_LOOKBACK:])
            self.vwap_indicator.append({
                "time": self.candlesticks[-1]['time'],
                "vwap_indicator": vwap
            })
    ### TODO change prev_tick to last candlestick
    def process_vwap_typicalprice_times_volume(self):
        typicalprice = (float(self.prev_tick['close']) + float(self.prev_tick['high']) + float(
            self.prev_tick['low'])) / 3
        return typicalprice*float(self.prev_tick['volume'])



    ###MACD and SIGNAL (Around 100 period to stabilize)

    def process_macd(self):
        closes = [float(candlestick['close']) for candlestick in self.candlesticks]
        self.get_ema(self.EMA_MULTIPLIER_PERIODS_1,self.EMA_MULTIPLIER_1,self.ema_values_1,closes)
        self.get_ema(self.EMA_MULTIPLIER_PERIODS_2, self.EMA_MULTIPLIER_2,self.ema_values_2,closes)
        self.get_macd()
        macd_values = [float(macd['macd_indicator']) for macd in self.macd_indicator]
        self.get_ema(self.EMA_MULTIPLIER_PERIODS_3, self.EMA_MULTIPLIER_3, self.ema_values_3, macd_values)
        print('done process macd')


    def get_ema(self, period, multiplier,ema_list,reference_list):
        if (len(reference_list) > period):
           # print('CAN GET EMA PERIOD: ',period)
            average = sum(reference_list[-period:]) / period
            ##First item in the list
            if (len(ema_list) == 0):
                ema_list.append({
                    "time": self.candlesticks[-1]['time'],
                    "ema_indicator": average
                })
            else:
                recent_value = reference_list[-1]
                spread = recent_value - ema_list[-1]['ema_indicator']
                ema_value = spread * multiplier + ema_list[-1]['ema_indicator']
                ema_list.append({
                    "time": self.candlesticks[-1]['time'],
                    "ema_indicator": ema_value
                })
        print('Done with get ema')

    def get_macd(self):
        ###Considering ema_period_2 is bigger than the first
        if (len(self.ema_values_2) != 0):
            print('CAN GET MACD')
            macd_value = self.ema_values_1[-1]['ema_indicator'] - self.ema_values_2[-1]['ema_indicator']
            self.macd_indicator.append({
                "time": self.candlesticks[-1]['time'],
                "macd_indicator": macd_value
            })
        print('Done with get macd')



    ###Test indicator
    def check_if_last_3_candlesticks_are_in_uptrend(self):
        if (self.candlesticks[-3]['close'] > self.candlesticks[-3]['open'] and self.candlesticks[-2]['close'] >
            self.candlesticks[-2]['open'] and self.candlesticks[-1]['close'] > self.candlesticks[-1]['open']):
            return True
        return False

    def process_candlesticks(self):
        inUptrend = self.check_if_last_3_candlesticks_are_in_uptrend()
        #print('In uptrend? ',inUptrend)




    ###After processing
    def end(self):
        print(self.candlesticks)
        print('Candlestick len: ',len(self.candlesticks),'VWAP len: ',len(self.vwap_indicator))
        print('EMA1 len: ', len(self.ema_values_1), 'EMA2 len: ', len(self.ema_values_2),'EMA3 len: ', len(self.ema_values_3))
        print('MACD len: ', len(self.macd_indicator))
        if (self.vwap_indicator):
            print(self.vwap_indicator)
        if (self.macd_indicator):
            print(self.macd_indicator)
        if (self.ema_values_3):
            print(self.ema_values_3)

        self.print_to_txt("output_of_live_trader.txt")
        print("\n====================")
        print("====================\n")


    def print_to_txt(self,txt):
        with open(txt, "w") as txt_file:
            txt_file.write("CANDLESTICKS\n\n")
            for line in self.candlesticks:
                txt_file.write(json.dumps(line))
                txt_file.write("\n")
            txt_file.write("\n\nVWAP\n\n")
            for line in self.vwap_indicator:
                txt_file.write(json.dumps(line))
                txt_file.write("\n")
            txt_file.write("\n\nMACD\n\n")
            for line in self.macd_indicator:
                txt_file.write(json.dumps(line))
                txt_file.write("\n")
            txt_file.write("\n\nSIGNAL\n\n")
            for line in self.ema_values_3:
                txt_file.write(json.dumps(line))
                txt_file.write("\n")

    def get_previous_data(self, timeperiod=10):
        client = Client(config.API_KEY, config.API_SECRET)
        ##Only if time frame in minute
        unix_minus = timeperiod * int(self.timeframe[0]) * 60
        #curr_time = datetime.utcnow()
        #unix_time = time.mktime(curr_time.timetuple())
        unix_time = int(datetime.utcnow().timestamp())
        old_unix_time = unix_time - unix_minus
        old_readable_time = datetime.fromtimestamp(old_unix_time).strftime("%d %b %Y %H:%M ")
        print('Getting old candlesticks')
        fetched_data = client.get_historical_klines("LTCUSDT", Client.KLINE_INTERVAL_1MINUTE, old_readable_time)
        old_candlesticks = []
        for row in fetched_data:
            old_candlesticks.append({
                "E": float(row[0]),
                "k": {
                    "o": row[1],
                    "h": row[2],
                    "l": row[3],
                    "c": row[4],
                    "v": row[5]
                }
            })
        for old_candlestick in old_candlesticks:
            self.add_message(old_candlestick)
