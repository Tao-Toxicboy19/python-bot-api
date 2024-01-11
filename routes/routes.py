from fastapi import APIRouter, HTTPException, Request
from controllers.orderController import createPosition
import ccxt
from funcitons.create_order import order

from funcitons.exchange import exchange
from funcitons.setLeverage import setLeverage

router = APIRouter()

@router.post("/")
async def createPosition(request:Request):
    try:
        result = await request.json()
        apiKey = result["apiKey"]
        secretKey = result["secretKey"]
        symbol = result["symbol"]
        amount = result["amount"]
        leverage = result["leverage"]
        position = result["position"]

        exchanges = exchange(apiKey, secretKey)
        setLeverage(symbol, leverage, exchanges)

        ticker = exchanges.fetch_ticker(symbol)
        lastPrice = ticker['last']
        totalPrice = (amount / lastPrice) * leverage

        orderSet = {
            'symbol': symbol,
            'totalPrice':totalPrice,
            'lastPrice':lastPrice,
            'position':position
        }

        createOrder = order(orderSet,exchanges)

        return createOrder
    

    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/wallet")
async def wallet_balance():
    return wallet_balance()