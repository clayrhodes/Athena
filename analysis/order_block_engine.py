"""
Athena Order Block Engine V1

Detects basic institutional order blocks from candle history.

Looks for:
- Bullish order blocks
- Bearish order blocks
- Displacement after the block
- Nearest active bullish/bearish zones

Safe version: if candle history is missing, Athena keeps running.
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

    candles = market.get("daily_candles")

    if isinstance(candles, list):
        return candles

    candles = market.get("ohlc")

    if isinstance(candles, list):
        return candles

    return []


def _body_size(candle):
    return abs(_num(candle.get("close")) - _num(candle.get("open")))


def _range_size(candle):
    return max(_num(candle.get("high")) - _num(candle.get("low")), 0.01)


def _is_bullish(candle):
    return _num(candle.get("close")) > _num(candle.get("open"))


def _is_bearish(candle):
    return _num(candle.get("close")) < _num(candle.get("open"))


def _has_displacement(candle):
    body = _body_size(candle)
    candle_range = _range_size(candle)

    return body >= candle_range * 0.55


def analyze_order_blocks(market):
    candles = _get_candles(market)
    current_price = _num(market.get("current_price", market.get("price")))

    bullish_blocks = []
    bearish_blocks = []
    signals = []
    warnings = []

    if len(candles) < 5:
        return {
            "name": "Order Block Engine",
            "score": 50,
            "bias": "neutral",
            "signals": ["Order Block Engine waiting for candle history."],
            "warnings": ["Not enough candles to detect order blocks."],
            "bullish_blocks": [],
            "bearish_blocks": [],
            "nearest_bullish_block": None,
            "nearest_bearish_block": None,
        }

    for i in range(1, len(candles) - 2):
        previous_candle = candles[i]
        next_candle = candles[i + 1]

        # Bullish order block:
        # Last bearish candle before strong bullish displacement.
        if _is_bearish(previous_candle) and _is_bullish(next_candle) and _has_displacement(next_candle):
            block = {
                "index": i,
                "type": "bullish",
                "low": _num(previous_candle.get("low")),
                "high": _num(previous_candle.get("high")),
                "open": _num(previous_candle.get("open")),
                "close": _num(previous_candle.get("close")),
                "displacement_candle_index": i + 1,
            }
            bullish_blocks.append(block)

        # Bearish order block:
        # Last bullish candle before strong bearish displacement.
        if _is_bullish(previous_candle) and _is_bearish(next_candle) and _has_displacement(next_candle):
            block = {
                "index": i,
                "type": "bearish",
                "low": _num(previous_candle.get("low")),
                "high": _num(previous_candle.get("high")),
                "open": _num(previous_candle.get("open")),
                "close": _num(previous_candle.get("close")),
                "displacement_candle_index": i + 1,
            }
            bearish_blocks.append(block)

    nearest_bullish_block = None
    nearest_bearish_block = None

    if current_price:
        valid_bullish = [
            block for block in bullish_blocks
            if block["low"] <= current_price
        ]

        valid_bearish = [
            block for block in bearish_blocks
            if block["high"] >= current_price
        ]

        if valid_bullish:
            nearest_bullish_block = sorted(
                valid_bullish,
                key=lambda block: abs(current_price - block["high"])
            )[0]

        if valid_bearish:
            nearest_bearish_block = sorted(
                valid_bearish,
                key=lambda block: abs(current_price - block["low"])
            )[0]

    score = 50

    if nearest_bullish_block:
        score += 15
        signals.append(
            "Bullish order block exists below/near current price."
        )

    if nearest_bearish_block:
        score -= 15
        signals.append(
            "Bearish order block exists above/near current price."
        )

    if bullish_blocks and len(bullish_blocks) > len(bearish_blocks):
        score += 8
        signals.append("More bullish order blocks than bearish order blocks.")

    if bearish_blocks and len(bearish_blocks) > len(bullish_blocks):
        score -= 8
        signals.append("More bearish order blocks than bullish order blocks.")

    score = max(0, min(100, int(score)))

    if score >= 65:
        bias = "bullish"
    elif score <= 35:
        bias = "bearish"
    else:
        bias = "neutral"

    if not signals:
        signals.append("No dominant order block bias detected yet.")

    return {
        "name": "Order Block Engine",
        "score": score,
        "bias": bias,
        "signals": signals,
        "warnings": warnings,
        "bullish_blocks": bullish_blocks,
        "bearish_blocks": bearish_blocks,
        "nearest_bullish_block": nearest_bullish_block,
        "nearest_bearish_block": nearest_bearish_block,
    }