import numpy as np
import pandas as pd
import statsmodels.api as sm
import sys

from statsmodels.tsa.stattools import adfuller, coint

from data.config import COINTEGRATION_THRESHOLD, CORRELATION_THRESHOLD, ROLLING_WINDOW, STATIONARY_TEST_THRESHOLD
from pairs.get_data import get_historic_data

def get_correlated_pairs():
    historical_data = get_historic_data()
    correlation_matrix = historical_data.corr()

    correlated_pairs = []

    tickers = correlation_matrix.columns

    # Only look at upper triangle (i < j)
    for i in range(len(tickers)):
        for j in range(i + 1, len(tickers)):
            corr_value = correlation_matrix.iloc[i, j]
            if corr_value > CORRELATION_THRESHOLD:
                correlated_pairs.append(
                    (tickers[i], tickers[j], corr_value)
                )

    return correlated_pairs

def get_cointegrated_pairs(correlated_pairs, market_data: pd.DataFrame):
    cointegrated_pairs = []

    for pair in correlated_pairs:
        stock1, stock2 = market_data[pair[0]], market_data[pair[1]]
        aligned_stocks = pd.concat([stock1, stock2], axis=1)

        cointegration_test = coint(aligned_stocks[pair[0]], aligned_stocks[pair[1]])
        p_value = cointegration_test[1]

        if p_value <= COINTEGRATION_THRESHOLD:
            cointegrated_pairs.append([pair, aligned_stocks])

    return cointegrated_pairs

def calculate_hedge_ratio(dependent_stock, independent_stock):
    X = sm.add_constant(independent_stock)
    model = sm.OLS(dependent_stock, X).fit()

    # dependent_stock = constant + hedge_ratio * independent_stock + epsilon,
    # where epsilon is a stationary series. As a result,
    # dependent_stock - hedge_ratio * independent_stock is stationary
    hedge_ratio = model.params[independent_stock.name]

    return hedge_ratio

def get_hedge_ratios(stock1_data, stock2_data):

    beta1 = calculate_hedge_ratio(stock1_data, stock2_data)
    beta2 = calculate_hedge_ratio(stock2_data, stock1_data)    

    return beta1, beta2

def get_best_spread(stock1, stock2, pair_data, hedge_ratios):

    spread1 = pair_data[stock1] - hedge_ratios[0] * pair_data[stock2]
    spread2 = pair_data[stock2] - hedge_ratios[1] * pair_data[stock1]

    p_value1 = adfuller(spread1)[1]
    p_value2 = adfuller(spread2)[1]

    if p_value1 < p_value2:
        return spread1, p_value1, hedge_ratios[0], stock1, stock2
    else:
        return spread2, p_value2, hedge_ratios[1], stock2, stock1

def get_z_score(spread):
    rolling_mean = spread.rolling(window=ROLLING_WINDOW).mean()
    rolling_std = spread.rolling(window=ROLLING_WINDOW).std()
    z_score = (spread - rolling_mean) / rolling_std
    return z_score