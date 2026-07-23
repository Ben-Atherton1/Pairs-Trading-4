import pandas as pd

from data.config import ENTRY_THRESHOLD, EXIT_THRESHOLD, STOP_THRESHOLD

class Signals:
    def __init__(self):
        self.in_trade = False

    def generate_positions(self, z_score):
        pass