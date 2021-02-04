import backtrader as bt

class RSIStrategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=15)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.buy(size=5)
        else:
            if self.rsi > 70:
                self.close()

