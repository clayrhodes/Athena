def format_reason_list(reasons):
    if not reasons:
        return "No major reasons found."

    return "\n".join(f"- {reason}" for reason in reasons)


def build_intelligence_section(intelligence):
    reasons = format_reason_list(intelligence.get("reasons", []))

    return f"""
================ ATHENA MISSION BRIEF ================

ATHENA INTELLIGENCE:
Recommendation: {intelligence.get("recommendation", "N/A")}
Overall Score: {intelligence.get("overall_score", "N/A")}
Trade Grade: {intelligence.get("trade_grade", "N/A")}
Confidence: {intelligence.get("confidence", "N/A")}

Why Athena Thinks This:
{reasons}

Strategy:
{intelligence.get("strategy", "No strategy available.")}

Forecast:
{intelligence.get("forecast", "No forecast available.")}
"""