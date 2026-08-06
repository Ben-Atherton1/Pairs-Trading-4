from data.tickers import TICKERS
from data.config import STARTING_CAPITAL
from pairs.get_data import get_backtesting_data
from pairs.validate_pairs import get_correlated_pairs, get_cointegrated_pairs
from backtesting.backtesting import backtest_pair



failed_tickers, correlated_pairs, historical_data = get_correlated_pairs(TICKERS)
print(f"Failed Tickers: {failed_tickers}")

if failed_tickers:
    cleaned_tickers = [ticker for ticker in TICKERS if ticker not in failed_tickers]
    failed_tickers, correlated_pairs, historical_data = get_correlated_pairs(cleaned_tickers)

cointegrated_pairs = get_cointegrated_pairs(correlated_pairs, historical_data)
print(f"No. Correlated Pairs: {len(correlated_pairs)}")
print(f"No. Cointegrated Pairs: {len(cointegrated_pairs)}")


#BACKTEST EACH PAIR

profiting_pairs = []

for pair in cointegrated_pairs:

    unpacked_pair = [pair[0][0], pair[0][1]]
    print(unpacked_pair)
    backtesting_data = get_backtesting_data(unpacked_pair)


    gross_pnl, actions, total_pnl, equity_curve, sharpe_ratio = backtest_pair(unpacked_pair, backtesting_data=backtesting_data)

    try:
        final_equity = STARTING_CAPITAL + total_pnl
        max_equity = max(equity_curve)
        max_draw_up = max_equity - STARTING_CAPITAL
        min_equity = min(equity_curve)
        max_drawdown = STARTING_CAPITAL - min_equity

        print(f"Pair: {pair}")
        print(f"Final Equity: £{final_equity:.2f}")
        print(f"Total PnL: £{total_pnl}")
        print(f"Max Equity: £{max_equity}")
        print(f"Min Equity: £{min_equity}")
        print(f"Max Drawup: £{max_draw_up}")
        print(f"Max Drawdown: £{max_drawdown}")
        print(f"Sharpe Ratio: {sharpe_ratio}")

        if total_pnl > 0:
            profiting_pairs.append([pair, total_pnl])

    except Exception as e:
        print(f"Exception Raised: {e}")
        continue

print(f"No. profiting pairs: {len(profiting_pairs)}")
print(f"Profiting Pairs: {profiting_pairs}")

# for i in range(len(actions)):
#     print(f"{i}) Units: {actions[i]["units"]}")


