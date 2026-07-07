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

    evidence = smart_money.get("evidence", [])

    if evidence:
        for item in evidence:
            report.append(f"- {item}")
    else:
        report.append("- No strong smart money evidence detected yet.")

    report.append("")
    report.append("Summary:")
    report.append(smart_money.get("summary", "No smart money summary available."))
    report.append("")
    report.append("=======================================================")

    return "\n".join(report)