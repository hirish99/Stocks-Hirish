from backtesting import Backtest
import datetime
from scraper import get_history
from sma_strategy1 import SmaCross
import numpy as np

s = np.datetime64('2003-09-01')
f = np.datetime64('2011-09-15')
def get_stats(start_date, end_date, data, cash):
    filtered_data = data[(data.index >= s)
                        & (data.index < f)]

    bt = Backtest(filtered_data, SmaCross, cash=cash, commission=.002,
                exclusive_orders=True)
    stats = bt.run()
    return stats

stats = get_stats(s, f, get_history('aapl'), 10000)
print(stats)
print(stats['Return (Ann.) [%]'])