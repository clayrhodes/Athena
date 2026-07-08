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
        print(f"Building section: {section_name}")

        section = sections.get(section_name)

        print(f"Exists? {section is not None}")

        if section:
            report.append(section)

    report.append(
        "======================================================="
    )

    return "\n\n".join(report)