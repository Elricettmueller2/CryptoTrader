# backtesting/backtester.py

import pandas as pd

class Backtester:
    def __init__(self, strategy, data, initial_capital=10000.0):
        self.strategy = strategy
        self.data = data
        self.initial_capital = initial_capital
        self.positions = None
        self.portfolio = None

    def run_backtest(self):
        signals = self.strategy.generate_signals(self.data)

        # Ensure no NaN values in signals before proceeding
        signals = signals.fillna(0)

        self.positions = signals['signal']

        # Debug: Check if any positions were created
        print(f"Total positions generated: {self.positions.sum()}")

        # Calculate portfolio performance
        self.calculate_portfolio_performance(signals)

        # Debug: Check initial portfolio value
        if self.portfolio['total'].iloc[0] == 0:
            print("Initial portfolio value is 0, which causes division by zero in performance calculations.")
        if self.positions.sum() == 0:
            print("No positions were generated during the backtest, hence no trades were made.")

        return self.portfolio

    def calculate_portfolio_performance(self, signals):
        positions = pd.DataFrame(index=signals.index).fillna(0.0)
        positions['positions'] = signals['positions']
        
        # Calculate cumulative positions held (number of units)
        positions['cum_positions'] = positions['positions'].cumsum()
        
        # Ensure cumulative positions are not negative (no short selling)
        positions['cum_positions'] = positions['cum_positions'].clip(lower=0)
        
        # Calculate holdings and cash
        portfolio = pd.DataFrame(index=positions.index)
        portfolio['holdings'] = positions['cum_positions'] * self.data['close']
        trade_value = positions['positions'] * self.data['close']
        portfolio['cash'] = self.initial_capital - trade_value.cumsum()
        
        # Ensure cash doesn't go negative
        portfolio['cash'] = portfolio['cash'].clip(lower=0)
        
        portfolio['total'] = portfolio['cash'] + portfolio['holdings']
        portfolio['returns'] = portfolio['total'].pct_change().fillna(0)
        
        self.portfolio = portfolio

