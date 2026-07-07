def _format_list(items, empty_text):
    if not items:
        return empty_text

    if isinstance(items, str):
        return items

    lines = []

    for item in items:
        if isinstance(item, dict):
            lines.append(f"- {item.get('label', item.get('key', 'Unknown'))}")
        else:
            lines.append(f"- {item}")

    return "\n".join(lines)


def build_market_section(
    price_action,
    support_text,
    resistance_text,
    vwap,
    mtf,
    decision,
    scores,
    decision_matrix=None,
):
    decision_matrix = decision_matrix or {}

    failed_checks = decision_matrix.get("failed", [])
    waiting_for = decision_matrix.get("hard_blocks", [])

    failed_text = _format_list(failed_checks, "None")
    waiting_text = _format_list(waiting_for, "Nothing")

    return f"""
PRICE ACTION:
Score: {price_action.get("score", "N/A")}
Summary: {price_action.get("summary", "No price action summary available")}

SUPPORT / RESISTANCE:
Nearest Support: {support_text}
Nearest Resistance: {resistance_text}

VWAP:
Score: {vwap.get("score", "N/A")}
Status: {vwap.get("status", "Unknown")}

MULTI-TIMEFRAME:
Weekly Score: {mtf.get("Weekly", {}).get("score", "N/A")}
Daily Score: {mtf.get("Daily", {}).get("score", "N/A")}
1 Hour Score: {mtf.get("1 Hour", {}).get("score", "N/A")}

FAILED CHECKS:
{failed_text}

WAITING FOR:
{waiting_text}

OVERALL:
Overall Score: {scores.get("overall_score", "N/A")}
Trade Grade: {scores.get("trade_grade", "N/A")}
Confidence: {scores.get("confidence", "N/A")}
"""