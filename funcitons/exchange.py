import ccxt

def exchange(apiKey, secretKey):
    try:
        exchange = ccxt.binance({
            'apiKey': apiKey,
            'secret': secretKey,
            'enableRateLimit': True,    
            'options': {
                'defaultType': 'future',
            }
        })
                  
        return exchange
    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {e}")
