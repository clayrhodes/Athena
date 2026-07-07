"""
Athena Institutional Structure Engine V1

Builds richer structure data for Smart Money and Liquidity engines.
"""


def _num(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def _clamp(value, low=0, high=100):
    return max(low, min(high, int(value)))


def analyze_institutional_structure(market):
    current_price = _num(market.get("current_price", market.get("price")))
    open_price = _num(market.get("open"))
    high = _num(market.get("high"))
    low = _num(market.get("low"))
    previous_close = _num(market.get("previous_close"))

    vwap_data = market.get("vwap", {})
    if isinstance(vwap_data, dict):
        vwap_price = _num(vwap_data.get("price", market.get("vwap_price")))
    else:
        vwap_price = _num(market.get("vwap_price"))

    score = 50
    signals = []

    broke_support = False
    reclaimed_support = False
    broke_resistance = False
    rejected_resistance = False

    long_lower_wick = False
    long_upper_wick = False
    near_support = False
    near_resistance = False

    above_vwap = False
    below_vwap = False

    if current_price and vwap_price:
        above_vwap = current_price > vwap_price
        below_vwap = current_price < vwap_price

    if current_price and low and high:
        day_range = max(high - low, 0.01)

        if open_price:
            lower_wick_size = min(open_price, current_price) - low
            upper_wick_size = high - max(open_price, current_price)
        else:
            lower_wick_size = current_price - low
            upper_wick_size = high - current_price

        long_lower_wick = lower_wick_size >= day_range * 0.35
        long_upper_wick = upper_wick_size >= day_range * 0.35

        near_support = current_price <= low + day_range * 0.25
        near_resistance = current_price >= high - day_range * 0.25

    if previous_close and low and current_price:
        broke_support = low < previous_close
        reclaimed_support = broke_support and current_price > previous_close

    if previous_close and high and current_price:
        broke_resistance = high > previous_close
        rejected_resistance = broke_resistance and current_price < previous_close

    if broke_support and reclaimed_support:
        score += 18
        signals.append("Price swept below previous close and reclaimed it.")

    if broke_resistance and rejected_resistance:
        score -= 18
        signals.append("Price swept above previous close and rejected it.")

    if long_lower_wick:
        score += 8
        signals.append("Long lower wick suggests sell-side liquidity response.")

    if long_upper_wick:
        score -= 8
        signals.append("Long upper wick suggests buy-side liquidity rejection.")

    if above_vwap:
        score += 6
        signals.append("Price is trading above VWAP.")

    if below_vwap:
        score -= 6
        signals.append("Price is trading below VWAP.")

    score = _clamp(score)

    if score >= 65:
        bias = "bullish"
    elif score <= 35:
        bias = "bearish"
    else:
        bias = "neutral"

    if not signals:
        signals.append("No institutional structure evidence detected yet.")

    return {
        "name": "Institutional Structure Engine",
        "score": score,
        "bias": bias,
        "signals": signals,
        "broke_support": broke_support,
        "reclaimed_support": reclaimed_support,
        "broke_resistance": broke_resistance,
        "rejected_resistance": rejected_resistance,
        "long_lower_wick": long_lower_wick,
        "long_upper_wick": long_upper_wick,
        "near_support": near_support,
        "near_resistance": near_resistance,
        "above_vwap": above_vwap,
        "below_vwap": below_vwap,
    }