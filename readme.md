# AutoTrader

A simple python program which makes autonomous trades based on several candlestick metrics.
It currently utilizes the Binance API to fetch crypto currency information and decide on whether to buy or sell based on the strategy employed.


## Requirements
```bash
pip install -r requirements.txt
```
## Getting started
In the current version, run: `python gui/dashboard.py`

##Usage

Browse to localhost:8050

Specify the crypto currency by its abbreviation.
Specify the time frame (Ex: 5m, 10m, 1h, ...)

For backrading: Press the `INITIALIZE DATA` button and then choose the number of candlesticks to process in the top input box then `SUBMIT`.

For live trading: Specify the number of previous candlesticks to load (From this time point) and press `START LIVE TRADING`

##TODOs

* Convert GUI from dashboard/plotly to tkinterg
* Seperate binance code to standalone module
* Make it easy to support other brokers
* Make it easy to setup a strategy