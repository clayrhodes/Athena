"""
Athena Liquidity Report Section
"""


def build_liquidity_section(liquidity):

    report = []

    report.append("")
    report.append("=======================================================")
    report.append("ATHENA LIQUIDITY")
    report.append("=======================================================")
    report.append("")

    report.append(
        f"Liquidity Score: {liquidity.get('score', 0)}/100"
    )

    report.append(
        f"Condition: {liquidity.get('condition', 'UNKNOWN')}"
    )

    report.append("")
    report.append("Evidence:")

    evidence = liquidity.get("evidence", [])

    if evidence:
        for item in evidence:
            report.append(f"- {item}")
    else:
        report.append("- No liquidity evidence available.")

    report.append("")
    report.append("Summary:")
    report.append(
        liquidity.get(
            "summary",
            "No liquidity summary available.",
        )
    )

    report.append("")
    report.append("=======================================================")

    return "\n".join(report)