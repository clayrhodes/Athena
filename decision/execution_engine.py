"""
Athena Execution Engine V1

Determines whether the setup is actually ready for entry.

This engine does NOT decide overall market direction.
It focuses only on trade timing and entry quality.
"""


def _num(value):
    try:
        return float(value)
    except Exception:
        return 0.0


def build_execution_report(
    market_structure=None,
    liquidity=None,
    smart_money=None,
    volume=None,
    price_action=None,
):
    market_structure = market_structure or {}
    liquidity = liquidity or {}
    smart_money = smart_money or {}
    volume = volume or {}
    price_action = price_action or {}

    score = 50
    signals = []
    waiting_for = []
    warnings = []

    structure_score = _num(market_structure.get("score"))
    liquidity_score = _num(liquidity.get("score"))
    smart_money_score = _num(smart_money.get("score"))
    volume_score = _num(volume.get("score"))
    price_score = _num(price_action.get("score"))

    if structure_score >= 75:
        score += 10
        signals.append("Market structure supports entry timing.")
    elif structure_score <= 45:
        score -= 10
        waiting_for.append("Cleaner market structure.")

    if liquidity_score >= 75:
        score += 10
        signals.append("Liquidity conditions support execution.")
    elif liquidity_score <= 45:
        score -= 10
        waiting_for.append("Better liquidity conditions.")

    if smart_money_score >= 75:
        score += 10
        signals.append("Smart money behavior supports entry.")
    elif smart_money_score <= 45:
        score -= 10
        waiting_for.append("Institutional confirmation.")

    if volume_score >= 70:
        score += 10
        signals.append("Volume is confirming the setup.")
    elif volume_score <= 50:
        score -= 15
        waiting_for.append("Volume confirmation.")
        warnings.append("Volume is not strong enough yet.")

    if price_score >= 70:
        score += 10
        signals.append("Price action supports entry.")
    elif price_score <= 45:
        score -= 10
        waiting_for.append("Stronger price action confirmation.")

    if score >= 90:
        status = "READY FOR ENTRY"
    elif score >= 75:
        status = "ALMOST READY"
    elif score >= 60:
        status = "WATCH FOR ENTRY"
    else:
        status = "NOT READY"

    score = max(0, min(100, round(score, 2)))

    return {
        "score": score,
        "status": status,
        "signals": signals,
        "waiting_for": waiting_for,
        "warnings": warnings,
        "summary": f"Execution readiness is {score}/100: {status}.",
    }