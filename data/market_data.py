from data.indicators import calculate_sma
import yfinance as yf


def get_market_snapshot(symbol):

    ticker = yf.Ticker(symbol)

    # Download the last 90 trading days
    data = ticker.history(period="90d")

    previous_price = data["Close"].iloc[-2]
    latest_price = data["Close"].iloc[-1]

    sma20 = calculate_sma(data, 20)
    sma50 = calculate_sma(data, 50)

    return {
        "symbol": symbol,
        "price": round(latest_price, 2),
        "trend": "Up" if latest_price > previous_price else "Down",
        "sma20": round(sma20, 2),
        "sma50": round(sma50, 2),
        "source": "Yahoo Finance"
    }