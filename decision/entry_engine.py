def safe_number(value, fallback):
    if value is None:
        return fallback

    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def build_entry_response(
    status,
    current_price,
    entry_price,
    entry_type,
    aggressive_entry,
    conservative_entry,
    stop_reference,
    resistance_reference,
    reason,
    expected_hold,
):
    entry_low = min(entry_price, conservative_entry)
    entry_high = max(entry_price, aggressive_entry)

    return {
        # Old keys trade_planner.py still expects
        "status": status,
        "entry_low": round(entry_low, 2),
        "entry_high": round(entry_high, 2),
        "distance": round(current_price - entry_high, 2),
        "message": reason,

        # New smarter keys report.py uses
        "entry_price": round(entry_price, 2),
        "entry_type": entry_type,
        "aggressive_entry": round(aggressive_entry, 2),
        "conservative_entry": round(conservative_entry, 2),
        "stop_reference": round(stop_reference, 2),
        "resistance_reference": round(resistance_reference, 2),
        "reason": reason,
        "expected_hold": expected_hold,
    }


def calculate_entry(market, buy_decision):
    current_price = safe_number(market.get("price"), 0)

    vwap_data = market.get("vwap", {})
    if not isinstance(vwap_data, dict):
        vwap_data = {}

    vwap = safe_number(vwap_data.get("price"), current_price)

    sr = market.get("support_resistance", {})
    if not isinstance(sr, dict):
        sr = {}

    support_data = sr.get("nearest_support") or {}
    resistance_data = sr.get("nearest_resistance") or {}

    support = safe_number(support_data.get("price"), vwap)
    resistance = safe_number(resistance_data.get("price"), current_price * 1.01)

    if buy_decision.get("should_buy", False):
        return build_entry_response(
            status="BUY NOW",
            current_price=current_price,
            entry_price=current_price,
            entry_type="Immediate Entry",
            aggressive_entry=current_price,
            conservative_entry=vwap,
            stop_reference=support,
            resistance_reference=resistance,
            reason="All buy conditions currently pass.",
            expected_hold="2–5 days",
        )

    if current_price > vwap:
        return build_entry_response(
            status="WAIT",
            current_price=current_price,
            entry_price=vwap,
            entry_type="Pullback to VWAP",
            aggressive_entry=current_price,
            conservative_entry=vwap,
            stop_reference=support,
            resistance_reference=resistance,
            reason="Price is extended above VWAP. Wait for a pullback.",
            expected_hold="2–5 days",
        )

    if current_price < support:
        return build_entry_response(
            status="WAIT",
            current_price=current_price,
            entry_price=support,
            entry_type="Reclaim Support",
            aggressive_entry=support,
            conservative_entry=vwap,
            stop_reference=support * 0.995,
            resistance_reference=resistance,
            reason="Wait for price to reclaim support before entering.",
            expected_hold="2–5 days",
        )

    return build_entry_response(
        status="WATCH",
        current_price=current_price,
        entry_price=current_price,
        entry_type="Inside Buy Zone",
        aggressive_entry=current_price,
        conservative_entry=vwap,
        stop_reference=support,
        resistance_reference=resistance,
        reason="Price is already inside the preferred buy zone.",
        expected_hold="2–5 days",
    )