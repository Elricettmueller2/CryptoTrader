# strategies/rsi_strategy.py

import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy

class RSIStrategy(BaseStrategy):
    def __init__(self, window=14, buy_threshold=30, sell_threshold=70):
        self.window = window
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def generate_signals(self, data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0

        # Ensure no NaN values in the data (use ffill and bfill as recommended)
        data['close'] = data['close'].ffill().bfill()

        # Calculate the Relative Strength Index (RSI)
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.window).mean()

        # Avoid division by zero or NaN in RSI calculation
        rs = gain / loss
        rs = rs.replace([np.inf, -np.inf], 0)  # Replace any infinite values with 0
        rsi = 100 - (100 / (1 + rs))

        # Check for NaN values in RSI and handle them
        rsi = rsi.fillna(50)  # Set neutral RSI value for missing data

        # Debug: Check for NaN in RSI values
        if rsi.isnull().any():
            print("There are NaN values in the RSI calculation.")

        # Buy signal when RSI is below buy_threshold
        signals['signal'] = np.where(rsi < self.buy_threshold, 1.0, 0.0)

        # Sell signal when RSI is above sell_threshold
        signals['signal'] = np.where(rsi > self.sell_threshold, -1.0, signals['signal'])

        # Generate trading orders (buy = 1, sell = -1)
        signals['positions'] = signals['signal'].diff()

        # Debug: Check for NaN values in the signals
        if signals.isnull().any().any():
            print("There are NaN values in the signals after processing.")
        
        return signals

    def execute_trades(self):
        """Not implemented: this function will execute live trades."""
        pass

    def analyze_performance(self):
        """Performance analysis will be handled by the backtester."""
        pass
