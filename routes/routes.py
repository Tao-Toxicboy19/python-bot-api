from fastapi import APIRouter, HTTPException, Request
import ccxt
from funcitons.create_order import order
from funcitons.exchange import exchange
from funcitons.setLeverage import setLeverage

router = APIRouter()

@router.post("/order")
async def createPosition(request:Request):
    try:
        result = await request.json()

        orders = []

        for item in result:
            # ดึงข้อมูลจากแต่ละรายการ JSON
            symbol = item["symbol"]
            leverage = item["leverage"]
            amount = item["amount"]
            apiKey = item["Users"]["key"][0]["apiKey"]
            secretKey = item["Users"]["key"][0]["secretKey"]
            position = item["position"]

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

            orders.append(createOrder)

        return orders

    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/wallet")
async def wallet_balance():
    return wallet_balance()