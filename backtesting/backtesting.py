import pandas as pd
import numpy as np

from data.config import RISK_FREE_RATE, ANNUAL_TRADING_DAYS, STARTING_CAPITAL, PORTFOLIO_PORTION_INVESTED_PER_TRADE
from backtesting.trading_signals import PairSignals
from pairs.validate_pairs import get_hedge_ratios, get_best_spread, get_z_score

# def get_sharpe_ratio(capital_series):
#     returns = capital_series.pct_change().dropna()
#     valid_returns = returns[(capital_series.shift(1) > 0) & (capital_series > 0)]
#     daily_risk_free_rate = RISK_FREE_RATE / ANNUAL_TRADING_DAYS
#     excess_returns = valid_returns - daily_risk_free_rate
#     mean_return = excess_returns.mean()
#     std_return = excess_returns.std()

#     sharpe_ratio = (ANNUAL_TRADING_DAYS ** 0.5) * mean_return / std_return

#     return sharpe_ratio

def get_sharpe_ratio(returns: pd.Series):
    """
    Calculates the annualized Sharpe ratio for a backtest.
    """

    # Convert annual risk-free rate to per-period
    rf_per_period = RISK_FREE_RATE / ANNUAL_TRADING_DAYS

    # Excess returns
    excess = returns - rf_per_period

    # Mean and std of excess returns
    mean_excess = excess.mean()
    std_excess = excess.std(ddof=1)  # sample std

    if std_excess == 0:
        return np.nan

    # Annualize Sharpe
    sharpe_ratio = np.sqrt(ANNUAL_TRADING_DAYS) * (mean_excess / std_excess)
    return sharpe_ratio

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


    def compute_trade_units(price1, price2, hedge_ratio, trade_capital):
        """
        Computes the number of spread units to trade based on available capital.

        For a long trade:
            Long: units of stock1
            Short: units * hedge_ratio of stock2
        """
        spread_notional = price1 + abs(hedge_ratio) * price2
        units = trade_capital / spread_notional
        return min(units, equity * PORTFOLIO_PORTION_INVESTED_PER_TRADE)


    previous_position = 0
    actions = []

    equity = STARTING_CAPITAL
    equity_curve = []

    #Returns on stock1 and stock2
    return1 = price1.pct_change()
    return2 = price2.pct_change()

    gross_pnl_series = []

    for t in position.index:
        current_position = position.loc[t]
        current_price1 = price1.loc[t]
        current_price2 = price2.loc[t]

        trade_capital = equity * PORTFOLIO_PORTION_INVESTED_PER_TRADE

        units = compute_trade_units(current_price1, current_price2, hedge_ratio, trade_capital)

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
            "stock2_px": current_price2,
            "units": units
        })

        # Compute PnL only when we have returns
        if current_position != 0 and not np.isnan(return1.loc[t]) and not np.isnan(return2.loc[t]):
            if t in return1.index and t in return2.index:

                #Price Changes
                price_change1 = current_price1 - price1.shift(1).loc[t]
                price_change2 = current_price2 - price2.shift(1).loc[t]

                
                # Long leg: stock1
                long_leg_pnl = units * current_position * price_change1

                # Short leg: stock2 (hedge_ratio units)
                short_leg_pnl = -units * current_position * hedge_ratio * price_change2

                # Total spread PnL
                pnl = long_leg_pnl + short_leg_pnl

                gross_pnl_series.append(pnl)

                equity += pnl
                
        equity_curve.append(equity)

        previous_position = current_position

    total_pnl = sum(gross_pnl_series)
    returns = pd.Series(equity_curve).pct_change().dropna()
    sharpe_ratio = get_sharpe_ratio(returns)

    return gross_pnl_series, actions, total_pnl, equity_curve, sharpe_ratio