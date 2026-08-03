import numpy as np
import pandas as pd
import sys
import yfinance as yf

from datetime import datetime, timedelta

from data.config import ROLLING_WINDOW, TRADING_DAYS_RATIO
from data.tickers import TICKERS

def get_market_data(tickers, start_date, end_date):

    all_data = []

    for ticker in tickers:
        df = yf.download(tickers=ticker, start=start_date, end=end_date)
        df['ticker'] = ticker
        all_data.append(df)

    combined_market_data = pd.concat(all_data)
    combined_market_data = combined_market_data.sort_index()

    if 'Adj Close' in combined_market_data.columns:
        adjusted_data = combined_market_data.pivot_table(
            values='Adj Close', index=combined_market_data.index, columns='ticker'
        )
    else:
        adjusted_data = combined_market_data.pivot_table(
            values='Close', index=combined_market_data.index, columns='ticker'
        )

    return adjusted_data

def get_historic_data():
    start_date = datetime.now()- timedelta(days=4*365+TRADING_DAYS_RATIO*ROLLING_WINDOW)
    end_date = datetime.now()- timedelta(days=365*TRADING_DAYS_RATIO*ROLLING_WINDOW)
    historic_data = get_market_data(TICKERS, start_date, end_date)

    return historic_data

def get_backtesting_data():
    start_date = datetime.now()- timedelta(days=365+TRADING_DAYS_RATIO*ROLLING_WINDOW)
    end_date = datetime.now()
    backtesting_data = get_market_data(TICKERS, start_date, end_date)

    return backtesting_data