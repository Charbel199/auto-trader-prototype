from datetime import datetime
from datetime import timedelta
import math
import configure as config
from binance.client import Client
import matplotlib.pyplot as plt
from processing import vwap_processing, macd_processing
from data_logging import log_to_txt
from plotting import plot

class TestStrategy:
    ###Candlesticks and ticks

    candlesticks = []
    current_tick = None
    prev_tick = None

    ###Stop loss variables

    stop_loss_flag = False
    stop_loss_counter = None
    stop_loss_counter_max = None

    ###Indicators

    ##Vwap indicator
    vwap_indicator = {}
    vwap_flag = -1
    # Assuming timeframe in minutes (To get one day)
    VWAP_INDICATOR_LOOKBACK = None
    typical_price_times_volume = []

    ##MACD
    EMA_MULTIPLIER_PERIODS_1 = None
    EMA_MULTIPLIER_PERIODS_2 = None
    EMA_MULTIPLIER_PERIODS_3 = None

    EMA_MULTIPLIER_1 = None
    EMA_MULTIPLIER_2 = None
    EMA_MULTIPLIER_3 = None

    ema_values_1 = {}
    ema_values_2 = {}
    macd_indicator = {}
    ema_values_3 = {}
    macd_flag = -1


    ###Transactions

    ##Buy
    buy_orders = {}
    ##Sell
    sell_orders = {}
    ##Position
    position = {}
    ##Initial Balance
    balance_history = {}
    balance = None



    def __init__(self, timeframe, crypto):
        self.crypto_usdt = crypto + "usdt"
        self.timeframe = timeframe
        self.initialize_variables()
        print("Processing ...")

    def initialize_variables(self):
        # Assuming timeframe in minutes (To get one day) TODO: Make it work for hours too
        if(self.timeframe[1] == 'm'):
            self.VWAP_INDICATOR_LOOKBACK = int(1440 / int(self.timeframe[0]))
        elif(self.timeframe[1] == 'h'):
            self.VWAP_INDICATOR_LOOKBACK = int(24 / int(self.timeframe[0]))

        self.EMA_MULTIPLIER_PERIODS_1 = 12
        self.EMA_MULTIPLIER_PERIODS_2 = 26
        self.EMA_MULTIPLIER_PERIODS_3 = 9
        self.EMA_MULTIPLIER_1 = 2 / (1 + self.EMA_MULTIPLIER_PERIODS_1)
        self.EMA_MULTIPLIER_2 = 2 / (1 + self.EMA_MULTIPLIER_PERIODS_2)
        self.EMA_MULTIPLIER_3 = 2 / (1 + self.EMA_MULTIPLIER_PERIODS_3)



        self.balance = 100
        self.stop_loss_counter = 0
        self.stop_loss_counter_max = 3


    def get_tick_from_message(self, message):
        close = message['k']['c']
        open = message['k']['o']
        high = message['k']['h']
        low = message['k']['l']
        volume = message['k']['v']

        # Just last three digit
        time = datetime.utcfromtimestamp(math.floor(int(message['E']) / 1000))
        open_time = datetime.utcfromtimestamp(math.floor(int(message['k']['t']) / 1000))
        close_time = datetime.utcfromtimestamp(math.floor(int(message['k']['T']) / 1000))
        tick = {
            "time": time,
            "open": float(open),
            "high": float(high),
            "low": float(low),
            "close": float(close),
            "volume": float(volume),
            "open_time": open_time,
            "close_time": close_time
        }
        print(tick)
        return tick

    def check_if_period_passed(self, previous_tick, current_tick):
        return previous_tick["open_time"] != current_tick["open_time"]


    ### Process tick by tick and store candlesticks
    def add_tick(self, message):
        tick = self.get_tick_from_message(message)

        ##Update previous and current tick
        if (not self.current_tick):
            self.current_tick = tick
            return
        else:
            self.prev_tick = self.current_tick
            self.current_tick = tick

        ###If new candlestick, add previous one
        if (self.check_if_period_passed(self.prev_tick, self.current_tick)):
            ###Processing after each new candlestick here:
            self.candlesticks.append(self.prev_tick)
            ##VWAP processing
            self.process_vwap()
            ##MACD
            self.process_macd()

            # self.test_transaction_strategy()
            self.test_macd_strat()
            self.balance_history[self.candlesticks[-1]['open_time']] = self.balance

    ###VWAP indicator
    def process_vwap(self):
        ###Maybe make it also a dictionary ?
        self.typical_price_times_volume.append(vwap_processing.typical_price_times_volume(self.candlesticks[-1]))
        vwap = vwap_processing.process_vwap(self.candlesticks, self.typical_price_times_volume,
                                            self.VWAP_INDICATOR_LOOKBACK)
        if(vwap):
            self.vwap_indicator[self.candlesticks[-1]['open_time']] = vwap


    ###MACD and SIGNAL (Around 100 period to stabilize)
    def process_macd(self):
        closes = [candlestick['close'] for candlestick in self.candlesticks]
        ema_value_1 = macd_processing.get_ema_value(self.EMA_MULTIPLIER_PERIODS_1, self.EMA_MULTIPLIER_1, self.ema_values_1, closes)
        ema_value_2 = macd_processing.get_ema_value(self.EMA_MULTIPLIER_PERIODS_2, self.EMA_MULTIPLIER_2, self.ema_values_2, closes)
        macd_value = macd_processing.get_macd_value(self.ema_values_1,self.ema_values_2)
        macd_values = list(self.macd_indicator.values())
        ema_value_3 = macd_processing.get_ema_value(self.EMA_MULTIPLIER_PERIODS_3, self.EMA_MULTIPLIER_3, self.ema_values_3, macd_values)
        if (ema_value_1):
            self.ema_values_1[self.candlesticks[-1]['open_time']] = ema_value_1
        if (ema_value_2):
            self.ema_values_2[self.candlesticks[-1]['open_time']] = ema_value_2
        if (ema_value_3):
            self.ema_values_3[self.candlesticks[-1]['open_time']] = ema_value_3
        if (macd_value):
            self.macd_indicator[self.candlesticks[-1]['open_time']] = macd_value



    def log_to_txt(self, txt):
        log_to_txt.print_to_txt(
            txt_file= txt,
            candlesticks= self.candlesticks,
            vwap_indicator= self.vwap_indicator,
            macd_indicator= self.macd_indicator,
            ema_values_3= self.ema_values_3,
            buy_orders= self.buy_orders,
            sell_orders= self.sell_orders,
            balance_history= self.balance_history
        )



    ##Getting previous data from Binance API, should ma
    def get_previous_data(self, old_data_time_period=10):
        client = Client(config.API_KEY, config.API_SECRET)
        if(self.timeframe[1] == "m"):
            old_time_multiplier = 60
        elif(self.timeframe[1] == "h"):
            old_time_multiplier = 3600
        unix_minus = old_data_time_period * int(self.timeframe[0]) * old_time_multiplier

        unix_time = int(datetime.utcnow().timestamp())
        old_unix_time = unix_time - unix_minus
        old_readable_time = datetime.fromtimestamp(old_unix_time).strftime("%d %b %Y %H:%M ")

        if(self.timeframe == "1m"):
            old_data_timeframe = Client.KLINE_INTERVAL_1MINUTE
        elif(self.timeframe == "5m"):
            old_data_timeframe = Client.KLINE_INTERVAL_5MINUTE
        elif (self.timeframe == "15m"):
            old_data_timeframe = Client.KLINE_INTERVAL_15MINUTE
        elif (self.timeframe == "1h"):
            old_data_timeframe = Client.KLINE_INTERVAL_1HOUR
        elif (self.timeframe == "2h"):
            old_data_timeframe = Client.KLINE_INTERVAL_2HOUR


        fetched_data = client.get_historical_klines(self.crypto_usdt.upper(), old_data_timeframe,
                                                    old_readable_time)
        old_candlesticks = []
        for row in fetched_data:
            old_candlesticks.append({
                "E": float(row[0]),
                "k": {
                    "o": row[1],
                    "h": row[2],
                    "l": row[3],
                    "c": row[4],
                    "v": row[5],
                    "T": row[6],
                    "t": row[0]
                }
            })
        for old_candlestick in old_candlesticks:
            self.add_tick(old_candlestick)

    ###Transactions
    def test_transaction_strategy(self):
        if (self.vwap_indicator):
            last_vwap_val = self.vwap_indicator[list(self.vwap_indicator)[-1]]
            last_close = self.candlesticks[-1]['close']
            # print("close vs vwap: ",last_close," ",last_vwap_val)
            if (last_vwap_val > last_close):
                if (self.vwap_flag == 1):
                    self.buy(list(self.vwap_indicator)[-1], 30, last_close)
                    self.vwap_flag = 0
                else:
                    self.vwap_flag = 0
            elif (last_vwap_val < last_close):
                if (self.vwap_flag == 0):
                    self.sell_all(list(self.vwap_indicator)[-1], last_close)
                    self.vwap_flag = 1
                else:
                    self.vwap_flag = 1
        else:
            print("No vwap")

    def test_macd_strat(self):
        if (self.ema_values_3):
            current_time = self.candlesticks[-1]['open_time']
            current_macd = self.macd_indicator[list(self.macd_indicator)[-1]]
            current_signal = self.ema_values_3[list(self.ema_values_3)[-1]]
            last_close = self.candlesticks[-1]['close']

            if (self.stop_loss_counter >= 3):
                if (self.candlesticks[-3]['close'] > self.candlesticks[-3]['open'] and self.candlesticks[-2]['close'] >
                    self.candlesticks[-2]['open'] and self.candlesticks[-1]['close'] > self.candlesticks[-1]['open']):
                    self.stop_loss_counter = 0
                return

            if (self.position):
                quantity = self.position[list(self.position)[-1]]
                current_quantity_price = quantity * last_close
                if (current_quantity_price < (50 * 0.98)):
                    self.sell_all(current_time, last_close)
                    self.stop_loss_flag = True
                    self.stop_loss_counter += 1

            if (current_macd > current_signal):
                if (self.macd_flag == 0 and current_macd < 0 and not self.stop_loss_flag):
                    self.buy(current_time, 50, last_close)
                self.macd_flag = 1


            elif (current_macd < current_signal):
                if (self.macd_flag == 1 and current_macd > 0):
                    self.sell_all(current_time, last_close)
                    # Reset counter
                    self.stop_loss_counter = 0
                self.macd_flag = 0
            if (current_macd > 0):
                self.stop_loss_flag = False





    ##Buy order
    def buy(self, time, amount, price):
        if (not self.position):
            self.buy_orders[time] = amount
            self.balance = self.balance - amount
            self.position[time] = amount / price

    ##Sell order
    def sell_all(self, time, price):
        if (self.position):
            # Sell the amount in the position
            self.sell_orders[time] = price * self.position[list(self.position)[-1]]
            self.balance = self.balance + price * self.position[list(self.position)[-1]]
            # Empty position after selling
            self.position.clear()

    def sell(self, time, amount, price):
        pass

    def plot(self):
        plot.plot_candlesticks(self.candlesticks,self.macd_indicator,self.ema_values_3)

