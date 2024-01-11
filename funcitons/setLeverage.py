import ccxt


def setLeverage(symbol,leverage,exchange):
    try:
        newSymbol = symbol.replace('/', '')
        res = exchange.fapiprivate_post_leverage({
            "symbol": newSymbol,
            "leverage":leverage
        })               
        print(res)
    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {e}")