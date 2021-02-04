from datetime import datetime
import math

import random
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class testStrategy:
    candlesticks = []
    messages = []
    current_tick = None
    prev_tick = None
    def __init__(self,timeframe):
        self.timeframe = timeframe
        self.chart_process()

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
        time = datetime.utcfromtimestamp(math.floor(message['E']/1000)).strftime('%Y-%m-%d %H:%M:%S')
        minute = datetime.utcfromtimestamp(math.floor(message['E']/1000)).strftime('%M')
        tick =  {
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

        if(self.current_tick and self.prev_tick):
            self.log(time, self.prev_tick)
            self.log(time, self.current_tick)
            ###If one minute has passed then insert candlestick
            if(self.prev_tick['minute'] != self.current_tick['minute']):
                self.candlesticks.append(self.prev_tick)

        ###If we have more than 3 candle sticks then we can start to process
        if(len(self.candlesticks)>3):
            self.process_candlesticks()

    def process_candlesticks(self):
        inUptrend = self.check_if_last_3_candlesticks_are_in_uptrend()
        print('In uptrend? ',inUptrend)


    def check_if_last_3_candlesticks_are_in_uptrend(self):
        if (self.candlesticks[-3]['close'] > self.candlesticks[-3]['open'] and self.candlesticks[-2]['close'] >
            self.candlesticks[-2]['open'] and self.candlesticks[-1]['close'] > self.candlesticks[-1]['open']):
            return True
        return False
    def end(self):
        print(len(self.candlesticks))
        if (self.candlesticks):
            closePrices = [float(candlestick['close']) for candlestick in self.candlesticks]
            print('Close prices: ',closePrices)



