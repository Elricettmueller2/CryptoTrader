# strategies/sma_strategy.py

import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy

class SimpleMovingAverageStrategy(BaseStrategy):
    def __init__(self, window=50):
        self.window = window

    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0

        # Ensure no NaN values in the data (ffill and bfill to fill missing values)
        data['close'] = data['close'].ffill().bfill()

        # Calculate the simple moving average (SMA)
        sma = data['close'].rolling(window=self.window, min_periods=1).mean()

        # Buy when price is above the SMA, sell when price is below
        signals['signal'] = np.where(data['close'] > sma, 1.0, -1.0)

        # Debug: Check for NaN values in the signals
        if signals.isnull().any().any():
            print("There are NaN values in the signals after processing.")

        # Fill NaN values in signals with 0 to ensure valid output
        signals = signals.fillna(0)

        # Generate trading orders (buy = 1, sell = -1)
        signals['positions'] = signals['signal'].diff()

        return signals

    def execute_trades(self):
        """Not implemented: this function will execute live trades."""
        pass

    def analyze_performance(self):
        """Performance analysis will be handled by the backtester."""
        pass
