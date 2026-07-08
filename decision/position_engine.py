"""
Athena Position Engine V1

Creates a standardized open-position object for Athena.

This engine is broker-safe:
- If no position is provided, Athena assumes no open trade.
- If a position is provided, Athena normalizes it so other engines can use it.
"""


def _num(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def build_position_report(position=None):
    position = position or {}

    symbol = position.get("symbol")
    quantity = _num(position.get("quantity"))
    entry_price = _num(position.get("entry_price"))
    current_price = _num(position.get("current_price"))
    position_type = position.get("type", "UNKNOWN")
    direction = position.get("direction", "UNKNOWN")

    is_open = bool(symbol and quantity != 0 and entry_price > 0)

    if not is_open:
        return {
            "is_open": False,
            "symbol": None,
            "type": "NONE",
            "direction": "NONE",
            "quantity": 0,
            "entry_price": 0,
            "current_price": 0,
            "unrealized_pl": 0,
            "unrealized_pl_percent": 0,
            "status": "NO OPEN POSITION",
            "summary": "No open position detected.",
        }

    unrealized_pl = 0
    unrealized_pl_percent = 0

    if current_price > 0:
        if direction.upper() in ["LONG", "CALL", "BULLISH"]:
            unrealized_pl = (current_price - entry_price) * quantity
            unrealized_pl_percent = ((current_price - entry_price) / entry_price) * 100
        elif direction.upper() in ["SHORT", "PUT", "BEARISH"]:
            unrealized_pl = (entry_price - current_price) * quantity
            unrealized_pl_percent = ((entry_price - current_price) / entry_price) * 100

    return {
        "is_open": True,
        "symbol": symbol,
        "type": position_type,
        "direction": direction,
        "quantity": quantity,
        "entry_price": entry_price,
        "current_price": current_price,
        "unrealized_pl": round(unrealized_pl, 2),
        "unrealized_pl_percent": round(unrealized_pl_percent, 2),
        "status": "OPEN POSITION",
        "summary": (
            f"Open {direction} {position_type} position detected for {symbol}. "
            f"Unrealized P/L: {round(unrealized_pl, 2)} "
            f"({round(unrealized_pl_percent, 2)}%)."
        ),
    }