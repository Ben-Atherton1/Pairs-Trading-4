from data.tickers import TICKERS
from data.config import STARTING_CAPITAL
from pairs.get_data import get_backtesting_data
from pairs.validate_pairs import get_cointegrated_pairs
from backtesting.backtesting import backtest_pair

backtesting_data = get_backtesting_data()
gross_pnl, actions, total_pnl, equity_curve, sharpe_ratio = backtest_pair(TICKERS, backtesting_data=backtesting_data)

final_equity = STARTING_CAPITAL + total_pnl
max_equity = max(equity_curve)
max_draw_up = max_equity - STARTING_CAPITAL
min_equity = min(equity_curve)
max_drawdown = STARTING_CAPITAL - min_equity

print(f"Pair: {TICKERS}")
print(f"Final Equity: £{final_equity:.2f}")
print(f"Total PnL: £{total_pnl}")
print(f"Max Equity: £{max_equity}")
print(f"Min Equity: £{min_equity}")
print(f"Max Drawup: £{max_draw_up}")
print(f"Max Drawdown: £{max_drawdown}")
print(f"Sharpe Ratio: {sharpe_ratio}")

# for i in range(len(actions)):
#     print(f"{i}) Units: {actions[i]["units"]}")


