def setLeverage(symbol,leverage,exchange):
    try:
        newSymbol = symbol.replace('/', '')
        exchange.fapiprivate_post_leverage({
            "symbol": newSymbol,
            "leverage":leverage
        })               
    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {e}")