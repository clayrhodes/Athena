"""
Athena Smart Money Engine V4

Institutional behavior engine.

Uses:
- Market structure
- Price action
- Volume
- Liquidity
- Order blocks

Detects:
- Accumulation
- Distribution
- Absorption
- Stop hunts
- Liquidity sweeps
- Trapped traders
- Order block support/resistance
"""


def _num(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def _bool(value):
    return bool(value)


def _text(value):
    try:
        return str(value).lower()
    except Exception:
        return ""


def _clamp(value, low=0, high=100):
    return max(low, min(high, int(value)))


def build_smart_money_report(
    market_structure=None,
    volume=None,
    price_action=None,
    liquidity=None,
):
    market_structure = market_structure or {}
    volume = volume or {}
    price_action = price_action or {}
    liquidity = liquidity or {}

    score = 50
    signals = []
    warnings = []
    failed_reasons = []

    structure_score = _num(market_structure.get("score"))
    volume_score = _num(volume.get("score"))
    price_score = _num(price_action.get("score"))
    liquidity_score = _num(liquidity.get("score"))

    trend = _text(market_structure.get("trend"))
    structure_bias = _text(market_structure.get("bias"))
    volume_bias = _text(volume.get("bias"))
    price_bias = _text(price_action.get("bias"))
    liquidity_bias = _text(liquidity.get("bias"))

    order_block_score = _num(price_action.get("order_block_score"), 50)
    order_block_bias = _text(price_action.get("order_block_bias"))

    bullish_ob = price_action.get("nearest_bullish_order_block")
    bearish_ob = price_action.get("nearest_bearish_order_block")

    near_support = _bool(price_action.get("near_support"))
    near_resistance = _bool(price_action.get("near_resistance"))

    high_volume = _bool(volume.get("high_volume")) or volume_score >= 70
    low_volume = _bool(volume.get("low_volume")) or volume_score < 45

    long_lower_wick = _bool(price_action.get("long_lower_wick"))
    long_upper_wick = _bool(price_action.get("long_upper_wick"))

    broke_support = _bool(price_action.get("broke_support"))
    reclaimed_support = _bool(price_action.get("reclaimed_support"))

    broke_resistance = _bool(price_action.get("broke_resistance"))
    rejected_resistance = _bool(price_action.get("rejected_resistance"))

    swept_lows = _bool(liquidity.get("swept_lows"))
    swept_highs = _bool(liquidity.get("swept_highs"))

    reclaimed_lows = _bool(liquidity.get("reclaimed_lows"))
    rejected_highs = _bool(liquidity.get("rejected_highs"))

    above_vwap = _bool(price_action.get("above_vwap"))
    below_vwap = _bool(price_action.get("below_vwap"))

    bos_bullish = _bool(price_action.get("bos_bullish"))
    bos_bearish = _bool(price_action.get("bos_bearish"))
    choch_bullish = _bool(price_action.get("choch_bullish"))
    choch_bearish = _bool(price_action.get("choch_bearish"))

    # ----------------------------
    # Order block behavior
    # ----------------------------

    if order_block_bias == "bullish":
        score += 10
        signals.append("Order block engine favors bullish institutional support.")

    if order_block_bias == "bearish":
        score -= 10
        signals.append("Order block engine favors bearish institutional resistance.")

    if bullish_ob:
        score += 8
        signals.append("Bullish order block exists below/near current price.")

    if bearish_ob:
        score -= 8
        signals.append("Bearish order block exists above/near current price.")

    if order_block_score >= 65:
        score += 5
        signals.append("Order block score supports bullish smart money bias.")

    if order_block_score <= 35:
        score -= 5
        signals.append("Order block score supports bearish smart money bias.")

    # ----------------------------
    # Market structure behavior
    # ----------------------------

    if bos_bullish:
        score += 10
        signals.append("Bullish break of structure supports institutional continuation.")

    if bos_bearish:
        score -= 10
        signals.append("Bearish break of structure warns of institutional downside.")

    if choch_bullish:
        score += 12
        signals.append("Bullish change of character detected.")

    if choch_bearish:
        score -= 12
        signals.append("Bearish change of character detected.")

    # ----------------------------
    # Bullish institutional behavior
    # ----------------------------

    if near_support and high_volume and long_lower_wick:
        score += 15
        signals.append("Accumulation possible near support.")

    if broke_support and reclaimed_support and high_volume:
        score += 18
        signals.append("Bullish stop hunt detected below support.")

    if swept_lows and reclaimed_lows:
        score += 18
        signals.append("Bullish liquidity sweep detected.")

    if high_volume and price_score >= 55 and structure_score < 50:
        score += 10
        signals.append("Bullish absorption detected.")

    if trend in ["bearish", "downtrend"] and price_bias in ["bullish", "reversal"] and high_volume:
        score += 8
        signals.append("Possible accumulation after bearish move.")

    if broke_support and reclaimed_support:
        score += 8
        signals.append("Bear trap possible: sellers may be trapped.")

    # ----------------------------
    # Bearish institutional behavior
    # ----------------------------

    if near_resistance and high_volume and long_upper_wick:
        score -= 15
        signals.append("Distribution possible near resistance.")

    if broke_resistance and rejected_resistance and high_volume:
        score -= 18
        signals.append("Bearish stop hunt detected above resistance.")

    if swept_highs and rejected_highs:
        score -= 18
        signals.append("Bearish liquidity sweep detected.")

    if high_volume and price_score <= 45 and structure_score > 50:
        score -= 10
        signals.append("Bearish absorption detected.")

    if trend in ["bullish", "uptrend"] and price_bias in ["bearish", "reversal"] and high_volume:
        score -= 8
        signals.append("Possible distribution after bullish move.")

    if broke_resistance and rejected_resistance:
        score -= 8
        signals.append("Bull trap possible: buyers may be trapped.")

    # ----------------------------
    # Bias confirmation
    # ----------------------------

    if volume_bias == "bullish":
        score += 5
    elif volume_bias == "bearish":
        score -= 5

    if liquidity_bias == "bullish":
        score += 5
    elif liquidity_bias == "bearish":
        score -= 5

    if structure_bias == "bullish":
        score += 3
    elif structure_bias == "bearish":
        score -= 3

    if price_bias == "bullish":
        score += 3
    elif price_bias == "bearish":
        score -= 3

    # ----------------------------
    # VWAP context
    # ----------------------------

    if above_vwap and score >= 55:
        score += 4
        signals.append("Price holding above VWAP supports bullish smart money bias.")

    if below_vwap and score <= 45:
        score -= 4
        signals.append("Price holding below VWAP supports bearish smart money bias.")

    # ----------------------------
    # Warnings / confidence reducers
    # ----------------------------

    if low_volume:
        warnings.append("Low volume reduces smart money confidence.")
        score -= 5

    if volume_score < 45:
        warnings.append("Volume is not confirming smart money activity.")
        failed_reasons.append("Volume is not confirming the move.")

    if liquidity_score < 45:
        warnings.append("Liquidity does not confirm institutional activity.")
        failed_reasons.append("Liquidity does not confirm the setup.")

    if not signals:
        signals.append("No strong institutional smart money footprint detected.")
        failed_reasons.append("No strong smart money footprint detected.")

    score = _clamp(score)

    if score >= 70:
        bias = "BULLISH SMART MONEY"
        passed = True
    elif score <= 30:
        bias = "BEARISH SMART MONEY"
        passed = True
    else:
        bias = "NEUTRAL / UNCLEAR SMART MONEY"
        passed = False

    return {
        "name": "Smart Money Engine",
        "score": score,
        "bias": bias,
        "passed": passed,
        "signals": signals,
        "warnings": warnings,
        "failed_reasons": failed_reasons,
        "accumulation": any("accumulation" in s.lower() for s in signals),
        "distribution": any("distribution" in s.lower() for s in signals),
        "absorption": any("absorption" in s.lower() for s in signals),
        "stop_hunt": any("stop hunt" in s.lower() for s in signals),
        "liquidity_sweep": any("liquidity sweep" in s.lower() for s in signals),
        "trapped_traders": any("trap" in s.lower() for s in signals),
        "order_block_supported": any("order block" in s.lower() for s in signals),
        "summary": (
            f"Smart Money Bias: {bias}. "
            f"Score: {score}/100. "
            f"Signals detected: {len(signals)}."
        ),
    }


def format_smart_money_report(report):
    lines = []

    lines.append("SMART MONEY ENGINE")
    lines.append("------------------")
    lines.append(f"Bias: {report.get('bias')}")
    lines.append(f"Score: {report.get('score')}/100")
    lines.append(f"Passed: {report.get('passed')}")
    lines.append("")

    lines.append("Signals:")
    for signal in report.get("signals", []):
        lines.append(f"- {signal}")

    if report.get("warnings"):
        lines.append("")
        lines.append("Warnings:")
        for warning in report.get("warnings", []):
            lines.append(f"- {warning}")

    if report.get("failed_reasons"):
        lines.append("")
        lines.append("Failed Reasons:")
        for reason in report.get("failed_reasons", []):
            lines.append(f"- {reason}")

    return "\n".join(lines)