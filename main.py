from data.tickers import TICKERS
from pairs.get_data import get_backtesting_data
from pairs.validate_pairs import get_cointegrated_pairs
from backtesting.backtesting import backtest_pair

backtesting_data = get_backtesting_data()
backtest_pair(TICKERS, backtesting_data=backtesting_data)