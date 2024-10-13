# strategies/__init__.py

from .base_strategy import BaseStrategy
from .moving_average_crossover import MovingAverageCrossoverStrategy
from .rsi_strategy import RSIStrategy
from .sma_strategy import SimpleMovingAverageStrategy  # Import the new strategy

STRATEGY_REGISTRY = {
    'moving_average_crossover': MovingAverageCrossoverStrategy,
    'rsi': RSIStrategy,
    'simple_moving_average': SimpleMovingAverageStrategy,  # Add the SMA strategy
}
