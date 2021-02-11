import csv
import argparse
from liveStrategies.firstStrategy import TestStrategy



###Arg parsing

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
###Initializing data

def initialize_data():
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

###Run test

def run_test():
    idx = 0
    while True:
        input_val = input("Enter command: ")
        input_val = input_val.lower()

        ##If all data has been processed already
        if(idx > len(candlesticks)):
            print('All data was processed')
            continue

        ##Plot
        if(input_val == "plot"):
            strategy.plot()
            continue

        ##Stop
        if(input_val == "s" or input_val == "stop"):
            print('Done')
            break

        ##Print to txt
        if(input_val =="print"):
            strategy.log_to_txt(output_file_name)
            continue

        ##Go through all the data
        if(input_val == "all"):
            for i in range(len(candlesticks)):
                message = candlesticks[idx]
                strategy.add_tick(message)
                idx += 1
            continue

        ##Number of messages to process
        if (input_val.isnumeric()):
            for i in range(int(input_val)):
                message = candlesticks[idx]
                strategy.add_tick(message)
                idx += 1
            continue

        ##For any other input, just process one message
        message = candlesticks[idx]
        strategy.add_tick(message)
        idx +=1







def main():
    global strategy
    strategy = TestStrategy(timeframe=timeframe, crypto=crypto)
    ##Initialize data from specified file
    initialize_data()
    run_test()

if __name__=="__main__":
    parse_args()
    main()