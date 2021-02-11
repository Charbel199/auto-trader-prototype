


def get_ema_value(period, multiplier, ema_list, reference_list):
    if (len(reference_list) >= period):
        ##First item in the list
        if (len(ema_list) == 0):
            average = sum(reference_list[-period:]) / period
            return average
        else:
            recent_value = reference_list[-1]
            spread = recent_value - ema_list[list(ema_list)[-1]]
            ema_value = spread * multiplier + ema_list[list(ema_list)[-1]]
            return ema_value

##Maybe make it more general, not only for dictionaries
def get_macd_value(ema_values_1,ema_values_2):
    ###Considering ema_period_2 is bigger than the first
    if (len(ema_values_2) != 0):
        macd_value = ema_values_1[list(ema_values_1)[-1]] - ema_values_2[list(ema_values_2)[-1]]
        return macd_value

