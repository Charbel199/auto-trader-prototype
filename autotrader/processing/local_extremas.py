import numpy as np
from scipy.signal import argrelextrema


def local_extrema_values(candlesticks, order=20):
    closes = [candlestick['close'] for candlestick in candlesticks]
    times = [candlestick['open_time'] for candlestick in candlesticks]
    closes = np.array(closes)
    max_values = argrelextrema(closes, np.greater, order=order)
    min_values = argrelextrema(closes, np.less, order=order)
    max_values = max_values[0].tolist()
    min_values = min_values[0].tolist()
    local_min_values = {}
    local_max_values = {}
    multiplier = 0
    for min in min_values:
        local_min_values[times[min]] = closes[min] * (1 - multiplier)
    for max in max_values:
        local_max_values[times[max]] = closes[max] * (1 + multiplier)
    return (local_min_values, local_max_values)


def get_line_equation(x_values, y_values):
    coefficients = np.polyfit(x_values, y_values, 1)
    return coefficients


def get_support_line_equation(local_min_values):
    min_dates = list(local_min_values)
    min_values = list(local_min_values.values())
    coefficients = get_line_equation([min_dates[-2], min_dates[-1]], [min_values[-2], min_values[-1]])
    return coefficients


def get_resistance_line_equation(local_max_values):
    max_dates = list(local_max_values)
    max_values = list(local_max_values.values())
    coefficients = get_line_equation([max_dates[-2], max_dates[-1]], [max_values[-2], max_values[-1]])
    return coefficients


def predict_values_from_line_equation(coefficients, x_values):
    polynomial = np.poly1d(coefficients)
    y_values = polynomial(x_values)
    return y_values
