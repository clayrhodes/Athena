"""
Athena Trade Management Engine V1

Evaluates what Athena should do AFTER a trade is already open.

This engine does not decide whether to enter.
It manages the trade thesis after entry.
"""


def _num(value):
    try:
        return float(value)
    except Exception:
        return 0.0


def build_trade_management_report(
    active_trade=None,
    market_structure=None,
    smart_money=None,
    liquidity=None,
    volume=None,
    price_action=None,
    probability=None,
):
    active_trade = active_trade or {}
    market_structure = market_structure or {}
    smart_money = smart_money or {}
    liquidity = liquidity or {}
    volume = volume or {}
    price_action = price_action or {}
    probability = probability or {}

    has_trade = bool(active_trade.get("is_open", False))

    if not has_trade:
        return {
            "status": "NO OPEN TRADE",
            "action": "NO MANAGEMENT NEEDED",
            "thesis_score": 0,
            "signals": [],
            "warnings": [],
            "exit_reasons": [],
            "summary": "No open trade detected. Trade management is standing by.",
        }

    thesis_score = 50
    signals = []
    warnings = []
    exit_reasons = []

    structure_score = _num(market_structure.get("score"))
    smart_money_score = _num(smart_money.get("score"))
    liquidity_score = _num(liquidity.get("score"))
    volume_score = _num(volume.get("score"))
    price_score = _num(price_action.get("score"))

    probabilities = probability.get("probabilities", {})
    bullish_continuation = _num(probabilities.get("bullish_continuation"))
    bearish_reversal = _num(probabilities.get("bearish_reversal"))
    pullback_risk = _num(probabilities.get("pullback_reversal_risk"))

    if structure_score >= 75:
        thesis_score += 10
        signals.append("Market structure still supports the trade thesis.")
    elif structure_score <= 45:
        thesis_score -= 15
        warnings.append("Market structure is weakening.")
        exit_reasons.append("Structure no longer supports the original thesis.")

    if smart_money_score >= 70:
        thesis_score += 10
        signals.append("Smart money behavior supports staying in the trade.")
    elif smart_money_score <= 45:
        thesis_score -= 10
        warnings.append("Smart money confirmation is weak.")

    if liquidity_score >= 70:
        thesis_score += 5
        signals.append("Liquidity conditions remain acceptable.")
    elif liquidity_score <= 45:
        thesis_score -= 10
        warnings.append("Liquidity conditions are weakening.")

    if volume_score >= 70:
        thesis_score += 10
        signals.append("Volume confirms the trade thesis.")
    elif volume_score <= 45:
        thesis_score -= 15
        warnings.append("Volume is not confirming the trade.")
        exit_reasons.append("Volume is failing to support continuation.")

    if price_score >= 70:
        thesis_score += 10
        signals.append("Price action remains supportive.")
    elif price_score <= 45:
        thesis_score -= 15
        warnings.append("Price action is weakening.")
        exit_reasons.append("Price action no longer supports holding.")

    if bullish_continuation >= 65:
        thesis_score += 10
        signals.append("Probability favors continuation.")
    elif bearish_reversal >= 35 or pullback_risk >= 30:
        thesis_score -= 10
        warnings.append("Reversal or pullback risk is elevated.")

    thesis_score = max(0, min(100, round(thesis_score, 2)))

    if thesis_score >= 85:
        action = "HOLD / CONSIDER ADDING ONLY ON CONFIRMATION"
        status = "THESIS STRONG"
    elif thesis_score >= 70:
        action = "HOLD"
        status = "THESIS VALID"
    elif thesis_score >= 55:
        action = "HOLD BUT DO NOT ADD"
        status = "THESIS MIXED"
    elif thesis_score >= 40:
        action = "REDUCE RISK / CONSIDER TRIMMING"
        status = "THESIS WEAKENING"
    else:
        action = "EXIT / THESIS FAILED"
        status = "THESIS FAILED"

    return {
        "status": status,
        "action": action,
        "thesis_score": thesis_score,
        "signals": signals,
        "warnings": warnings,
        "exit_reasons": exit_reasons,
        "summary": f"Trade management status: {status}. Recommended action: {action}.",
    }