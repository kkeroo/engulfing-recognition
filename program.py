import yfinance as yf
import csv
import pandas

def ticker_history_data (symbol, period, interval):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period, interval=interval)
    return hist[-2:]


def is_bullish_candlestick(candle):
    return candle["Close"] > candle["Open"]

def is_bearish_candlestick(candle):
    return candle["Close"] < candle["Open"]

def is_engulfing_bullish (current_candle, previous_candle):
    if is_bearish_candlestick(previous_candle) and is_bullish_candlestick(current_candle):
        # If previous candle was red and current is green
        if current_candle["Close"] > previous_candle["Open"] and current_candle["Open"] < previous_candle["Close"]:
            return True
    return False

tickers = []

with open("sp500_tickers.csv", "r") as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        tickers.append(row[0])

for ticker in tickers:
    ticker_hist = ticker_history_data(ticker, "1d", "1h")
    #print(len(ticker_hist))
    #print (ticker_hist.iloc[0]["Open"])
    #print(ticker_hist.iloc[1])

    if len(ticker_hist) > 1:
        current_candle = ticker_hist.iloc[1]
        previous_candle = ticker_hist.iloc[0]

        if is_engulfing_bullish(current_candle, previous_candle):
            print ("Stock {} is engulfing bullish".format(ticker))