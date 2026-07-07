import pandas as pd


def calculate_vwap(data):

    high = data["High"]
    low = data["Low"]
    close = data["Close"]
    volume = data["Volume"]

    # Handle yfinance DataFrame columns
    if hasattr(high, "columns"):
        high = high.iloc[:, 0]

    if hasattr(low, "columns"):
        low = low.iloc[:, 0]

    if hasattr(close, "columns"):
        close = close.iloc[:, 0]

    if hasattr(volume, "columns"):
        volume = volume.iloc[:, 0]

    typical_price = (high + low + close) / 3

    cumulative_price_volume = (typical_price * volume).cumsum()
    cumulative_volume = volume.cumsum()

    vwap = cumulative_price_volume / cumulative_volume

    current_price = float(close.iloc[-1])
    current_vwap = float(vwap.iloc[-1])

    if current_price > current_vwap:
        bias = "Above VWAP"
        score = 100
    elif current_price < current_vwap:
        bias = "Below VWAP"
        score = 0
    else:
        bias = "At VWAP"
        score = 50

    return {
        "vwap": round(current_vwap, 2),
        "price": round(current_price, 2),
        "bias": bias,
        "score": score,
        "distance": round(current_price - current_vwap, 2)
    }