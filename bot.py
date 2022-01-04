import websocket, json, pprint

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

closes = []

def on_open(ws):
    print("--- opened connection ---")

def on_close(ws, close_status_code, close_msg):
    print("-- closing --")
    print(f"close status code: {close_status_code}")
    print(f"close message: {close_msg}")
    print("--- closed connection ---")

def on_message(ws, message):
    global closes
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
        print("-" * 20)

def on_error(ws, error):
    print(error)


if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()