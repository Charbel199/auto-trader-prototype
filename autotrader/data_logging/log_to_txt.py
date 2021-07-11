from datetime import datetime

def print_to_txt(txt_file, candlesticks, vwap_indicator, macd_indicator,ema_values_3, buy_orders, sell_orders, balance_history):
    with open(txt_file, "w") as txt_file:
        for line in candlesticks:
            txt_file.write(datetime.utcfromtimestamp(line["open_time"]).strftime('%Y-%m-%d %H:%M'))
            txt_file.write("\t")
            txt_file.write("Close: ")
            txt_file.write("{:.2f}".format(line["close"]))
            txt_file.write("\t")
            txt_file.write("Open: ")
            txt_file.write("{:.2f}".format(line["open"]))
            txt_file.write("\t")
            txt_file.write("Low: ")
            txt_file.write("{:.2f}".format(line["low"]))
            txt_file.write("\t")
            txt_file.write("High: ")
            txt_file.write("{:.2f}".format(line["high"]))
            txt_file.write("\t")
            if (vwap_indicator.get(line['open_time'])):
                txt_file.write("{:.2f}".format(vwap_indicator.get(line['open_time'])))
            else:
                txt_file.write("No data")
            txt_file.write("\t")
            if (macd_indicator.get(line['open_time'])):
                txt_file.write("{:.2f}".format(macd_indicator.get(line['open_time'])))
            else:
                txt_file.write("No data")
            txt_file.write("\t")
            if (ema_values_3.get(line['open_time'])):
                txt_file.write("{:.2f}".format(ema_values_3.get(line['open_time'])))
            else:
                txt_file.write("No data")
            txt_file.write("\t")
            txt_file.write("\t")
            if (buy_orders.get(line['time'])):
                txt_file.write("{:.2f}".format(buy_orders.get(line['time'])))
            else:
                txt_file.write("No Buy")
            txt_file.write("\t")
            txt_file.write("\t")
            if (sell_orders.get(line['time'])):
                txt_file.write("{:.2f}".format(sell_orders.get(line['time'])))
            else:
                txt_file.write("No Sell")
            txt_file.write("\t")
            txt_file.write("\t")
            if (balance_history.get(line['time'])):
                txt_file.write("{:.2f}".format(balance_history.get(line['time'])))
            else:
                txt_file.write("0")
            txt_file.write("\n")