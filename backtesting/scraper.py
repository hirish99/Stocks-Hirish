import yfinance as yf
from backtesting.test import GOOG
import numpy as np

def get_history(ticker, start=None, end=None):
    tick = yf.Ticker(ticker)
    if start==None and end==None:
        df = tick.history(period='max')[['Open','High','Low','Close','Volume']]
    else:
        df = tick.history(start=start,end=end)[['Open','High','Low','Close','Volume']]
    df.index = df.index.date
    df.index = df.index.astype("datetime64[ns]")
    return df
