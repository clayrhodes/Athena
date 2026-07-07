def analyze_momentum(market):

    score = 50
    reasons = []

    rsi = market["rsi"]
    macd = market["macd"]

    if rsi > 70:
        score -= 20
        reasons.append("RSI is overbought")

    elif rsi > 55:
        score += 25
        reasons.append("RSI shows bullish momentum")

    elif rsi < 30:
        score -= 10
        reasons.append("RSI is very weak / oversold")

    elif rsi < 45:
        score -= 25
        reasons.append("RSI shows bearish momentum")

    else:
        reasons.append("RSI is neutral")

    if macd["histogram"] > 0:
        score += 25
        reasons.append("MACD histogram is positive")

    else:
        score -= 25
        reasons.append("MACD histogram is negative")

    score = max(0, min(100, score))

    return {
        "score": score,
        "reasons": reasons
    }