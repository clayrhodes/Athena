def analyze_trend(market):
    """
    Athena Trend Engine V2

    Evaluates:
    - Price vs moving averages
    - Moving average alignment
    - Trend direction
    - Trend strength
    """

    score = 0
    evidence = []

    price = market.get("price", 0)
    sma20 = market.get("sma20", 0)
    sma50 = market.get("sma50", 0)
    sma200 = market.get("sma200", 0)

    # Price vs Moving Averages
    if price > sma20:
        score += 15
        evidence.append("Price is above the 20 SMA.")
    else:
        evidence.append("Price is below the 20 SMA.")

    if price > sma50:
        score += 20
        evidence.append("Price is above the 50 SMA.")
    else:
        evidence.append("Price is below the 50 SMA.")

    if price > sma200:
        score += 30
        evidence.append("Price is above the 200 SMA.")
    else:
        evidence.append("Price is below the 200 SMA.")

    # Moving Average Alignment
    if sma20 > sma50:
        score += 15
        evidence.append("20 SMA is above the 50 SMA.")
    else:
        evidence.append("20 SMA is below the 50 SMA.")

    if sma50 > sma200:
        score += 20
        evidence.append("50 SMA is above the 200 SMA.")
    else:
        evidence.append("50 SMA is below the 200 SMA.")

    score = max(0, min(100, score))

    # Determine trend direction and strength
    if score >= 85:
        direction = "Bullish"
        strength = "Very Strong"
    elif score >= 70:
        direction = "Bullish"
        strength = "Strong"
    elif score >= 55:
        direction = "Bullish"
        strength = "Moderate"
    elif score >= 45:
        direction = "Neutral"
        strength = "Mixed"
    elif score >= 30:
        direction = "Bearish"
        strength = "Moderate"
    else:
        direction = "Bearish"
        strength = "Strong"

    summary = (
        f"{strength} {direction.lower()} trend. "
        f"Trend score: {score}/100."
    )

    return {
        "score": score,
        "direction": direction,
        "strength": strength,
        "summary": summary,
        "evidence": evidence,
    }