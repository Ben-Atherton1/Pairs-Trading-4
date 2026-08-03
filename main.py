from data.tickers import TICKERS
from pairs.get_data import get_backtesting_data
from pairs.validate_pairs import get_cointegrated_pairs
from backtesting.backtesting import backtest_pair

backtesting_data = get_backtesting_data()
gross_pnl, actions, total_pnl, equity_curve = backtest_pair(TICKERS, backtesting_data=backtesting_data)

print(f"PnL: {gross_pnl}")
print(f"Total PnL: {total_pnl}")
print(equity_curve)
