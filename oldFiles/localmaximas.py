import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt

def localextrema(candlesticks):
    arr = [candlestick['close'] for candlestick in candlesticks]
    times = [candlestick['open_time'] for candlestick in candlesticks]
    arr = np.array(arr)
    maxm = argrelextrema(arr, np.greater,order=20)  # (array([1, 3, 6]),)
    minm = argrelextrema(arr, np.less,order=20)  # (array([2, 5, 7]),)
    maxm = maxm[0].tolist()
    minm = minm[0].tolist()
    localmins = []
    localmaxs = []
    for min in minm:
        localmins.append(times[min])
    for max in maxm:
        localmaxs.append(times[max])
    return (localmins,localmaxs)