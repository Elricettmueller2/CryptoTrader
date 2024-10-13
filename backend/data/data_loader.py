# data/data_loader.py

import ccxt
import pandas as pd

def fetch_historical_data(pair, timeframe='1d', since=None, limit=1000):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol=pair, timeframe=timeframe, since=since, limit=limit)
    data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data.set_index('timestamp', inplace=True)

    # Fill missing data (forward and backward fill to avoid NaNs)
    data = data.ffill().bfill()

    # Check for any remaining NaN values
    if data.isnull().any().any():
        print("There are still NaN values in the data after filling.")

    return data
