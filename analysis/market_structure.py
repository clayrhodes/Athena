def analyze_market_structure(market):

    score = 50
    reasons = []

    price = market["price"]
    sma20 = market["sma20"]
    sma50 = market["sma50"]
    sma200 = market["sma200"]

    if price > sma20 and sma20 > sma50 and sma50 > sma200:
        score += 40
        reasons.append("Market structure is fully bullish")

    elif price < sma20 and sma20 < sma50 and sma50 < sma200:
        score -= 40
        reasons.append("Market structure is fully bearish")

    else:
        reasons.append("Market structure is mixed")

    score = max(0, min(100, score))

    return {
        "score": score,
        "reasons": reasons
    }