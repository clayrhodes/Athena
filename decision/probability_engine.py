def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, value))


def normalize_probabilities(probabilities):
    total = sum(probabilities.values())

    if total == 0:
        return probabilities

    return {
        key: round((value / total) * 100)
        for key, value in probabilities.items()
    }


def build_probability_report(scores, forecast):
    trend = scores.get("trend", {}).get("score", 0)
    momentum = scores.get("momentum", {}).get("score", 0)
    volume = scores.get("volume", {}).get("score", 0)
    structure = scores.get("structure", {}).get("score", 0)
    vwap = scores.get("vwap", {}).get("score", 0)
    price_action = scores.get("price_action", {}).get("score", 0)

    mtf = scores.get("multi_timeframe", {})
    weekly = mtf.get("Weekly", {}).get("score", 0)
    daily = mtf.get("Daily", {}).get("score", 0)
    hourly = mtf.get("1 Hour", {}).get("score", 0)

    bull_score = (
        trend * 0.20 +
        structure * 0.18 +
        weekly * 0.18 +
        daily * 0.14 +
        vwap * 0.12 +
        price_action * 0.10 +
        momentum * 0.05 +
        volume * 0.03
    )

    bear_score = (
        (100 - trend) * 0.24 +
        (100 - structure) * 0.20 +
        (100 - weekly) * 0.16 +
        (100 - daily) * 0.12 +
        (100 - vwap) * 0.10 +
        (100 - price_action) * 0.08 +
        (100 - momentum) * 0.06 +
        (100 - volume) * 0.04
    )

    range_score = (
        abs(50 - trend) * -0.20 +
        abs(50 - momentum) * -0.15 +
        abs(50 - structure) * -0.20 +
        abs(50 - vwap) * -0.15 +
        abs(50 - price_action) * -0.15 +
        abs(50 - hourly) * -0.15 +
        100
    )

    reversal_score = (
        (100 - hourly) * 0.25 +
        (100 - momentum) * 0.20 +
        (100 - price_action) * 0.20 +
        (100 - vwap) * 0.15 +
        volume * 0.10 +
        (100 - structure) * 0.10
    )

    raw = {
        "bullish_continuation": clamp(bull_score),
        "bearish_reversal": clamp(bear_score),
        "range_consolidation": clamp(range_score),
        "pullback_reversal_risk": clamp(reversal_score),
    }

    probabilities = normalize_probabilities(raw)
    most_likely = max(probabilities, key=probabilities.get)

    reasons = []

    if weekly >= 80:
        reasons.append("Weekly timeframe supports bullish continuation.")
    if daily >= 80:
        reasons.append("Daily timeframe supports bullish continuation.")
    if trend >= 80:
        reasons.append("Trend score is strong.")
    if structure >= 75:
        reasons.append("Market structure is healthy.")
    if vwap >= 75:
        reasons.append("Price is above VWAP.")
    if price_action >= 75:
        reasons.append("Price action supports continuation.")
    if hourly < 50:
        reasons.append("Short-term timeframe is weaker, so entry timing still matters.")
    if volume < 50:
        reasons.append("Volume is not strong enough yet, so confirmation matters.")

    return {
        "probabilities": probabilities,
        "most_likely": most_likely,
        "confidence": probabilities.get(most_likely, 0),
        "reasons": reasons,
    }