def analyze_price_action(market):

    price = market["price"]
    sma20 = market["sma20"]
    sma50 = market["sma50"]
    vwap = market["vwap"]["vwap"]
    rsi = market["rsi"]
    macd = market["macd"]

    patterns = []
    warnings = []
    score = 50

    if price > sma20 and sma20 > sma50:
        patterns.append("Bullish trend structure")
        score += 20

    if price > vwap:
        patterns.append("Price is holding above VWAP")
        score += 15
    else:
        warnings.append("Price is below VWAP")
        score -= 15

    if rsi > 55:
        patterns.append("RSI supports bullish momentum")
        score += 10
    elif rsi < 45:
        warnings.append("RSI shows weak momentum")
        score -= 10

    if macd["histogram"] > 0:
        patterns.append("MACD momentum is positive")
        score += 10
    else:
        warnings.append("MACD momentum is negative")
        score -= 10

    if price > sma20 and price > vwap and macd["histogram"] < 0:
        patterns.append("Possible bullish pullback setup")
        warnings.append("Momentum has not confirmed yet")

    score = max(0, min(100, score))

    if score >= 80:
        pattern_quality = "Strong"
    elif score >= 65:
        pattern_quality = "Good"
    elif score >= 50:
        pattern_quality = "Mixed"
    else:
        pattern_quality = "Weak"

    return {
        "score": score,
        "quality": pattern_quality,
        "patterns": patterns,
        "warnings": warnings
    }