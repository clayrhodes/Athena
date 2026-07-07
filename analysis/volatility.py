def analyze_volatility(market):

    score = 50
    reasons = []

    price = market["price"]
    atr = market["atr"]

    atr_percent = (atr / price) * 100

    if atr_percent > 2:
        score -= 25
        reasons.append("ATR is high compared to price")

    elif atr_percent > 1:
        score += 10
        reasons.append("ATR is normal / tradable")

    else:
        score += 20
        reasons.append("ATR is low and controlled")

    score = max(0, min(100, score))

    return {
        "score": score,
        "atr_percent": atr_percent,
        "reasons": reasons
    }