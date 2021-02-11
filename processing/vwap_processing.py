


def typical_price_times_volume(last_candlestick):
    typicalprice = (last_candlestick['close'] + last_candlestick['high'] +
                    last_candlestick['low']) / 3
    return typicalprice * last_candlestick['volume']



def process_vwap(candlesticks, typical_price_times_volume, VWAP_INDICATOR_LOOKBACK ):
    if (len(typical_price_times_volume) >= VWAP_INDICATOR_LOOKBACK):
        relevant_candlesticks = candlesticks[-VWAP_INDICATOR_LOOKBACK:]
        relevant_typical_price_times_volume = typical_price_times_volume[-VWAP_INDICATOR_LOOKBACK:]
        volumes = [candlestick['volume'] for candlestick in relevant_candlesticks]

        vwap = sum(relevant_typical_price_times_volume)/ sum(volumes)

        return vwap

