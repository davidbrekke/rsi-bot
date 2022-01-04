import websocket, json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import config

# CONSTANTS
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "ETHUSD"
TRADE_QUANTITY = 0.001

closes = []
in_position = False

# instantiate binance client
client = Client(config.API_KEY, config.API_SECRET, tld='us')

# @FUNCTION:
#   order
# @DESCRIPTION:
#   place an order on binance
# @PARAMS:
#   side: SIDE_BUY or SIDE_SELL
#   quantity: float
#   symbol: string
#   type: ORDER_TYPE_MARKET or ORDER_TYPE_LIMIT
# @RETURN:
#   True if order was placed successfully
#   False if order was not placed successfully
def order(side, quantity, symbol, type=ORDER_TYPE_MARKET):
    try:
        order = client.create_order(symbol=symbol, side=side, type=type, quantity=quantity)
        print(f"{side} {quantity} {symbol}")
        print('sending order')
        print(order)
    except Exception as e:
        print(e)
        return False
    return True

# @FUNCTION:
#   on_open
# @DESCRIPTION:
#   run on websocket open
# @PARAMS:
#   ws: websocket
def on_open(ws):
    print("--- opened connection ---")

# @FUNCTION:
#   on_close
# @DESCRIPTION:
#   run on websocket close
# @PARAMS:
#   ws: websocket
#   code_status_code: int
#   close_msg: string
def on_close(ws, close_status_code, close_msg):
    print("-- closing --")
    print(f"close status code: {close_status_code}")
    print(f"close message: {close_msg}")
    print("--- closed connection ---")

# @FUNCTION:
#   on_message
# @DESCRIPTION:
#   run on every message received from the websocket
def on_message(ws, message):
    # global vars
    global closes, in_position
    print("- received message -")
    # parse message to json
    json_message = json.loads(message)
    # pprint.pprint(json_message)

    # define variables from json message
    symbol = json_message['s']
    time = json_message['E']
    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']
    high = candle['h']
    low = candle['l']
    open = candle['o']
    volume = candle['v']

    print(f"# {symbol} {time} {is_candle_closed} ${float(close)}")

    # if the candle is closed, append the close to the closes list
    if is_candle_closed:
        print("-" * 20)
        print(f"$ CLOSE at: ${float(close)}")
        closes.append(float(close))
        print(f"closes: {closes}")

        # if the closes list is greater than the rsi period, calculate the rsi
        if len(closes) > RSI_PERIOD:
            # convert closes to numpy array
            np_closes = numpy.array(closes)

            # calculate the rsi
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print(f"rsi:\n{rsi}")

            last_rsi = rsi[-1]
            print(f"latest rsi: {last_rsi}")

            # if the latest rsi is greater than the overbought threshold, sell if in position
            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print(f"rsi: {last_rsi} > {RSI_OVERBOUGHT}")
                    print("--- overbought ---")
                    print("--- SELL ! ---")
                    # @TODO: add binance logic to sell
                    # order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    # if order_succeeded:
                    #     in_position = False

                else:
                    print(f"rsi: {last_rsi} > {RSI_OVERBOUGHT}")
                    print("--- overbought ---")
                    print("--- no position ---")

            # if the latest rsi is greater than the oversold threshold, buy if not in position
            if last_rsi > RSI_OVERSOLD:
                if in_position:
                    print(f"rsi: {last_rsi} > {RSI_OVERSOLD}")
                    print("--- oversold ---")
                    print("--- IN POSITION ! ---")
                else:
                    print(f"rsi: {last_rsi} > {RSI_OVERSOLD}")
                    print("--- oversold ---")
                    print("--- BUY ! ---")
                    # @TODO: add binance logic to buy
                    # order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    # if order_succeeded:
                    #     in_position = True
        print("-" * 20)

# @FUNCTION:
#   on_error
# @DESCRIPTION:
#   run on websocket error
# @PARAMS:
#   ws: websocket
#   error: string
def on_error(ws, error):
    print(error)


# @FUNCTION:
#   main
# @DESCRIPTION:
#   open websocket connection and run forever
def main():
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

# 
if __name__ == "__main__":
    main()