# strategies/base_strategy.py

from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    @abstractmethod
    def generate_signals(self, data):
        """Generate trading signals based on data."""
        pass

    @abstractmethod
    def execute_trades(self):
        """Execute trades based on generated signals."""
        pass

    @abstractmethod
    def analyze_performance(self):
        """Analyze the performance of the strategy."""
        pass
