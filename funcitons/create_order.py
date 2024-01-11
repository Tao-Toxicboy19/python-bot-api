import ccxt

from funcitons.exchange import exchange

def order(orderSet,exchange):
    try:
       symbol = orderSet["symbol"]
       totalPrice = orderSet["totalPrice"]
       lastPrice = orderSet["lastPrice"]
       position = orderSet["position"]
       
       order = exchange.create_limit_buy_order(symbol, totalPrice, lastPrice, params={
                'positionSide': position,
            })
       return order


    except Exception as e:
    # Handle the exception here
     print(f"An error occurred: {e}")