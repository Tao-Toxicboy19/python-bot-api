import ccxt

def wallet_balance(api_key, secret_key, coin_symbol=None):
    exchange = ccxt.binance({
        'apiKey': api_key,  # Use the provided API key
        'secret': secret_key,  # Use the provided Secret key
    })

    try:
        # Fetch the balance of all assets in the wallet
        wallet_balance = exchange.fetch_balance()

        if coin_symbol:
            # If a specific coin symbol is provided, filter the balance for that coin
            coin_balance = next((balance for balance in wallet_balance['info']['balances'] if balance['asset'] == coin_symbol), None)
            return coin_balance
        else:
            # If no specific coin symbol is provided, return the entire wallet balance
            return wallet_balance

    except ccxt.NetworkError as e:
        print(f'Network error: {e}')
    except ccxt.ExchangeError as e:
        print(f'Exchange error: {e}')
    except Exception as e:
        print(f'Error: {e}')

# Example usage
api_key = 'lTuNlO5EnfHPGiIIeY6vdQeNiPfQB16SyNIpIE8sCotKe9unmUq8u5qk7QbVCIOa'
secret_key = 'gtXa9rva2MdnNEl0rzizie0MWIBfGY1J32hRUWyjNEIr6LoOMuUh1tHIuePgkkgB'
coin_symbol = 'USDT'  # Set to None if you want the balance for all coins

balance = wallet_balance(api_key, secret_key, coin_symbol)
print(balance)
