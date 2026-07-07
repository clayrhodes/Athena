"""
Athena Market Breadth Report Section
"""


def build_market_breadth_section(market_breadth):
    lines = []

    lines.append("=======================================================")
    lines.append("ATHENA MARKET BREADTH")
    lines.append("-------------------------------------------------------")

    condition = (
        market_breadth.get("condition")
        or market_breadth.get("breadth")
        or "UNKNOWN"
    )

    lines.append(f"Condition: {condition}")

    lines.append(
        f"Score: {market_breadth.get('score', 0)}/100"
    )

    ad_ratio = market_breadth.get("advance_decline_ratio")

    if ad_ratio is not None:
        adv = round(ad_ratio * 100)
        dec = round((1 - ad_ratio) * 100)
    else:
        adv = market_breadth.get("advance_percent", 0)
        dec = market_breadth.get("decline_percent", 0)

    lines.append(f"Advancers: {adv}%")
    lines.append(f"Decliners: {dec}%")

    lines.append(
        f"New Highs: {market_breadth.get('new_highs', 0)}"
    )

    lines.append(
        f"New Lows: {market_breadth.get('new_lows', 0)}"
    )

    lines.append("")

    signals = (
        market_breadth.get("signals")
        or market_breadth.get("bullish_signals")
        or []
    )

    if signals:
        lines.append("Signals:")
        for signal in signals:
            lines.append(f"- {signal}")

    warnings = market_breadth.get("warnings", [])

    if warnings:
        lines.append("")
        lines.append("Warnings:")
        for warning in warnings:
            lines.append(f"- {warning}")

    lines.append("")
    lines.append(
        market_breadth.get(
            "summary",
            "No market breadth summary available.",
        )
    )

    return "\n".join(lines)