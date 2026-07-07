"""
Athena Options Flow Engine V1

Institutional options activity analysis.

Current support:

- Call vs Put flow
- Bullish vs Bearish premium
- Sweep detection
- Block trade detection
- Unusual activity detection
- Flow conviction scoring

Designed to work safely now and accept live options
flow data later.
"""


def _num(value, default=0):
    try:
        return float(value)
    except Exception:
        return default


def build_options_flow_report(market):
    options_data = market.get("options_flow", {})

    call_premium = _num(options_data.get("call_premium"))
    put_premium = _num(options_data.get("put_premium"))
    bullish_premium = _num(options_data.get("bullish_premium"))
    bearish_premium = _num(options_data.get("bearish_premium"))

    sweep_count = _num(options_data.get("sweep_count"))
    block_count = _num(options_data.get("block_count"))
    unusual_count = _num(options_data.get("unusual_count"))

    total_directional_premium = bullish_premium + bearish_premium

    score = 50
    signals = []
    warnings = []

    bullish_flow = False
    bearish_flow = False
    unusual_activity = False
    sweep_activity = False
    block_activity = False

    if call_premium > put_premium and call_premium > 0:
        score += 10
        bullish_flow = True
        signals.append("Call premium is leading put premium.")

    if put_premium > call_premium and put_premium > 0:
        score -= 10
        bearish_flow = True
        warnings.append("Put premium is leading call premium.")

    if bullish_premium > bearish_premium and bullish_premium > 0:
        score += 15
        bullish_flow = True
        signals.append("Bullish premium is leading bearish premium.")

    if bearish_premium > bullish_premium and bearish_premium > 0:
        score -= 15
        bearish_flow = True
        warnings.append("Bearish premium is leading bullish premium.")

    if sweep_count >= 3:
        score += 10
        sweep_activity = True
        unusual_activity = True
        signals.append("Multiple sweep orders detected.")

    if block_count >= 2:
        score += 8
        block_activity = True
        unusual_activity = True
        signals.append("Large block trade activity detected.")

    if unusual_count >= 3:
        score += 10
        unusual_activity = True
        signals.append("Unusual options activity detected.")

    if bullish_flow and bearish_flow:
        score -= 8
        warnings.append("Mixed options flow detected.")

    if total_directional_premium == 0:
        condition = "NO LIVE OPTIONS FLOW DATA"
        warnings.append("No live options flow data is connected yet.")
    else:
        if score >= 75:
            condition = "BULLISH INSTITUTIONAL FLOW"
        elif score <= 35:
            condition = "BEARISH INSTITUTIONAL FLOW"
        elif unusual_activity:
            condition = "UNUSUAL MIXED FLOW"
        else:
            condition = "NEUTRAL FLOW"

    score = max(0, min(100, int(score)))

    return {
        "score": score,
        "condition": condition,
        "call_premium": call_premium,
        "put_premium": put_premium,
        "bullish_premium": bullish_premium,
        "bearish_premium": bearish_premium,
        "sweep_count": int(sweep_count),
        "block_count": int(block_count),
        "unusual_count": int(unusual_count),
        "bullish_flow": bullish_flow,
        "bearish_flow": bearish_flow,
        "unusual_activity": unusual_activity,
        "sweep_activity": sweep_activity,
        "block_activity": block_activity,
        "signals": signals,
        "warnings": warnings,
        "summary": (
            f"Options Flow Condition: {condition}. "
            f"Options flow score: {score}/100."
        ),
    }