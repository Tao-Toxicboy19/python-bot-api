from http.client import HTTPException


def closePositions(exchanges,setPositions):
    try: 
        symbol = setPositions['symbol']
        totalPrice = setPositions['totalPrice']
        lastPrice = setPositions['lastPrice']
        position = setPositions['position']
        status = setPositions['status']
        print(status)
        
        if(status == 'SHORT'):
            close = exchanges.create_market_buy_order(symbol, totalPrice, params={
                'positionSide': 'SHORT',
            })
        elif(status == 'LONG'):
            close = exchanges.create_market_sell_order(symbol, totalPrice, params={
                'positionSide': 'LONG',
            })
        else:
            return None

        return close

    except Exception as e:
        # Handle the exception here
        print(f'An error occurred: {e}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
        