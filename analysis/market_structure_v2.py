"""
Athena Market Structure Engine V2

Institutional candle-sequence structure engine.

Detects:
- Swing highs
- Swing lows
- Break of Structure (BOS)
- Change of Character (CHoCH)
- Trend bias
- Basic liquidity targets

Safe version: works even if candle data is missing.
"""


def _num(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def _get_candles(market):
    candles = market.get("candles")
    if isinstance(candles, list):
        return candles

    candles = market.get("ohlc")
    if isinstance(candles, list):
        return candles

    candles = market.get("history")
    if isinstance(candles, list):
        return candles

    return []


def _candle_value(candle, key):
    if isinstance(candle, dict):
        return _num(candle.get(key))
    return 0.0


def analyze_market_structure_v2(market):
    candles = _get_candles(market)

    signals = []
    warnings = []

    swing_highs = []
    swing_lows = []

    bos_bullish = False
    bos_bearish = False
    choch_bullish = False
    choch_bearish = False

    current_price = _num(market.get("current_price", market.get("price")))

    if len(candles) < 5:
        warnings.append("Not enough candle history for Market Structure V2.")
        return {
            "name": "Market Structure Engine V2",
            "score": 50,
            "bias": "neutral",
            "trend": "neutral",
            "signals": ["Market Structure V2 waiting for candle history."],
            "warnings": warnings,
            "swing_highs": [],
            "swing_lows": [],
            "last_swing_high": None,
            "last_swing_low": None,
            "bos_bullish": False,
            "bos_bearish": False,
            "choch_bullish": False,
            "choch_bearish": False,
            "buy_side_liquidity": None,
            "sell_side_liquidity": None,
        }

    for i in range(1, len(candles) - 1):
        prev_candle = candles[i - 1]
        candle = candles[i]
        next_candle = candles[i + 1]

        high = _candle_value(candle, "high")
        low = _candle_value(candle, "low")

        prev_high = _candle_value(prev_candle, "high")
        next_high = _candle_value(next_candle, "high")

        prev_low = _candle_value(prev_candle, "low")
        next_low = _candle_value(next_candle, "low")

        if high > prev_high and high > next_high:
            swing_highs.append({
                "index": i,
                "price": high,
            })

        if low < prev_low and low < next_low:
            swing_lows.append({
                "index": i,
                "price": low,
            })

    last_swing_high = swing_highs[-1]["price"] if swing_highs else None
    last_swing_low = swing_lows[-1]["price"] if swing_lows else None

    score = 50

    if current_price and last_swing_high and current_price > last_swing_high:
        bos_bullish = True
        score += 20
        signals.append("Bullish Break of Structure above last swing high.")

    if current_price and last_swing_low and current_price < last_swing_low:
        bos_bearish = True
        score -= 20
        signals.append("Bearish Break of Structure below last swing low.")

    if len(swing_highs) >= 2 and len(swing_lows) >= 2:
        previous_high = swing_highs[-2]["price"]
        latest_high = swing_highs[-1]["price"]

        previous_low = swing_lows[-2]["price"]
        latest_low = swing_lows[-1]["price"]

        higher_high = latest_high > previous_high
        higher_low = latest_low > previous_low
        lower_high = latest_high < previous_high
        lower_low = latest_low < previous_low

        if higher_high and higher_low:
            score += 15
            trend = "bullish"
            signals.append("Structure shows higher highs and higher lows.")
        elif lower_high and lower_low:
            score -= 15
            trend = "bearish"
            signals.append("Structure shows lower highs and lower lows.")
        else:
            trend = "mixed"
            signals.append("Structure is mixed or transitioning.")

        if lower_low and current_price > latest_high:
            choch_bullish = True
            score += 15
            signals.append("Bullish Change of Character detected.")

        if higher_high and current_price < latest_low:
            choch_bearish = True
            score -= 15
            signals.append("Bearish Change of Character detected.")
    else:
        trend = "neutral"
        warnings.append("Not enough swing points to confirm structure trend.")

    score = max(0, min(100, int(score)))

    if score >= 65:
        bias = "bullish"
    elif score <= 35:
        bias = "bearish"
    else:
        bias = "neutral"

    if not signals:
        signals.append("No major structure break detected yet.")

    return {
        "name": "Market Structure Engine V2",
        "score": score,
        "bias": bias,
        "trend": trend,
        "signals": signals,
        "warnings": warnings,
        "swing_highs": swing_highs,
        "swing_lows": swing_lows,
        "last_swing_high": last_swing_high,
        "last_swing_low": last_swing_low,
        "bos_bullish": bos_bullish,
        "bos_bearish": bos_bearish,
        "choch_bullish": choch_bullish,
        "choch_bearish": choch_bearish,
        "buy_side_liquidity": last_swing_high,
        "sell_side_liquidity": last_swing_low,
    }