import pandas as pd
import numpy as np

from data.config import ENTRY_THRESHOLD, EXIT_THRESHOLD, STOP_THRESHOLD

class PairSignals:
    def __init__(self, pair):
        self.pair = pair

    def generate_positions(self, z_score):
        position = pd.Series(0, index=z_score.index)

        for i in range(1, len(z_score)):
            z = z_score.iloc[i]
            prev = position.iloc[i - 1]

            if np.isnan(z):
                position.iloc[i] = 0
                continue

            if prev == 0:
                if z < -ENTRY_THRESHOLD:
                    position.iloc[i] = 1 #Enter Long Trade
                elif z > ENTRY_THRESHOLD:
                    position.iloc[i] = -1 #Enter Short Trade
                else:
                    position.iloc[i] = 0
            elif prev > 0:
                if z > -EXIT_THRESHOLD or z < -STOP_THRESHOLD:
                    position.iloc[i] = 0
                else:
                    position.iloc[i] = prev
            elif prev < 0:
                if z < EXIT_THRESHOLD or z > STOP_THRESHOLD:
                    position.iloc[i] = 0
                else:
                    position.iloc[i] = prev

        return position
