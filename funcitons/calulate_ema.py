import ccxt
import pandas as pd

findData = ccxt.binance()

def fetchOkexData(symbol, timeframe, since, limit):
    ohlcv = findData.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

def calculateEMA(df, span):
    df['ema'] = df['close'].ewm(span=span, adjust=False).mean()