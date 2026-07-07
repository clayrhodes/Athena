"""
Athena Liquidity Engine V3

Institutional liquidity analysis.

Detects:
- Equal highs
- Equal lows
- Buy-side liquidity
- Sell-side liquidity
- Liquidity pools
- Liquidity sweeps
- Reclaimed lows
- Rejected highs
"""


def _num(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def _text(value):
    try:
        return str(value).lower()
    except Exception:
        return ""


def _clamp(value, low=0, high=100):
    return max(low, min(high, int(value)))


def build_liquidity_report(price_action=None, market_structure=None, volume=None):
    price_action = price_action or {}
    market_structure = market_structure or {}
    volume = volume or {}

    score = 50
    signals = []
    warnings = []

    price_score = _num(price_action.get("score"))
    volume_score = _num(volume.get("score"))
    structure_score = _num(market_structure.get("score"))

    bullish = _num(price_action.get("bullish_score"))
    bearish = _num(price_action.get("bearish_score"))

    trend = _text(market_structure.get("trend"))
    price_bias = _text(price_action.get("bias"))
    volume_bias = _text(volume.get("bias"))

    high_volume = volume_score >= 70 or bool(volume.get("high_volume"))
    low_volume = volume_score < 45 or bool(volume.get("low_volume"))

    near_support = bool(price_action.get("near_support"))
    near_resistance = bool(price_action.get("near_resistance"))

    long_lower_wick = bool(price_action.get("long_lower_wick"))
    long_upper_wick = bool(price_action.get("long_upper_wick"))

    broke_support = bool(price_action.get("broke_support"))
    reclaimed_support = bool(price_action.get("reclaimed_support"))

    broke_resistance = bool(price_action.get("broke_resistance"))
    rejected_resistance = bool(price_action.get("rejected_resistance"))

    equal_highs = False
    equal_lows = False
    buy_side_liquidity = False
    sell_side_liquidity = False
    liquidity_pool = False
    liquidity_sweep = False
    swept_lows = False
    swept_highs = False
    reclaimed_lows = False
    rejected_highs = False

    # Equal highs / buy-side liquidity
    if bearish >= bullish and structure_score >= 65:
        equal_highs = True
        buy_side_liquidity = True
        score += 6
        signals.append("Possible equal highs creating buy-side liquidity.")

    # Equal lows / sell-side liquidity
    if bullish >= bearish and structure_score >= 65:
        equal_lows = True
        sell_side_liquidity = True
        score += 6
        signals.append("Possible equal lows creating sell-side liquidity.")

    # Liquidity pool
    if high_volume and structure_score >= 65:
        liquidity_pool = True
        score += 10
        signals.append("Institutional liquidity pool possible.")

    # Bullish sweep
    if broke_support and reclaimed_support:
        liquidity_sweep = True
        swept_lows = True
        reclaimed_lows = True
        score += 18
        signals.append("Bullish liquidity sweep: lows were taken and reclaimed.")

    if near_support and long_lower_wick and high_volume:
        liquidity_sweep = True
        swept_lows = True
        reclaimed_lows = True
        score += 12
        signals.append("Sell-side liquidity may have been swept near support.")

    # Bearish sweep
    if broke_resistance and rejected_resistance:
        liquidity_sweep = True
        swept_highs = True
        rejected_highs = True
        score += 18
        signals.append("Bearish liquidity sweep: highs were taken and rejected.")

    if near_resistance and long_upper_wick and high_volume:
        liquidity_sweep = True
        swept_highs = True
        rejected_highs = True
        score += 12
        signals.append("Buy-side liquidity may have been swept near resistance.")

    # Bias
    if swept_lows and reclaimed_lows:
        bias = "bullish"
        score += 5
    elif swept_highs and rejected_highs:
        bias = "bearish"
        score -= 5
    elif volume_bias in ["bullish", "bearish"]:
        bias = volume_bias
    elif price_bias in ["bullish", "bearish"]:
        bias = price_bias
    else:
        bias = "neutral"

    if low_volume:
        warnings.append("Low volume makes liquidity detection less reliable.")
        score -= 5

    score = _clamp(score)

    if liquidity_sweep and bias == "bullish":
        condition = "BULLISH LIQUIDITY SWEEP"
    elif liquidity_sweep and bias == "bearish":
        condition = "BEARISH LIQUIDITY SWEEP"
    elif liquidity_pool:
        condition = "HIGH LIQUIDITY"
    elif score <= 40:
        condition = "LOW LIQUIDITY"
    else:
        condition = "BALANCED"

    if not signals:
        signals.append("No liquidity evidence available.")

    return {
        "name": "Liquidity Engine",
        "score": score,
        "bias": bias,
        "condition": condition,
        "equal_highs": equal_highs,
        "equal_lows": equal_lows,
        "buy_side_liquidity": buy_side_liquidity,
        "sell_side_liquidity": sell_side_liquidity,
        "liquidity_pool": liquidity_pool,
        "liquidity_sweep": liquidity_sweep,
        "swept_lows": swept_lows,
        "swept_highs": swept_highs,
        "reclaimed_lows": reclaimed_lows,
        "rejected_highs": rejected_highs,
        "signals": signals,
        "warnings": warnings,
        "summary": (
            f"Liquidity Condition: {condition}. "
            f"Bias: {bias}. "
            f"Liquidity score: {score}/100."
        ),
    }


def format_liquidity_report(report):
    lines = []

    lines.append("ATHENA LIQUIDITY")
    lines.append("----------------")
    lines.append(f"Condition: {report.get('condition')}")
    lines.append(f"Bias: {report.get('bias')}")
    lines.append(f"Score: {report.get('score')}/100")
    lines.append("")

    lines.append("Signals:")
    for signal in report.get("signals", []):
        lines.append(f"- {signal}")

    if report.get("warnings"):
        lines.append("")
        lines.append("Warnings:")
        for warning in report.get("warnings", []):
            lines.append(f"- {warning}")

    return "\n".join(lines)