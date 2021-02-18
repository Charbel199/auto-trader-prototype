import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import csv
import argparse
from liveStrategies.firstStrategy import TestStrategy
import websocket, json
import plotly.graph_objs as go


app = dash.Dash()
app.layout = html.Div(children=[
        dcc.Input(id='input', value='', type='text'),
        html.Button('Submit', id='button'),
        html.Div(id='my-div'),
        html.Div(id='graphs', children=dcc.Graph(id="live-graph")),
        dcc.Interval(
            id='graph-update',
            interval=2000
        )
    ])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='button', component_property='n_clicks')],
    state=[State(component_id='input',component_property='value')]
)
def update_value(n_clicks, input_val):

    print('Clicked with {}'.format(input_val))

    if (input_val == 'test'):
        print('TEST')
        return 'test'
    if (input_val == 'stop'):
        print('Stopping scoket')
        ws.close()
        return 'stopped socket'
    if (input_val == 'run'):
        print('Going to run socket')
        run_socket()
        return 'Running socket'

    if(input_val == ''):
        return 'Input was nothing'
    ##Print to txt
    if (input_val == "print"):
        strategy.log_to_txt(output_file_name)
        return 'Printing'
    ##If all data has been processed already
    if (idx >= len(candlesticks)):
        print('All data was processed')
        return 'All data was processed'

    ##Go through all the data
    if (input_val == "all"):
        for i in range(len(candlesticks)):
            message = candlesticks[idx]
            strategy.add_tick(message)
            idx += 1
            if (idx >= len(candlesticks)):
                print('All data was processed')
                break
        return 'All data being processed'

    ##Number of messages to process
    if (input_val.isnumeric()):
        for i in range(int(input_val)):
            message = candlesticks[idx]
            strategy.add_tick(message)
            idx += 1
            if (idx >= len(candlesticks)):
                print('All data was processed')
                break
        return 'Hey'



@app.callback(
    Output(component_id='live-graph', component_property='figure'),
    [Input(component_id='graph-update', component_property='n_intervals')]
)
def update_graph(inpu_data):
    return strategy.plot()


def initialize_data():
    print('Initializing candlesticks')
    global candlesticks
    candlesticks = []
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
           # print(row)
            candlesticks.append({
                "E": float(row[0]),
                "k": {
                    "o": row[1],
                    "h": row[2],
                    "l": row[3],
                    "c": row[4],
                    "v": row[5],
                    "T": row[6],
                    "t": row[0]
                }
            })

def parse_args():
    global crypto
    global timeframe
    global file_name
    global output_file_name

    crypto = "ltc"
    timeframe = "1m"
    file_name = "data/ltc1m.csv"
    output_file_name = "output_of_test_live_trader.txt"
    parser = argparse.ArgumentParser(description='Live trading bot')
    parser.add_argument('-c', '--crypto', help='Set crypto currency', required=False)
    parser.add_argument('-tf', '--timeframe', help='Set time frame', required=False)
    parser.add_argument('-f', '--file', help='File name', required=False)
    parser.add_argument('-o', '--output', help='Output txt file', required=False)
    args = vars(parser.parse_args())
    if args['crypto']:
        crypto = args['crypto']
    if args['timeframe']:
        timeframe = args['timeframe']
    if args['file']:
        file_name = args['file']
    if args['output']:
        output_file_name = args['output']



###LIVE TRADER
def on_open(ws):
    print("Opening connection ...")
    crypto_usdt = crypto+"usdt"
    print('Currency: ',crypto_usdt,'\t Time frame: ',timeframe)
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params": [
            crypto_usdt+"@kline_"+timeframe
        ],
        "id": 1
    }
    print('Starting to receive messages: ')
    ws.send(json.dumps(subscribe_message))
def on_message(ws, message):
    message = json.loads(message)
    strategy.add_tick(message)
    strategy.log_to_txt(output_file_name)


    #strategy.end()


def on_error(ws, error):
    print('Error ',error)

def on_close(ws):
    print('Closed')

def run_socket():

    socket = "wss://stream.binance.com:9443/ws/kline_"+timeframe
    print('Connecting ... ')
    print('Socket'+ socket)
    global ws
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()



if __name__ == '__main__':
    print('Launching dashboard')
    parse_args()
    if(False):
        print('Backtesting')

        global strategy
        global idx
        idx = 0
        initialize_data()

    strategy = TestStrategy(timeframe=timeframe, crypto=crypto)

    if(True):
        strategy.get_previous_data(old_data_time_period=2)




    app.run_server(debug=True)


'''
1- Backtesting or Live (Option to stop both)
2- Delete all data button and delete all data when starting new backtesting or live
3- Get prev data on running socket
4- Change parameters for run

'''