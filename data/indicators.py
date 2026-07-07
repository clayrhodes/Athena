def calculate_rsi(close, period=14):
    delta = close.diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return float(rsi.iloc[-1])


def calculate_macd(close):
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()

    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal

    return {
        "macd": float(macd.iloc[-1]),
        "signal": float(signal.iloc[-1]),
        "histogram": float(histogram.iloc[-1])
    }


def calculate_atr(data, period=14):
    high = data["High"]
    low = data["Low"]
    close = data["Close"]

    if hasattr(high, "columns"):
        high = high.iloc[:, 0]
    if hasattr(low, "columns"):
        low = low.iloc[:, 0]
    if hasattr(close, "columns"):
        close = close.iloc[:, 0]

    previous_close = close.shift(1)

    tr1 = high - low
    tr2 = (high - previous_close).abs()
    tr3 = (low - previous_close).abs()

    true_range = tr1.combine(tr2, max).combine(tr3, max)
    atr = true_range.rolling(period).mean()

    return float(atr.iloc[-1])