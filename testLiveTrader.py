import csv
import argparse
from liveStrategies.firstStrategy import testStrategy



###Arg parsing

def parse_args():
    global crypto
    global timeframe
    crypto = "ltc"
    timeframe = "1m"
    parser = argparse.ArgumentParser(description='Live trading bot')
    parser.add_argument('-c', '--crypto', help='Set crypto currency', required=False)
    parser.add_argument('-tf', '--timeframe', help='Set time frame', required=False)
    args = vars(parser.parse_args())
    if args['crypto']:
        crypto = args['crypto']
    if args['timeframe']:
        timeframe = args['timeframe']


def initialize_data():
    global candlesticks
    candlesticks = []

    with open('data/ltc1m.csv', 'r') as f:
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
                    "v": row[5]
                }
            })


def run_test():
    idx = 0
    while True:
        inputval = input("Enter something: ")
        if(inputval == "s"):
            print('Done')
            break
        if(inputval =="print"):
            strategy.print_to_txt("output_of_test_live_trader.txt")
            continue
        if (inputval.isnumeric()):
            for i in range(int(inputval)):
                message = candlesticks[idx]
                strategy.add_message(message)
                idx += 1
            continue

        message = candlesticks[idx]
        strategy.add_message(message)
        idx +=1

def main():
    global strategy
    strategy = testStrategy(timeframe=timeframe)
    initialize_data()
    run_test()

if __name__=="__main__":
    parse_args()
    main()