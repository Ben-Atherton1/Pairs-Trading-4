Pairs trading is a mean-reversion strategy which trades stock pairs which are closely related, correlated, and cointegrated.

It is a good idea to choose a specific sector or market in which to look for closely related pairs in. This program screens the Nasdaq-100.

To identify correlated pairs, Pearson's correlation coefficient is calculated for every possible pair and those with a coefficient sufficiently close to 1 are returned. Correlated pairs are then tested for cointegration: a statistical property where two time series have a stable long-term equilibrium.

Cointegration is tested with the Engle-Granger method. For pairs trading, this means a stable spread exists for cointegrated pairs. This spread has a constant mean. Keeping track of the spread via Z-score allows us to place trades, expecting the pair to revert back to the stable equilibrium. This looks like shorting one stock when the price is greater than the mean whilst entering long positions on the other when the price is significantly less than the mean.
