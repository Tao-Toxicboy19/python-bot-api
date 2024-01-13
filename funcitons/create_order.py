
def order(orderSet,exchanges):
    try:
        symbol = orderSet["symbol"]
        totalPrice = orderSet["totalPrice"]
        lastPrice = orderSet["lastPrice"]
        position = orderSet["position"]

        if(position == "LONG"):
            order = exchanges.create_limit_buy_order(symbol, totalPrice, lastPrice, params={
                'positionSide': position,
                'isIsolated': 'TRUE',
            })

        elif(position == "SHORT"):
           order = exchanges.create_limit_sell_order(symbol, totalPrice, lastPrice, params={
                'positionSide': position,
                'isIsolated': 'TRUE',
            })
        else:
           return None

        return order

    except Exception as e:
    # Handle the exception here
     print(f"An error occurred: {e}")