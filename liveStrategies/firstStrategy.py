from datetime import datetime
import math
import configure as config
from binance.client import Client
import matplotlib.pyplot as plt


class testStrategy:
    candlesticks = []
    current_tick = None
    prev_tick = None

    stop_loss_flag = False
    stop_loss_counter = 0
    ###Indicators
    ##Vwap indicator
    vwap_indicator = {}
    vwap_flag = -1
    # Assuming timeframe in minutes (To get one day)
    VWAP_INDICATOR_LOOKBACK = 1440
    volume_times_typicalprice = []

    ##MACD
    EMA_MULTIPLIER_PERIODS_1 = 12
    EMA_MULTIPLIER_PERIODS_2 = 26
    EMA_MULTIPLIER_PERIODS_3 = 9

    EMA_MULTIPLIER_1 = 2 / (1 + EMA_MULTIPLIER_PERIODS_1)
    EMA_MULTIPLIER_2 = 2 / (1 + EMA_MULTIPLIER_PERIODS_2)
    EMA_MULTIPLIER_3 = 2 / (1 + EMA_MULTIPLIER_PERIODS_3)

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
    balance = 100

    def __init__(self, timeframe, crypto):
        self.crypto_usdt = crypto + "usdt"
        self.timeframe = timeframe
        # Assuming timeframe in minutes (To get one day)
        # self.VWAP_INDICATOR_LOOKBACK = int(1440/int(self.timeframe[0]))
        print("Processing ...")

    def log(self, time, txt, dt=None):
        print('{} {}'.format(time, txt))

    ### Process tick by tick and store candlesticks
    def add_message(self, message):
        close = message['k']['c']
        open = message['k']['o']
        high = message['k']['h']
        low = message['k']['l']
        volume = message['k']['v']
        # Just last three digit
        time = datetime.utcfromtimestamp(math.floor(message['E'] / 1000)).strftime('%Y-%m-%d %H:%M')
        minute = datetime.utcfromtimestamp(math.floor(message['E'] / 1000)).strftime('%M')
        tick = {
            "time": time,
            "minute": minute,
            "open": float(open),
            "high": float(high),
            "low": float(low),
            "close": float(close),
            "volume": float(volume)
        }
        print(self.stop_loss_counter)
        if (not self.current_tick):
            self.current_tick = tick
        else:
            self.prev_tick = self.current_tick
            self.current_tick = tick

        ##If we have at least 2 ticks TODO: Change it to if not then continue
        if (self.current_tick and self.prev_tick):
            ###If one minute has passed then insert candlestick  TODO: Make it automatic
            if (self.prev_tick['minute'] != self.current_tick['minute']):
                # print(self.balance)
                # self.log(time, self.prev_tick)
                # self.log(time, self.current_tick)
                # print("THERE IS CHANGE")
                self.candlesticks.append(self.prev_tick)

                ##VWAP processing
                self.volume_times_typicalprice.append(self.process_vwap_typicalprice_times_volume())
                self.process_vwap()

                ##MACD
                self.process_macd()
                # self.end()

                # self.test_transaction_strategy()
                self.test_macd_strat()
                self.balance_history[self.candlesticks[-1]['time']] = self.balance

    ###VWAP indicator
    def process_vwap(self):

        if (len(self.volume_times_typicalprice) >= self.VWAP_INDICATOR_LOOKBACK):
            # print('CAN GET VWAP')
            volumes = [candlestick['volume'] for candlestick in self.candlesticks]
            vwap = sum(self.volume_times_typicalprice[-self.VWAP_INDICATOR_LOOKBACK:]) / sum(
                volumes[-self.VWAP_INDICATOR_LOOKBACK:])
            self.vwap_indicator[self.candlesticks[-1]['time']] = vwap
            # self.vwap_indicator.append({
            #     "time": self.candlesticks[-1]['time'],
            #     "vwap_indicator":
            # })

    ### TODO change prev_tick to last candlestick
    def process_vwap_typicalprice_times_volume(self):
        typicalprice = (self.prev_tick['close'] + self.prev_tick['high'] +
                        self.prev_tick['low']) / 3
        return typicalprice * self.prev_tick['volume']

    ###MACD and SIGNAL (Around 100 period to stabilize)

    def process_macd(self):
        closes = [candlestick['close'] for candlestick in self.candlesticks]
        self.get_ema(self.EMA_MULTIPLIER_PERIODS_1, self.EMA_MULTIPLIER_1, self.ema_values_1, closes)
        self.get_ema(self.EMA_MULTIPLIER_PERIODS_2, self.EMA_MULTIPLIER_2, self.ema_values_2, closes)
        self.get_macd()
        # macd_values = [float(macd['macd_indicator']) for macd in self.macd_indicator]
        macd_values = list(self.macd_indicator.values())
        self.get_ema(self.EMA_MULTIPLIER_PERIODS_3, self.EMA_MULTIPLIER_3, self.ema_values_3, macd_values)
        # print('done process macd')

    def get_ema(self, period, multiplier, ema_list, reference_list):
        if (len(reference_list) >= period):
            # print('CAN GET EMA PERIOD: ',period)
            average = sum(reference_list[-period:]) / period
            ##First item in the list
            if (len(ema_list) == 0):
                ema_list[self.candlesticks[-1]['time']] = average
                # ema_list.append({
                #    "time": self.candlesticks[-1]['time'],
                #    "ema_indicator": average
                # })
            else:
                recent_value = reference_list[-1]
                spread = recent_value - ema_list[list(ema_list)[-1]]
                ema_value = spread * multiplier + ema_list[list(ema_list)[-1]]
                ema_list[self.candlesticks[-1]['time']] = ema_value
                # print('Done with get ema')

    def get_macd(self):
        ###Considering ema_period_2 is bigger than the first
        if (len(self.ema_values_2) != 0):
            # print('CAN GET MACD')
            macd_value = self.ema_values_1[list(self.ema_values_1)[-1]] - self.ema_values_2[list(self.ema_values_2)[-1]]
            self.macd_indicator[self.candlesticks[-1]['time']] = macd_value
            # self.macd_indicator.append({
            #    "time": self.candlesticks[-1]['time'],
            #    "macd_indicator": macd_value
            # })
            # print('Done with get macd')

    ###After processing, after getting one new candlestick
    def end(self):
        print(self.candlesticks)
        print('Candlestick len: ', len(self.candlesticks), 'VWAP len: ', len(self.vwap_indicator))
        print('EMA1 len: ', len(self.ema_values_1), 'EMA2 len: ', len(self.ema_values_2), 'EMA3 len: ',
              len(self.ema_values_3))
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

    def print_to_txt(self, txt):
        with open(txt, "w") as txt_file:
            for line in self.candlesticks:
                txt_file.write(line["time"])
                txt_file.write("\t")
                txt_file.write("Close: ")
                txt_file.write("{:.2f}".format(line["close"]))
                txt_file.write("\t")
                txt_file.write("Open: ")
                txt_file.write("{:.2f}".format(line["open"]))
                txt_file.write("\t")
                txt_file.write("Low: ")
                txt_file.write("{:.2f}".format(line["low"]))
                txt_file.write("\t")
                txt_file.write("High: ")
                txt_file.write("{:.2f}".format(line["high"]))
                txt_file.write("\t")
                if (self.vwap_indicator.get(line['time'])):
                    txt_file.write("{:.2f}".format(self.vwap_indicator.get(line['time'])))
                else:
                    txt_file.write("No data")
                txt_file.write("\t")
                if (self.macd_indicator.get(line['time'])):
                    txt_file.write("{:.2f}".format(self.macd_indicator.get(line['time'])))
                else:
                    txt_file.write("No data")
                txt_file.write("\t")
                if (self.ema_values_3.get(line['time'])):
                    txt_file.write("{:.2f}".format(self.ema_values_3.get(line['time'])))
                else:
                    txt_file.write("No data")
                txt_file.write("\t")
                txt_file.write("\t")
                txt_file.write("\t")
                if (self.buy_orders.get(line['time'])):
                    txt_file.write("{:.2f}".format(self.buy_orders.get(line['time'])))
                else:
                    txt_file.write("No Buy")
                txt_file.write("\t")
                txt_file.write("\t")
                if (self.sell_orders.get(line['time'])):
                    txt_file.write("{:.2f}".format(self.sell_orders.get(line['time'])))
                else:
                    txt_file.write("No Sell")
                txt_file.write("\t")
                txt_file.write("\t")
                if (self.balance_history.get(line['time'])):
                    txt_file.write("{:.2f}".format(self.balance_history.get(line['time'])))
                txt_file.write("\n")

    ##Getting previous data from Binance API
    def get_previous_data(self, timeperiod=10):
        client = Client(config.API_KEY, config.API_SECRET)
        ##Only if time frame in minute
        unix_minus = timeperiod * int(self.timeframe[0]) * 60
        # curr_time = datetime.utcnow()
        # unix_time = time.mktime(curr_time.timetuple())
        unix_time = int(datetime.utcnow().timestamp())
        old_unix_time = unix_time - unix_minus
        old_readable_time = datetime.fromtimestamp(old_unix_time).strftime("%d %b %Y %H:%M ")
        # print('Getting old candlesticks')
        ###TODO: KLINE INTERVAL 1 MINUTE should depend on input time frame
        fetched_data = client.get_historical_klines(self.crypto_usdt.upper(), Client.KLINE_INTERVAL_1MINUTE,
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
                    "v": row[5]
                }
            })
        for old_candlestick in old_candlesticks:
            self.add_message(old_candlestick)

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
                    self.sell_all(list(self.macd_indicator)[-1], last_close)
                    self.stop_loss_flag = True
                    self.stop_loss_counter += 1

            if (current_macd > current_signal):
                if (self.macd_flag == 0 and current_macd < 0 and not self.stop_loss_flag):
                    self.buy(list(self.macd_indicator)[-1], 50, last_close)
                self.macd_flag = 1


            elif (current_macd < current_signal):
                if (self.macd_flag == 1 and current_macd > 0):
                    self.sell_all(list(self.macd_indicator)[-1], last_close)
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

    def sell(selfself, time, amount, price):
        pass

    ###Plotting
    def plot(self):
        times = [candlestick['time'] for candlestick in self.candlesticks]
        close_values = [candlestick['close'] for candlestick in self.candlesticks]
        vwap_times = list(self.vwap_indicator)
        vwap_values = list(self.vwap_indicator.values())
        buy_times = list(self.buy_orders)
        sell_times = list(self.sell_orders)
        plt.plot(times, close_values)
        plt.plot(vwap_times, vwap_values, color="b")
        for buy_time in buy_times:
            plt.scatter(buy_time, self.buy_orders[buy_time] / 110, color="g", marker='^')
        for sell_time in sell_times:
            plt.scatter(sell_time, self.sell_orders[sell_time] / 110, color="r", marker='+')
        plt.xticks([])
        plt.show()
