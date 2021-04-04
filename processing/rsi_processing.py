
def process_rsi(candlesticks, RSI_INDICATOR_LOOKBACK, previous_gain = None, previous_loss = None):
    closes = [candlestick['close'] for candlestick in candlesticks]
    changes = []
    if (len(closes) > RSI_INDICATOR_LOOKBACK):

        if(not previous_gain):

            for i in range(-RSI_INDICATOR_LOOKBACK-1,-1):
                change = closes[i+1]-closes[i]
                changes.append(change)

            gains = []
            losses = []
            for change in changes:
                if(change>=0):
                    gains.append(change)
                else:
                    losses.append(-change)

            avg_gain = sum(gains)/RSI_INDICATOR_LOOKBACK
            avg_loss = sum(losses)/RSI_INDICATOR_LOOKBACK
            rs = avg_gain/avg_loss
            rsi = 100 - (100/(1+rs))
            return avg_gain,avg_loss,rsi
        else:
            last_change = closes[-1] - closes[-2]
            if(last_change<0):
                last_dt = -last_change
                last_ut = 0
            else:
                last_ut = last_change
                last_dt = 0

            avg_gain = (last_ut + (RSI_INDICATOR_LOOKBACK-1)* previous_gain)/RSI_INDICATOR_LOOKBACK
            avg_loss = (last_dt + (RSI_INDICATOR_LOOKBACK - 1) * previous_loss) / RSI_INDICATOR_LOOKBACK
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return avg_gain,avg_loss,rsi



    return (None,None,None)