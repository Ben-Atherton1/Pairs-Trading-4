import pandas as pd

from backtesting.trading_signals import PairSignals
from pairs.validate_pairs import get_hedge_ratios, get_best_spread, get_z_score

def backtest_pair(pair: list[str, str], backtesting_data):
    """
    Runs a backtest using unseen market data on a pair determined to be correlated and cointegrated on historical data
    """

    stock1 = pair[0]
    stock2 = pair[1]

    stock1_data = backtesting_data[stock1][stock1]
    stock2_data = backtesting_data[stock2][stock2]

    pair_signals = PairSignals(pair)

    beta1, beta2 = get_hedge_ratios(stock1_data=stock1_data, stock2_data=stock2_data)
    spread, p_value, hedge_ratio, stock1, stock2 = get_best_spread(stock1=stock1, stock2=stock2, pair_data=backtesting_data, hedge_ratios=[beta1, beta2])
    z_score = get_z_score(spread)

    position = pair_signals.generate_positions(z_score)

    #Price Data for stock1 and stock2
    price1 = backtesting_data[stock1][stock1]
    price2 = backtesting_data[stock2][stock2]

    previous_position = 0
    actions = []
    for t in position.index:
        current_position = position.loc[t]
        current_price1 = price1.loc[t]
        current_price2 = price2.loc[t]

        if previous_position == 0 and current_position == 1:
            action = "Enter Long"
        elif previous_position == 0 and current_position == -1:
            action = "Enter Short"
        elif previous_position != 0 and current_position == 0:
            action = "Exit"
        elif current_position == 1:
            action = "Hold Long"
        elif current_position == -1:
            action = "Hold Short"
        else:
            action = "Flat"

        actions.append({
            "timestamp": t,
            "action": action,
            "position": current_position,
            "stock1_px": current_price1,
            "stock2_px": current_price2
        })

        previous_position = current_position

    #Returns on stock1 and stock2
    return1 = price1.pct_change()
    return2 = price2.pct_change()

    gross_pnl = position.shift(1) * (return1 - hedge_ratio * return2)
    total_pnl = gross_pnl.sum()
    equity_curve = gross_pnl.cumsum()


    return gross_pnl, actions, total_pnl, equity_curve