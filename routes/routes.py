from fastapi import APIRouter, HTTPException, Request
import ccxt
from funcitons.calulate_ema import calculateEMA, fetchOkexData
from funcitons.close_position import closePositions
from funcitons.create_order import order
from funcitons.exchange import exchange
from funcitons.setLeverage import setLeverage

router = APIRouter()

@router.post("/calulate/ema")
async def calculate(request: Request):
    try:
        result = await request.json()
        symbols = result["symbols"]
        tf = result["tf"]
        value = tf[0]["value"]
        timeFrame = tf[0]["timeFrame"]

        since = ccxt.binance().milliseconds() - value
        coinsValue = []

        for i in symbols:
            symbol = i["symbol"]
            ema = i.get("ema")
            if ema is None:
                ema = 15
            limit = ema * 2
            symbol_data = fetchOkexData(symbol, timeFrame, since, limit)
            calculateEMA(symbol_data, ema)
            latest_two_entries = symbol_data.iloc[-3:]

            latestOpenPrices = latest_two_entries["close"].tolist()
            latestOpenEma = latest_two_entries["ema"].tolist()

            latestOpenPrice_1 = latestOpenPrices[-1]
            latestOpenPrice_2 = latestOpenPrices[-2]
            latestOpenEma_1 = latestOpenEma[-1]
            latestOpenEma_2 = latestOpenEma[-2]

            if latestOpenEma_2 >= latestOpenPrice_2:
                if latestOpenEma_1 <= latestOpenPrice_1:
                    coinsValue.append({"symbol": symbol, "timeframe": timeFrame, "position": "LONG"})
            if latestOpenEma_2 <= latestOpenPrice_2:
                if latestOpenEma_1 >= latestOpenPrice_1:
                    coinsValue.append({"symbol": symbol, "timeframe": timeFrame, "position": "SHORT"})

        return coinsValue

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")