from datetime import datetime, timedelta
import yfinance as yf
from dateutil.parser import parse
import logging


def calculate_performance(symbol, days_ago):
    ticker = yf.Ticker(symbol)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_ago)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    historical_data = ticker.history(start=start_date, end=end_date)
    old_price = historical_data["Close"].iloc[0]
    new_price = historical_data["Close"].iloc[-1]
    percent_change = ((new_price - old_price) / old_price) * 100
    return round(percent_change, 2)


def get_best_performing(stocks, days_ago):
    best_stock = None
    best_performance = None
    for stock in stocks:
        try:
            performance = calculate_performance(stock, days_ago)
            if best_performance is None or performance > best_performance:
                best_stock = stock
                best_performance = performance
        except Exception as e:
            print(f"Could not calculate performance for {stock}: {e}")
    return best_stock, best_performance


def get_stock_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period="1d")
    return round(todays_data["Close"][0], 2)


def get_date_stock_price(symbol, date=None):
    ticker = yf.Ticker(symbol)
    if date:
        try:
            start_date = parse(date)
            end_date = start_date + timedelta(days=1)
            t_data = ticker.history(start=str(start_date.date()), end=str(end_date.date()))
        except Exception:
            logging.exception("Exception on date stock price")
            return "Not found"
    else:
        t_data = ticker.history(period="1d")

    return round(t_data["Close"].iloc[0], 2)


def get_price_change_percent(symbol, days_ago):
    ticker = yf.Ticker(symbol)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_ago)

    # Convert dates to string format that yfinance can accept
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    historical_data = ticker.history(start=start_date, end=end_date)

    # Get the closing price N days ago and today's closing price
    old_price = historical_data["Close"].iloc[0]
    new_price = historical_data["Close"].iloc[-1]

    percent_change = ((new_price - old_price) / old_price) * 100

    return round(percent_change, 2)
