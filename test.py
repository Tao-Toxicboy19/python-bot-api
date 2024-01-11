import ccxt

apiKey = 'lTuNlO5EnfHPGiIIeY6vdQeNiPfQB16SyNIpIE8sCotKe9unmUq8u5qk7QbVCIOa'
secretKey = 'gtXa9rva2MdnNEl0rzizie0MWIBfGY1J32hRUWyjNEIr6LoOMuUh1tHIuePgkkgB'
symbol = 'ETH/USDT'  # Corrected the symbol format

exchange = ccxt.binance({
    'apiKey': apiKey,
    'secret': secretKey,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
    }
})

try:
    response = exchange.fapiprivate_post_leverage({
        "symbol": "ETHUSDT",
        "leverage":10
    })

    print(response)

    # Fetch ticker after setting leverage
    ticker = exchange.fetch_ticker(symbol)
    lastPrice = ticker['last']
    print(f'Last price of {symbol}: {lastPrice}')

except ccxt.NetworkError as e:
    print(f'Network error: {e}')
except ccxt.ExchangeError as e:
    print(f'Exchange error: {e}')
except Exception as e:
    print(f'Error: {e}')
