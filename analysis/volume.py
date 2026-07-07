def analyze_volume(market):

    score = 50
    reasons = []

    current_volume = market["current_volume"]
    average_volume = market["average_volume"]

    if current_volume > average_volume:
        score += 30
        reasons.append("Volume is above the 20-day average")
    else:
        score -= 20
        reasons.append("Volume is below the 20-day average")

    score = max(0, min(100, score))

    return {
        "score": score,
        "reasons": reasons
    }