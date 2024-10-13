# strategies/moving_average_crossover.py

import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy

class MovingAverageCrossoverStrategy(BaseStrategy):
    def __init__(self, short_window=50, long_window=200):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0

        # Calculate short and long moving averages
        signals['short_mavg'] = data['close'].rolling(window=self.short_window, min_periods=1).mean()
        signals['long_mavg'] = data['close'].rolling(window=self.long_window, min_periods=1).mean()

        # Avoid chained assignment by using .iloc or .loc properly
        condition = signals['short_mavg'].iloc[self.short_window:] > signals['long_mavg'].iloc[self.short_window:]
        signals.loc[signals.index[self.short_window:], 'signal'] = np.where(condition, 1.0, 0.0)

        # Generate trading orders (buy = 1, sell = -1)
        signals['positions'] = signals['signal'].diff()

        # Ensure no NaN values in the signals
        signals = signals.fillna(0)

        return signals

    def execute_trades(self):
        pass

    def analyze_performance(self):
        pass
