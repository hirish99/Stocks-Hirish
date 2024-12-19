from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
from scraper import get_history
import datetime
import numpy as np

from evaluation import get_stats

class SmaCross1(Strategy):
    '''
    If 10 day moving average crosses 20 day moving average
    buy (full equity), if not sell (full equity).
    '''
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()

class SmaCross2(Strategy):
    '''
    If 10 day moving average crosses 20 day moving average
    buy (full equity), if not sell (50% of equity).
    '''
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell(size=.5)

s = np.datetime64('2020-01-01')
f = np.datetime64('2024-01-01')
stats1 = get_stats(s, f, get_history('aapl'), 10000, SmaCross1)
stats2 = get_stats(s, f, get_history('aapl'), 10000, SmaCross2)

print(stats1)
print(stats2)
print("SMA Strat 1: ", stats1['Return (Ann.) [%]'])
print("SMA Strat 2: ", stats2['Return (Ann.) [%]'])
print("Buy/Hold Return: ", stats1['Buy & Hold Return [%]'])