import websocket, json
import argparse
from liveStrategies.firstStrategy import testStrategy



###Arg parsing

def parse_args():
    global crypto
    global timeframe
    crypto = "ltc"
    timeframe = "1m"
    parser = argparse.ArgumentParser(description='Live trading bot')
    parser.add_argument('-c', '--crypto', help='Set crypto currency', required=False)
    parser.add_argument('-tf', '--timeframe', help='Set time frame', required=False)
    args = vars(parser.parse_args())
    if args['crypto']:
        crypto = args['crypto']
    if args['timeframe']:
        timeframe = args['timeframe']


###End of arg parsing


def on_open(ws):
    print("Opening connection ...")
    currency = crypto+"usdt"
    print('Currency: ',currency,'\t Time frame: ',timeframe)
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params": [
            currency+"@kline_"+timeframe
        ],
        "id": 1
    }
    print('Starting to receive messages: ')
    ws.send(json.dumps(subscribe_message))



def on_message(ws, message):
    message = json.loads(message)
    strategy.add_message(message)
    #strategy.end()


def on_error(ws, error):
    print('Error ',error)

def on_close(ws):
    print('Closed')

def run_socket():
    socket = "wss://stream.binance.com:9443/ws/kline_"+timeframe
    print('Connecting ... ')
    print('Socket'+ socket)
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

def main():
    global strategy
    strategy = testStrategy(timeframe=timeframe, crypto=crypto)
    strategy.get_previous_data(timeperiod=100)
    run_socket()

if __name__=="__main__":
    parse_args()
    main()


