def format_reason_list(reasons):
    if not reasons:
        return "No trend evidence found."

    return "\n".join(f"- {reason}" for reason in reasons)


def build_trend_section(trend):
    evidence = format_reason_list(trend.get("evidence", []))

    return f"""
TREND ANALYSIS:
Score: {trend.get("score", "N/A")}
Direction: {trend.get("direction", "Unknown")}
Strength: {trend.get("strength", "Unknown")}
Summary: {trend.get("summary", "No trend summary available")}

Trend Evidence:
{evidence}
"""