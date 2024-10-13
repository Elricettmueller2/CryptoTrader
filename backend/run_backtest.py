# run_backtest.py

''' Use different strats with following terminal messages

    1#/  Moving average cross : 
    
        python -m backend.run_backtest --strategy moving_average_crossover --params '{"short_window":50,"long_window":200}'

    2#/ Rsi

        python -m backend.run_backtest --strategy rsi --params '{"window":14,"buy_threshold":30,"sell_threshold":70}'

'''

import argparse
from .data.data_loader import fetch_historical_data
from .backtesting.backtester import Backtester
from .backtesting.performance import calculate_performance_metrics
from .strategies import STRATEGY_REGISTRY

def main():
    parser = argparse.ArgumentParser(description='Backtest trading strategies.')
    parser.add_argument('--strategy', type=str, required=True, help='Strategy name')
    parser.add_argument('--symbol', type=str, default='BTC/USDT', help='Trading pair symbol')
    parser.add_argument('--timeframe', type=str, default='1d', help='Timeframe for data')
    parser.add_argument('--params', type=str, help='Strategy parameters in JSON format')
    args = parser.parse_args()

    # Fetch historical data
    data = fetch_historical_data(args.symbol, timeframe=args.timeframe)

    # Get strategy class from registry
    StrategyClass = STRATEGY_REGISTRY.get(args.strategy)
    if not StrategyClass:
        raise ValueError(f"Strategy '{args.strategy}' not found.")

    # Parse strategy parameters
    import json
    parameters = json.loads(args.params) if args.params else {}
    strategy = StrategyClass(**parameters)

    # Generate signals and run backtest
    signals = strategy.generate_signals(data)
    backtester = Backtester(strategy, data)
    portfolio = backtester.run_backtest()

    # Calculate performance metrics
    metrics = calculate_performance_metrics(portfolio)
    print("Performance Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value:.2%}")

    if portfolio['total'].isnull().any():
        print("There are NaN values in the portfolio. Check your calculations.")

        # Check for NaN in data or signals
    if data['close'].isnull().any():
        print("There are NaN values in the data.")
    if signals.isnull().any().any():
        print("There are NaN values in the signals.")

        # Fetch historical data
    data = fetch_historical_data(args.symbol, timeframe=args.timeframe)

    # Check for NaN values in the data
    if data.isnull().any().any():
        print("There are NaN values in the fetched historical data.")



    # Plot results
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12,6))
    plt.plot(data['close'], label='Close Price', alpha=0.5)
    buy_signals = signals.loc[signals['positions'] == 1.0]
    sell_signals = signals.loc[signals['positions'] == -1.0]
    plt.plot(buy_signals.index, data.loc[buy_signals.index]['close'], '^', markersize=10, color='g', label='Buy Signal')
    plt.plot(sell_signals.index, data.loc[sell_signals.index]['close'], 'v', markersize=10, color='r', label='Sell Signal')
    plt.title('Price Chart with Trade Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
