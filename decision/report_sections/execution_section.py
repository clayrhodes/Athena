"""
Athena Execution Section

Formats the Execution Engine report.
"""


def build_execution_section(execution):
    report = []

    report.append("")
    report.append("=======================================================")
    report.append("ATHENA EXECUTION ENGINE")
    report.append("=======================================================")
    report.append("")

    report.append(f"Execution Readiness: {execution.get('score', 0)}/100")
    report.append(f"Status: {execution.get('status', 'UNKNOWN')}")
    report.append("")

    signals = execution.get("signals", [])
    waiting_for = execution.get("waiting_for", [])
    warnings = execution.get("warnings", [])

    report.append("Signals:")
    if signals:
        for signal in signals:
            report.append(f"- {signal}")
    else:
        report.append("- None")

    report.append("")
    report.append("Waiting For:")
    if waiting_for:
        for item in waiting_for:
            report.append(f"- {item}")
    else:
        report.append("- Nothing. Execution conditions are satisfied.")

    report.append("")
    report.append("Warnings:")
    if warnings:
        for warning in warnings:
            report.append(f"- {warning}")
    else:
        report.append("- None")

    report.append("")
    report.append(f"Summary: {execution.get('summary', 'No summary available.')}")
    report.append("")
    report.append("=======================================================")
    report.append("")

    return "\n".join(report)