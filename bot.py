import websocket, json, pprint, talib, numpy

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "ETHUSD"
TRADE_QUANTITY = 0.001

closes = []
in_position = False

def on_open(ws):
    print("--- opened connection ---")

def on_close(ws, close_status_code, close_msg):
    print("-- closing --")
    print(f"close status code: {close_status_code}")
    print(f"close message: {close_msg}")
    print("--- closed connection ---")

def on_message(ws, message):
    global closes, in_position
    print("- received message -")
    json_message = json.loads(message)
    # pprint.pprint(json_message)

    candle = json_message['k']
    symbol = json_message['s']
    time = json_message['E']

    is_candle_closed = candle['x']
    close = candle['c']

    print(f"# {symbol} {time} {is_candle_closed} ${float(close)}")

    if is_candle_closed:
        print("-" * 20)
        print(f"$ CLOSE at: ${float(close)}")
        closes.append(float(close))
        print(f"closes: {closes}")

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)

            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print(f"rsi:\n{rsi}")

            last_rsi = rsi[-1]
            print(f"latest rsi: {last_rsi}")

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print(f"rsi: {last_rsi} > {RSI_OVERBOUGHT}")
                    print("--- overbought ---")
                    print("--- SELL ! ---")
                    # @TODO: add binance logic to sell
                else:
                    print(f"rsi: {last_rsi} > {RSI_OVERBOUGHT}")
                    print("--- overbought ---")
                    print("--- no position ---")

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



        print("-" * 20)

def on_error(ws, error):
    print(error)


if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()