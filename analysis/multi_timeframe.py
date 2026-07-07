import yfinance as yf


def calculate_bias(close):

    sma20 = close.rolling(20).mean().iloc[-1]
    sma50 = close.rolling(50).mean().iloc[-1]

    price = close.iloc[-1]

    if price > sma20 and sma20 > sma50:
        return "Bullish", 100

    elif price < sma20 and sma20 < sma50:
        return "Bearish", 0

    elif price > sma20:
        return "Neutral Bullish", 75

    elif price < sma20:
        return "Neutral Bearish", 25

    return "Neutral", 50


def analyze_multi_timeframe():

    timeframes = {
        "1 Hour": ("60d", "1h"),
        "Daily": ("1y", "1d"),
        "Weekly": ("5y", "1wk"),
    }

    results = {}

    for name, (period, interval) in timeframes.items():

        data = yf.download(
            "SPY",
            period=period,
            interval=interval,
            auto_adjust=True,
            progress=False
        )

        close = data["Close"]

        if hasattr(close, "columns"):
            close = close.iloc[:, 0]

        bias, score = calculate_bias(close)

        results[name] = {
            "bias": bias,
            "score": score
        }

    return results