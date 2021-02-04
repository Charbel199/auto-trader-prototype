import backtrader as bt
class SMAStrategy(bt.Strategy):

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(period=15)
        self.counter = 0

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        self.counter+=1
        self.log('Position #{}'.format(self.counter))
        #print(self.position)
        if not self.position:
            if self.sma > self.data.close:
                self.log("Bought5")
                self.buy(size=5)
        else:
            if self.sma < self.data.close:
                self.log("Closed")
                self.close()# Do something else