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
    print("-- received message --")
    json_message = json.loads(message)
    pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print(f"close at: {close}")
        closes.append(float(close))
        print(f"closes: {closes}")

def on_error(ws, error):
    print(error)


if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()