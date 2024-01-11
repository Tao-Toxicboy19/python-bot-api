from fastapi import APIRouter
import ccxt

router = APIRouter()

async def wallet_balance(api_key, secret_key, coin_symbol=None):
    exchange = ccxt.binance({
        'apiKey': api_key,
        'secret': secret_key,
    })

    try:
        wallet_balance = await exchange.fetch_balance()

        if coin_symbol:
            coin_balance = next((balance for balance in wallet_balance['info']['balances'] if balance['asset'] == coin_symbol), None)
            return coin_balance
        else:
            return wallet_balance

    except ccxt.NetworkError as e:
        print(f'Network error: {e}')
    except ccxt.ExchangeError as e:
        print(f'Exchange error: {e}')
    except Exception as e:
        print(f'Error: {e}')

@router.post("/wallet")
async def get_wallet_balance(api_key: str, secret_key: str, coin_symbol: str = None):
    return await wallet_balance(api_key, secret_key, coin_symbol)
