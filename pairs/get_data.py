import numpy as np
import pandas as pd
import sys
import yfinance as yf

from datetime import datetime, timedelta

from data.config import ROLLING_WINDOW, TRADING_DAYS_RATIO
from data.tickers import TICKERS

def get_market_data(tickers, start, end) -> pd.DataFrame:
    market_data = yf.download(tickers, start=start, end=end)

    if 'Adj Close' in market_data.columns:
        adjusted_data = market_data['Adj Close']
    else:
        adjusted_data = market_data['Close']

    return adjusted_data

def get_historic_data(tickers):
    start_date = datetime.now()- timedelta(days=4*365+TRADING_DAYS_RATIO*ROLLING_WINDOW)
    end_date = datetime.now()- timedelta(days=365+TRADING_DAYS_RATIO*ROLLING_WINDOW)
    historic_data = get_market_data(tickers, start_date, end_date)

    return historic_data

def get_backtesting_data(pair):
    start_date = datetime.now()- timedelta(days=365+TRADING_DAYS_RATIO*ROLLING_WINDOW)
    end_date = datetime.now()
    backtesting_data = get_market_data(pair, start_date, end_date)

    return backtesting_data