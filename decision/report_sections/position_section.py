"""
Athena Position Report Section
"""


def build_position_section(position):

    report = []

    report.append("")
    report.append("=======================================================")
    report.append("ATHENA POSITION MANAGER")
    report.append("=======================================================")
    report.append("")

    report.append(f"Status: {position.get('status', 'UNKNOWN')}")
    report.append(f"Symbol: {position.get('symbol', 'None')}")
    report.append(f"Direction: {position.get('direction', 'None')}")
    report.append(f"Type: {position.get('type', 'None')}")
    report.append(f"Quantity: {position.get('quantity', 0)}")
    report.append(f"Entry Price: {position.get('entry_price', 0)}")
    report.append(f"Current Price: {position.get('current_price', 0)}")
    report.append(
        f"Unrealized P/L: ${position.get('unrealized_pl', 0)}"
    )
    report.append(
        f"Unrealized P/L %: {position.get('unrealized_pl_percent', 0)}%"
    )

    report.append("")
    report.append("Summary:")
    report.append(position.get("summary", ""))
    report.append("")
    report.append("=======================================================")

    return "\n".join(report)