def safe_number(value, fallback=0):
    if value is None:
        return fallback

    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def build_risk_report(trade_plan, probability, account_size=1000, max_risk_percent=1):
    planned_entry = safe_number(trade_plan.get("planned_entry"))
    stop_loss = safe_number(trade_plan.get("stop_loss"))
    target_2 = safe_number(trade_plan.get("target_2"))

    risk_per_share = max(planned_entry - stop_loss, 0)
    reward_per_share = max(target_2 - planned_entry, 0)

    max_dollar_risk = round(account_size * (max_risk_percent / 100), 2)

    if risk_per_share > 0:
        shares_allowed = int(max_dollar_risk / risk_per_share)
    else:
        shares_allowed = 0

    probabilities = probability.get("probabilities", {})
    win_probability = safe_number(probabilities.get("bullish_continuation"), 0) / 100
    loss_probability = 1 - win_probability

    expected_value = round(
        (reward_per_share * win_probability) - (risk_per_share * loss_probability),
        2,
    )

    if risk_per_share <= 0:
        risk_rating = "INVALID"
        recommendation = "REJECTED"
    elif expected_value > 0 and shares_allowed > 0:
        risk_rating = "ACCEPTABLE"
        recommendation = "APPROVED"
    else:
        risk_rating = "WEAK"
        recommendation = "WAIT"

    return {
        "account_size": account_size,
        "max_risk_percent": max_risk_percent,
        "max_dollar_risk": max_dollar_risk,
        "risk_per_share": round(risk_per_share, 2),
        "reward_per_share": round(reward_per_share, 2),
        "shares_allowed": shares_allowed,
        "win_probability": round(win_probability * 100),
        "expected_value": expected_value,
        "risk_rating": risk_rating,
        "recommendation": recommendation,
    }