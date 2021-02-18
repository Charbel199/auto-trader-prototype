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
app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                     html.Div(className='four columns div-user-controls',
                              children=[
                                  html.H2('AUTO TRADER'),
                                  html.P('Visualising time series with Plotly - Dash.'),
                                  dcc.Input(id='input', value='', type='text'),
                                  html.Button('Submit', id='button'),
                                  html.Div(id='my-div'),
                                  html.Button('Initialize Data', id='initialize-data-button', n_clicks=0),
                                  html.Div(id='initialize-data-output', style={'display': 'none'}),

                                  html.Button('Reset Strategy', id='reset-strategy-button', n_clicks=0),
                                  html.Div(id='reset-strategy-output', style={'display': 'none'}),

                                  dcc.Input(id='start-live-trader-text', value='', type='text'),
                                  html.Button('Start live trading', id='start-live-trader-button', n_clicks=0),
                                  html.Div(id='start-live-trader-output', style={'display': 'none'}),

                                  html.Button('Stop live trading', id='stop-live-trader-button', n_clicks=0),
                                  html.Div(id='stop-live-trader-output', style={'display': 'none'}),

                                  html.Div(id='log-div'),
                                  dcc.Interval(
                                      id='log-update',
                                      interval=2000
                                  )
                              ]
                              ),
                     html.Div(className='eight columns div-for-charts bg-grey',
                              children=[
                                  dcc.Graph(id="live-graph", config={'displayModeBar': True}),
                                  dcc.Interval(
                                      id='graph-update',
                                      interval=2000
                                  )
                              ])
                 ])
    ]

)


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='button', component_property='n_clicks')],
    state=[State(component_id='input', component_property='value')]
)
def update_value(n_clicks, input_val):
    global idx
    print('Clicked with {}'.format(input_val))
    global ws
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

    if (input_val == ''):
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
def update_graph(input_data):
    return strategy.plot()


@app.callback(
    Output(component_id='initialize-data-output', component_property='children'),
    [Input(component_id='initialize-data-button', component_property='n_clicks')]
)
def initialize_data(n_clicks):
    if (n_clicks <= 0):
        return
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


@app.callback(
    Output(component_id='reset-strategy-output', component_property='children'),
    [Input(component_id='reset-strategy-button', component_property='n_clicks')]
)
def reset_strategy(n_clicks):
    if (n_clicks <= 0):
        return
    print('Resetting strategy')
    global strategy
    global idx
    idx = 0

    strategy = TestStrategy(timeframe=timeframe, crypto=crypto)


@app.callback(
    Output(component_id='start-live-trader-output', component_property='children'),
    [Input(component_id='start-live-trader-button', component_property='n_clicks'),
     Input(component_id='start-live-trader-text', component_property='value')]
)
def start_live_trader(n_clicks, input_val):
    if (n_clicks <= 0):
        return
    strategy.get_previous_data(old_data_time_period=int(input_val))
    run_socket()


@app.callback(
    Output(component_id='stop-live-trader-output', component_property='children'),
    [Input(component_id='stop-live-trader-button', component_property='n_clicks')]
)
def start_live_trader(n_clicks):
    if (n_clicks <= 0):
        return
    global ws
    ws.close()

@app.callback(
    Output(component_id='log-div', component_property='children'),
    [Input(component_id='log-update', component_property='n_intervals')]
)
def uodate_logs(input_data):
    global logs
    logs = ['Added 1', 'Processing']
    return logs
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
    crypto_usdt = crypto + "usdt"
    print('Currency: ', crypto_usdt, '\t Time frame: ', timeframe)
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params": [
            crypto_usdt + "@kline_" + timeframe
        ],
        "id": 1
    }
    print('Starting to receive messages...')
    ws.send(json.dumps(subscribe_message))


def on_message(ws, message):
    message = json.loads(message)
    strategy.add_tick(message)
    strategy.log_to_txt(output_file_name)


def on_error(ws, error):
    print('Error ', error)


def on_close(ws):
    print('Closed')


def run_socket():
    socket = "wss://stream.binance.com:9443/ws/kline_" + timeframe
    print('Connecting ... ')
    print('Socket' + socket)
    global ws
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()


if __name__ == '__main__':
    print('Launching dashboard')
    parse_args()
    global idx
    global strategy
    idx = 0

    strategy = TestStrategy(timeframe=timeframe, crypto=crypto)
    app.run_server(debug=True)

'''
1- Backtesting or Live (Option to stop both)
2- Delete all data button and delete all data when starting new backtesting or live
3- Get prev data on running socket
4- Change parameters for run

'''
