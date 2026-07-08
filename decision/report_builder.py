"""
Athena Report Builder
"""


def build_report(sections):

    order = [
        "executive_summary",
        "market_story",
        "market_intelligence",
        "intelligence",
        "narrative",
        "historical_similarity",
        "smart_money",
        "liquidity",
        "market_breadth",
        "news",
        "economic_calendar",
        "decision_matrix",
        "conviction",
        "risk",
        "execution",
        "portfolio",
        "position",
        "trade_management",
        "checklist",
        "probability",
        "market_regime",
        "institutional",
        "institutional_thesis",
        "forecast",
        "trend",
        "trade",
        "market",
    ]

    report = []

    for section_name in order:
        section = sections.get(section_name)

        if section:
            report.append(section)

    report.append(
        "======================================================="
    )

    return "\n\n".join(report)