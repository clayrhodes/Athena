"""
Athena Smart Money Report Section
"""


def build_smart_money_section(smart_money):

    report = []

    report.append("")
    report.append("=======================================================")
    report.append("ATHENA SMART MONEY")
    report.append("=======================================================")
    report.append("")

    report.append(f"Score: {smart_money.get('score', 0)}/100")
    report.append(f"Bias: {smart_money.get('bias', 'UNKNOWN')}")
    report.append("")

    report.append("Evidence:")

    signals = smart_money.get("signals", [])

    if signals:
        for signal in signals:
            report.append(f"- {signal}")
    else:
        report.append("- No strong smart money evidence detected yet.")

    warnings = smart_money.get("warnings", [])

    if warnings:
        report.append("")
        report.append("Warnings:")
        for warning in warnings:
            report.append(f"- {warning}")

    failed = smart_money.get("failed_reasons", [])

    if failed:
        report.append("")
        report.append("Waiting For:")
        for item in failed:
            report.append(f"- {item}")

    report.append("")
    report.append("Summary:")
    report.append(
        smart_money.get(
            "summary",
            "No smart money summary available."
        )
    )

    report.append("")
    report.append("=======================================================")

    return "\n".join(report)