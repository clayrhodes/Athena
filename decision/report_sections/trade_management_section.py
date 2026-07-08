"""
Athena Trade Management Report Section
"""


def build_trade_management_section(trade_management):

    report = []

    report.append("")
    report.append("=======================================================")
    report.append("ATHENA TRADE MANAGEMENT")
    report.append("=======================================================")
    report.append("")

    report.append(
        f"Trade Thesis Score: {trade_management.get('thesis_score', 0)}/100"
    )
    report.append(f"Status: {trade_management.get('status', 'UNKNOWN')}")
    report.append(f"Recommended Action: {trade_management.get('action', 'UNKNOWN')}")
    report.append("")

    report.append("Positive Signals:")

    signals = trade_management.get("signals", [])

    if signals:
        for signal in signals:
            report.append(f"- {signal}")
    else:
        report.append("- None")

    report.append("")
    report.append("Warnings:")

    warnings = trade_management.get("warnings", [])

    if warnings:
        for warning in warnings:
            report.append(f"- {warning}")
    else:
        report.append("- None")

    report.append("")
    report.append("Exit Reasons:")

    exits = trade_management.get("exit_reasons", [])

    if exits:
        for reason in exits:
            report.append(f"- {reason}")
    else:
        report.append("- None")

    report.append("")
    report.append("Summary:")
    report.append(trade_management.get("summary", ""))
    report.append("")
    report.append("=======================================================")

    return "\n".join(report)