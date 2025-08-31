# Stocks-Hirish
### Setup

```
python3 -m venv ~/stocks 
source ~/stocks/bin/activate
python3 -m pip install backtesting
pip install yfinance
pip install matplotlib
```

```
source ~/stocks/bin/activate
```

```
python3 RothIRA/RothIRA.py
```





### Strategies (Add More)
- sma_strategy1.py: A simple crossover strategy. Once the 10 day SMA exceeds the 20 day SMA buy more stock. Otherwise sell some stock.

### Purpose
- Play around with different strategies (simple) and decide on how to evaluate them (for fun :))
- Pipeline: Scrape Data YFinance -> Create Strategy -> Backtest Strategy -> Repeat
 
### Terminology
- Backtesting: Asseses the viability of a trading model by simulating how it would have played out retrospectively.
The issue with backtesting is that you can overfit to historical data which will yield garbage data w/respect to the future. 
- Simple Moving Average (SMA): An average of a stocks-price taken for the past X days and stored continuously.
- Drawdown: A period of time when the stock decreases from a peak till it reaches the peak again. 
- Volatility: Standard deviation of stock returns (per day?) over some given time period.



