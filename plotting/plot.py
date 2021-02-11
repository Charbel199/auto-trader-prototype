import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly

def plot_candlesticks(candlesticks, macd_indicator, ema_values_3):


    dates = [candlestick['open_time'] for candlestick in candlesticks]
    closes = [candlestick['close'] for candlestick in candlesticks]
    opens = [candlestick['open'] for candlestick in candlesticks]
    highs = [candlestick['high'] for candlestick in candlesticks]
    lows = [candlestick['low'] for candlestick in candlesticks]

    macd_dates = list(macd_indicator)
    macd_values = list(macd_indicator.values())


    ema_dates = list(ema_values_3)
    ema_values = list(ema_values_3.values())

    fig = make_subplots(rows=2, cols=1)
    fig.append_trace(go.Candlestick(x=dates,
                                         open=opens, high=highs,
                                         low=lows, close=closes),row=1,col=1)

    fig.append_trace(go.Scatter(x=macd_dates, y=macd_values), row=2, col=1)
    fig.append_trace(go.Scatter(x=ema_dates, y=ema_values), row=2, col=1)
    fig.update_xaxes(matches = 'x')
    fig.update_layout(xaxis_rangeslider_visible=False)
    plotly.offline.plot(fig)
