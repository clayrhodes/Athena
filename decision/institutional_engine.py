"""
Athena Institutional Engine V1
Uses Athena's completed analysis engines instead of raw market data.
"""


def _extract_score(data):
    """
    Attempts to extract a normalized 0-100 score from an engine output.
    """

    if isinstance(data, (int, float)):
        return float(data)

    if isinstance(data, dict):
        for key in (
            "score",
            "strength",
            "confidence",
            "value",
            "overall_score",
            "overall",
        ):
            value = data.get(key)
            if isinstance(value, (int, float)):
                return float(value)

    return 50.0


def build_institutional_report(
    trend,
    market_structure,
    multi_timeframe,
    vwap,
    momentum,
    volume,
    auction_flow,
    market_regime,
):

    trend_score = _extract_score(trend)
    structure_score = _extract_score(market_structure)
    mtf_score = _extract_score(multi_timeframe)
    vwap_score = _extract_score(vwap)
    momentum_score = _extract_score(momentum)
    volume_score = _extract_score(volume)
    auction_score = _extract_score(auction_flow)
    regime_score = _extract_score(market_regime)

    score = (
        trend_score * 0.20
        + structure_score * 0.15
        + mtf_score * 0.15
        + vwap_score * 0.10
        + momentum_score * 0.10
        + volume_score * 0.10
        + auction_score * 0.10
        + regime_score * 0.10
    )

    score = round(score)

    reasons = []

    if trend_score >= 70:
        reasons.append("Higher timeframe trend favors institutions.")

    if structure_score >= 70:
        reasons.append("Healthy market structure.")

    if mtf_score >= 70:
        reasons.append("Timeframes are aligned.")

    if vwap_score >= 70:
        reasons.append("Price remains above value.")

    if momentum_score >= 70:
        reasons.append("Momentum confirms participation.")

    if volume_score >= 70:
        reasons.append("Strong participation volume.")

    if auction_score >= 70:
        reasons.append("Auction flow favors buyers.")

    if regime_score >= 70:
        reasons.append("Market regime supports continuation.")

    if score >= 80:
        bias = "INSTITUTIONAL ACCUMULATION"
        confidence = "HIGH"

    elif score >= 65:
        bias = "ACCUMULATION"
        confidence = "GOOD"

    elif score >= 45:
        bias = "NEUTRAL"
        confidence = "MODERATE"

    elif score >= 30:
        bias = "DISTRIBUTION"
        confidence = "GOOD"

    else:
        bias = "INSTITUTIONAL DISTRIBUTION"
        confidence = "HIGH"

    return {
        "institutional_score": score,
        "institutional_bias": bias,
        "institutional_confidence": confidence,
        "institutional_reasons": reasons,
    }