from backtesting.trading_signals import PairSignals
from pairs.get_data import get_backtesting_data
from pairs.validate_pairs import get_hedge_ratios, get_best_spread, get_z_score

def backtest_pair(pair: list[str], backtesting_data):
    """
    Runs a backtest using unseen market data on a pair determined to be correlated and cointegrated on historical data
    """

    stock1, stock2 = pair

    pair_signals = PairSignals(pair)

    beta1, beta2 = get_hedge_ratios(stock1_data=backtesting_data[stock1], stock2_data=backtesting_data[stock2])
    spread, p_value, hedge_ratio, stock1, stock2 = get_best_spread(stock1=stock1, stock2=stock2, pair_data=backtesting_data, hedge_ratios=[beta1, beta2])
    z_score = get_z_score(spread)

    position = pair_signals.generate_positions(z_score)

    spread_returns = spread.diff()
    gross_pnl = position.shift(1) * spread_returns

    return gross_pnl