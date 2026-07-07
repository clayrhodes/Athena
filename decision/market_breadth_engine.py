"""
Athena Market Breadth Engine V2

Institutional market participation analysis.

This engine evaluates whether the broader market is
supporting or fighting the current trade thesis.

Supports:
- Advance / decline participation
- New highs vs new lows
- Percentage above 20 / 50 / 200 SMA
- Breadth thrust conditions
- Internal divergence warnings
- Safe fallback when no live breadth provider is connected
"""


def _num(value, default=0):
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def _pct(part, whole):
    part = _num(part)
    whole = _num(whole)

    if whole <= 0:
        return 0

    return round((part / whole) * 100, 2)


def _clamp_score(score):
    return max(0, min(100, int(score)))


def _get_breadth_data(market):
    """
    Accepts multiple possible keys so future providers can plug in easily.
    """

    return (
        market.get("market_breadth")
        or market.get("breadth")
        or market.get("internals")
        or {}
    )


def _get_value(data, *keys, default=0):
    for key in keys:
        if key in data:
            return data.get(key)
    return default


def build_market_breadth_report(
    market,
    thesis=None,
    market_regime=None,
):
    thesis = thesis or {}
    market_regime = market_regime or {}

    breadth_data = _get_breadth_data(market)

    advancers = _num(
        _get_value(
            breadth_data,
            "advancers",
            "advancing",
            "advance_issues",
            "nyse_advancers",
        )
    )

    decliners = _num(
        _get_value(
            breadth_data,
            "decliners",
            "declining",
            "decline_issues",
            "nyse_decliners",
        )
    )

    new_highs = _num(
        _get_value(
            breadth_data,
            "new_highs",
            "highs",
            "nyse_new_highs",
        )
    )

    new_lows = _num(
        _get_value(
            breadth_data,
            "new_lows",
            "lows",
            "nyse_new_lows",
        )
    )

    percent_above_20 = _num(
        _get_value(
            breadth_data,
            "percent_above_20_sma",
            "above_20_sma",
            "pct_above_20",
            default=None,
        ),
        default=None,
    )

    percent_above_50 = _num(
        _get_value(
            breadth_data,
            "percent_above_50_sma",
            "above_50_sma",
            "pct_above_50",
            default=None,
        ),
        default=None,
    )

    percent_above_200 = _num(
        _get_value(
            breadth_data,
            "percent_above_200_sma",
            "above_200_sma",
            "pct_above_200",
            default=None,
        ),
        default=None,
    )

    total_issues = advancers + decliners

    advance_percent = _pct(advancers, total_issues)
    decline_percent = _pct(decliners, total_issues)

    score = 50
    signals = []
    warnings = []

    breadth_thrust = False
    weak_participation = False
    internal_divergence = False
    data_connected = total_issues > 0

    if not data_connected:
        return {
            "score": 50,
            "condition": "NO LIVE BREADTH DATA",
            "status": "OFFLINE",
            "advance_percent": 0,
            "decline_percent": 0,
            "new_highs": 0,
            "new_lows": 0,
            "percent_above_20_sma": None,
            "percent_above_50_sma": None,
            "percent_above_200_sma": None,
            "breadth_thrust": False,
            "weak_participation": False,
            "internal_divergence": False,
            "signals": [],
            "warnings": [
                "No live market breadth data is connected yet."
            ],
            "summary": (
                "Market Breadth Condition: NO LIVE BREADTH DATA. "
                "Breadth score: 50/100."
            ),
        }

    if advance_percent >= 70:
        score += 25
        breadth_thrust = True
        signals.append(
            "Strong breadth thrust: advancers are heavily leading decliners."
        )

    elif advance_percent >= 65:
        score += 20
        breadth_thrust = True
        signals.append(
            "Bullish breadth thrust supports continuation."
        )

    elif advance_percent >= 55:
        score += 10
        signals.append(
            "Positive advance/decline participation supports the thesis."
        )

    elif decline_percent >= 70:
        score -= 25
        weak_participation = True
        warnings.append(
            "Severe negative breadth: decliners are heavily leading advancers."
        )

    elif decline_percent >= 60:
        score -= 20
        weak_participation = True
        warnings.append(
            "Decliners are leading advancers. Breadth is weakening."
        )

    if new_highs > new_lows and new_highs > 0:
        score += 10
        signals.append("New highs are leading new lows.")

    if new_lows > new_highs and new_lows > 0:
        score -= 10
        warnings.append("New lows are leading new highs.")

    if percent_above_20 is not None:
        if percent_above_20 >= 65:
            score += 8
            signals.append("Most stocks are above their 20-day moving average.")
        elif percent_above_20 <= 40:
            score -= 8
            warnings.append("Many stocks are below their 20-day moving average.")

    if percent_above_50 is not None:
        if percent_above_50 >= 65:
            score += 10
            signals.append("Most stocks are above their 50-day moving average.")
        elif percent_above_50 <= 40:
            score -= 10
            warnings.append("Many stocks are below their 50-day moving average.")

    if percent_above_200 is not None:
        if percent_above_200 >= 60:
            score += 7
            signals.append("Long-term market breadth remains healthy.")
        elif percent_above_200 <= 40:
            score -= 7
            warnings.append("Long-term market breadth is deteriorating.")

    thesis_bias = str(
        thesis.get("bias", thesis.get("forecast", ""))
    ).upper()

    regime_label = str(
        market_regime.get("regime", market_regime.get("bias", ""))
    ).upper()

    if "BULL" in thesis_bias and decline_percent >= 55:
        internal_divergence = True
        score -= 10
        warnings.append(
            "Bullish thesis conflicts with weak market internals."
        )

    if "BEAR" in thesis_bias and advance_percent >= 55:
        internal_divergence = True
        score -= 10
        warnings.append(
            "Bearish thesis conflicts with strong market internals."
        )

    if "BULL" in regime_label and decline_percent >= 60:
        internal_divergence = True
        score -= 8
        warnings.append(
            "Bullish regime conflicts with negative market breadth."
        )

    score = _clamp_score(score)

    if score >= 80:
        condition = "STRONG BROAD PARTICIPATION"
    elif score >= 70:
        condition = "BROAD PARTICIPATION"
    elif score <= 35:
        condition = "SEVERE WEAK PARTICIPATION"
    elif score <= 45:
        condition = "WEAK PARTICIPATION"
    elif internal_divergence:
        condition = "INTERNAL DIVERGENCE"
    else:
        condition = "NEUTRAL PARTICIPATION"

    return {
        "score": score,
        "condition": condition,
        "status": "LIVE",
        "advance_percent": advance_percent,
        "decline_percent": decline_percent,
        "new_highs": int(new_highs),
        "new_lows": int(new_lows),
        "percent_above_20_sma": percent_above_20,
        "percent_above_50_sma": percent_above_50,
        "percent_above_200_sma": percent_above_200,
        "breadth_thrust": breadth_thrust,
        "weak_participation": weak_participation,
        "internal_divergence": internal_divergence,
        "signals": signals,
        "warnings": warnings,
        "summary": (
            f"Market Breadth Condition: {condition}. "
            f"Advance participation: {advance_percent}%. "
            f"Breadth score: {score}/100."
        ),
    }