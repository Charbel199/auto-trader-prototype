from datetime import datetime
import math


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

        ##If we have at least 2 ticks TODO: Change it to if not then continue
        if(self.current_tick and self.prev_tick):
            self.log(time, self.prev_tick)
            self.log(time, self.current_tick)

            ###If one minute has passed then insert candlestick  TODO: Make it automatic
            if(self.prev_tick['minute'] != self.current_tick['minute']):
                print("THERE IS CHANGE")
                self.candlesticks.append(self.prev_tick)

                ##VWAP processing
                self.volume_times_typicalprice.append(self.process_vwap_typicalprice_times_volume())
                self.process_vwap()

                ##MACD
                self.process_macd()


        ###If we have more than 3 candle sticks then we can start to process
        if(len(self.candlesticks)>3):
            self.process_candlesticks()





    ###VWAP indicator
    def process_vwap(self):
        print('Calculating VWAP')
        if(len(self.volume_times_typicalprice)>self.VWAP_INDICATOR_LOOKBACK):
            volumes = [float(candlestick['volume']) for candlestick in self.candlesticks]
            vwap = sum(self.volume_times_typicalprice[-self.VWAP_INDICATOR_LOOKBACK:]) / sum(volumes[-self.VWAP_INDICATOR_LOOKBACK:])
            self.vwap_indicator.append({
                "minute": self.candlesticks[-1]['minute'],
                "vwap_indicator": vwap
            })
    def process_vwap_typicalprice_times_volume(self):
        typicalprice = (float(self.prev_tick['close']) + float(self.prev_tick['high']) + float(
            self.prev_tick['low'])) / 3
        return typicalprice*float(self.prev_tick['volume'])



    ###MACD

    def process_macd(self):
        closes = [float(candlestick['close']) for candlestick in self.candlesticks]
        self.get_ema(self.EMA_MULTIPLIER_PERIODS_1,self.EMA_MULTIPLIER_1,self.ema_values_1,closes)
        self.get_ema(self.EMA_MULTIPLIER_PERIODS_2, self.EMA_MULTIPLIER_2,self.ema_values_2,closes)
        self.get_macd()
        self.get_ema(self.EMA_MULTIPLIER_PERIODS_3, self.EMA_MULTIPLIER_3, self.macd_indicator)



    def get_ema(self, period, multiplier,ema_list,reference_list):
        if (len(reference_list) > period):
            average = sum(reference_list[-period:]) / period
            ##First item in the list
            if (len(ema_list) == 0):
                ema_list.append({
                    "minute": self.candlesticks[-1]['minute'],
                    "ema_indicator": average
                })
            else:
                recent_value = reference_list[-1]
                spread = recent_value - ema_list[-1]
                ema_value = spread * multiplier + ema_list[-1]
                ema_list.append({
                    "minute": self.candlesticks[-1]['minute'],
                    "ema_indicator": ema_value
                })

    def get_macd(self):
        ###Considering ema_period_2 is bigger than the first
        if (len(self.ema_values_2) != 0):
            macd_value = self.ema_values_1[-1]['ema_indicator'] - self.ema_values_2[-1]['ema_indicator']
            self.macd_indicator.append({
                "minute": self.candlesticks[-1]['minute'],
                "vwap_indicator": macd_value
            })




    ###Test indicator
    def check_if_last_3_candlesticks_are_in_uptrend(self):
        if (self.candlesticks[-3]['close'] > self.candlesticks[-3]['open'] and self.candlesticks[-2]['close'] >
            self.candlesticks[-2]['open'] and self.candlesticks[-1]['close'] > self.candlesticks[-1]['open']):
            return True
        return False

    def process_candlesticks(self):
        inUptrend = self.check_if_last_3_candlesticks_are_in_uptrend()
        print('In uptrend? ',inUptrend)




    ###After processing
    def end(self):
        print(len(self.candlesticks))
        if (self.vwap_indicator):
            print(self.vwap_indicator)
        if (self.macd_indicator):
            print(self.macd_indicator)
        if (self.ema_values_3):
            print(self.ema_values_3)




