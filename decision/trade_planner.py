def safe_number(value, fallback=0):
    if value is None:
        return fallback

    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def build_trade_plan(market, entry, buy_decision):
    current_price = safe_number(market.get("price"))
    atr = safe_number(market.get("atr"), 1)

    entry_price = safe_number(entry.get("entry_price"), current_price)
    stop_reference = safe_number(entry.get("stop_reference"), entry_price - atr)
    resistance_reference = safe_number(
        entry.get("resistance_reference"),
        entry_price + atr,
    )

    should_buy = buy_decision.get("should_buy", False) or buy_decision.get("answer") == "YES"

    if should_buy:
        direction = "CALL"
        action = "BUY NOW"
        planned_entry = current_price
    else:
        direction = "CALL WATCHLIST"
        action = "WAIT"
        planned_entry = entry_price

    stop_loss = round(min(stop_reference - (atr * 0.25), planned_entry - (atr * 0.75)), 2)

    target_1 = round(max(resistance_reference, planned_entry + (atr * 0.75)), 2)
    target_2 = round(planned_entry + (atr * 1.25), 2)
    target_3 = round(planned_entry + (atr * 2.0), 2)

    risk = round(planned_entry - stop_loss, 2)
    reward = round(target_2 - planned_entry, 2)

    risk_reward = round(reward / risk, 2) if risk > 0 else 0

    if risk_reward >= 2.5:
        quality = "Excellent"
    elif risk_reward >= 2.0:
        quality = "Good"
    elif risk_reward >= 1.5:
        quality = "Acceptable"
    else:
        quality = "Weak"

    if action == "BUY NOW":
        plan = "Buy now only if spread and liquidity are acceptable."
    elif entry.get("entry_type") == "Pullback to VWAP":
        plan = "Wait for price to pull back toward VWAP before entering."
    elif entry.get("entry_type") == "Reclaim Support":
        plan = "Wait for price to reclaim support before entering."
    else:
        plan = "Watch for confirmation before entering."

    return {
        "direction": direction,
        "action": action,
        "planned_entry": round(planned_entry, 2),
        "stop_loss": stop_loss,
        "target_1": target_1,
        "target_2": target_2,
        "target_3": target_3,
        "risk": risk,
        "reward": reward,
        "risk_reward": risk_reward,
        "quality": quality,
        "plan": plan,
    }