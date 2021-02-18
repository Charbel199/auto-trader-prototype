import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly
from processing import local_extremas
import numpy as np
from datetime import datetime
import math
def plot_candlesticks(candlesticks, macd_indicator, ema_values_3, vwap_indicator, buy_orders, sell_orders, local_min = None, local_max = None):
    fig = make_subplots(rows=2, cols=1)

    dates = [candlestick['open_time'] for candlestick in candlesticks]
    closes = [candlestick['close'] for candlestick in candlesticks]
    opens = [candlestick['open'] for candlestick in candlesticks]
    highs = [candlestick['high'] for candlestick in candlesticks]
    lows = [candlestick['low'] for candlestick in candlesticks]

    if(macd_indicator):
        macd_dates = list(macd_indicator)
        macd_values = list(macd_indicator.values())
        fig.append_trace(go.Scatter(x=macd_dates, y=macd_values, name="MACD"), row=2, col=1)

    if(ema_values_3):
        ema_dates = list(ema_values_3)
        ema_values = list(ema_values_3.values())
        fig.append_trace(go.Scatter(x=ema_dates, y=ema_values, name="Signal"), row=2, col=1)

    if(vwap_indicator):
        vwap_dates = list(vwap_indicator)
        vwap_values = list(vwap_indicator.values())
        fig.append_trace(go.Scatter(x=vwap_dates, y=vwap_values, line=dict(color="cyan"), name="VWAP"), row=1, col=1)

    if(buy_orders):
        buy_dates = list(buy_orders)
        buy_values = []
        for buy_date in buy_dates:
            buy_values.append(closes[dates.index(buy_date)])
        fig.append_trace(go.Scatter(
            x=buy_dates,
            y=buy_values,
            marker=dict(color="gold", size=13, symbol=46),
            mode="markers",
            name="Buy"
        ), row=1, col=1)
    if(sell_orders):
        sell_dates = list(sell_orders)
        sell_values = []
        for sell_date in sell_dates:
            sell_values.append(closes[dates.index(sell_date)])
        fig.append_trace(go.Scatter(
            x=sell_dates,
            y=sell_values,
            marker=dict(color="silver", size=13, symbol=45),
            mode="markers",
            name="Sell"
        ), row=1, col=1)



    fig.append_trace(go.Candlestick(x=dates,
                                         open=opens, high=highs,
                                         low=lows, close=closes,name="Candlesticks"),row=1,col=1)

    projection = 600

    if(local_min):
        min_dates = list(local_min)
        min_values = list(local_min.values())

        fig.append_trace(go.Scatter(
            x=min_dates,
            y=min_values,
            marker=dict(color="red", size=13, symbol=23),
            mode="markers",
            name="Min"
        ), row=1, col=1)

        if (len(min_values) >= 2):
            date1 = min_dates[-2]
            date2 = min_dates[-1]
            coefficients = local_extremas.get_support_line_equation(local_min)
            projected_date = date2 + projection
            x_values = [date1, projected_date]
            y_values = local_extremas.predict_values_from_line_equation(coefficients, x_values)
            fig.add_shape(type="line",
                          x0=x_values[0], y0=y_values[0], x1=x_values[1], y1=y_values[1],
                          line=dict(
                              color="MediumPurple",
                              width=3,
                              dash="dot",

                          ), row=1, col=1
                          )
    if(local_max):
        max_dates = list(local_max)
        max_values = list(local_max.values())
        fig.append_trace(go.Scatter(
            x=max_dates,
            y=max_values,
            marker=dict(color="blue", size=13, symbol=23),
            mode="markers",
            name="Max"
        ), row=1, col=1)

        if (len(max_values) >= 2):
            date1 = max_dates[-2]
            date2 = max_dates[-1]
            coefficients = local_extremas.get_resistance_line_equation(local_max)
            projected_date = date2 + projection
            x_values = [date1, projected_date]
            y_values = local_extremas.predict_values_from_line_equation(coefficients, x_values)
            fig.add_shape(type="line",
                          x0=x_values[0], y0=y_values[0], x1=x_values[1], y1=y_values[1],
                          line=dict(
                              color="MediumPurple",
                              width=3,
                              dash="dot",

                          ), row=1, col=1
                          )











    fig.update_xaxes(matches = 'x')

    fig.update_layout(xaxis_rangeslider_visible=False, height=1600, width=1800)
    fig.update_layout(legend=dict(font=dict(family="Courier", size=20, color="black")),
                      legend_title=dict(font=dict(family="Courier", size=15, color="blue")))
    return fig
    plotly.offline.plot(fig)
