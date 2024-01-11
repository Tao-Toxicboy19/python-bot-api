import ccxt

def lastPrice(symbol,exchange):
    try:
        ticker = exchange.fetch_ticker(symbol)
        lastPrice  = ticker['last']
        
        return lastPrice 

    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {e}")