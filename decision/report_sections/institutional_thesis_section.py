"""
Athena Institutional Thesis Report Section
"""


def build_institutional_thesis_section(thesis):

    report = []

    report.append("")
    report.append("=======================================================")
    report.append("ATHENA INSTITUTIONAL THESIS")
    report.append("=======================================================")
    report.append("")

    report.append(f"Market Regime: {thesis.get('regime', 'Unknown')}")
    report.append(f"Institutional Bias: {thesis.get('institutional_bias', 'Unknown')}")
    report.append(f"Forecast: {thesis.get('forecast', 'Unknown')}")
    report.append(f"Primary Scenario: {thesis.get('primary_scenario', 'Unknown')}")
    report.append("")

    report.append(f"Confidence: {thesis.get('confidence', 0)}%")
    report.append(f"Conviction: {thesis.get('conviction', 'Unknown')}")
    report.append(f"Trade Grade: {thesis.get('trade_grade', 'N/A')}")
    report.append("")

    report.append("Summary:")
    report.append(thesis.get("summary", "No summary available."))

    report.append("")
    report.append("=======================================================")

    return "\n".join(report)