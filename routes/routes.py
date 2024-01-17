from fastapi import APIRouter, HTTPException, Request
import ccxt
from funcitons.calulate_ema import calculateEMA, fetchOkexData
from funcitons.close_position import closePositions
from funcitons.create_order import order
from funcitons.exchange import exchange
from funcitons.setLeverage import setLeverage
from typing import List

router = APIRouter()

@router.post("/open/order")
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

@router.post("/calulate/ema")
async def calculate(request: Request):
    try:
        result = await request.json()

        limit = 30
        symbols = result["symbols"]
        tf = result["tf"][0]
        value = tf["value"]
        timeFrame = tf["timeFrame"]

        since = ccxt.binance().milliseconds() - value

        coinsValue = []

        for i in symbols:
            symbol = i["name"]
            symbol_data = fetchOkexData(symbol, timeFrame, since, limit)
            calculateEMA(symbol_data)
            latest_two_entries = symbol_data.iloc[-3:]

            latestOpenPrices = latest_two_entries["close"].tolist()
            latestOpenEma = latest_two_entries["ema"].tolist()

            latestOpenPrice_2 = latestOpenPrices[-2]
            latestOpenPrice_3 = latestOpenPrices[-3]
            latestOpenEma_2 = latestOpenEma[-2]
            latestOpenEma_3 = latestOpenEma[-3]

            if latestOpenEma_3 >= latestOpenPrice_3:
                if latestOpenEma_2 <= latestOpenPrice_2:
                    coinsValue.append({"symbol": symbol, "timeframe": timeFrame, "position": "LONG"})
            if latestOpenEma_3 <= latestOpenPrice_3:
                if latestOpenEma_2 >= latestOpenPrice_2:
                    coinsValue.append({"symbol": symbol, "timeframe": timeFrame, "position": "SHORT"})

        return coinsValue

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/close/order")
async def closeOrder(request: Request):
    try:
        result = await request.json()
        
        closed = []

        for item in result:
            apiKey = item["Users"]["key"][0]["apiKey"]
            secretKey = item["Users"]["key"][0]["secretKey"]
            symbol = item['symbol']
            amount = item['amount']
            leverage = item['leverage']
            status = item['status']
            position = item['position']

            if(status == position):
                return
            
            exchanges = exchange(apiKey, secretKey)
            setLeverage(symbol,leverage,exchanges)
    
            ticker = exchanges.fetch_ticker(symbol)
            lastPrice = ticker['last']
            totalPrice = (amount / lastPrice) * leverage
        
            setPositions = {
                'symbol': symbol,
                'totalPrice': totalPrice,
                'lastPrice': lastPrice,
                'status': status,
                'position':position
            }

            closeOrder = closePositions(exchanges, setPositions)
            closed.append(closeOrder)
            
        return closed 
     
    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
        