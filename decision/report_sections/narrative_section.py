"""
Athena Narrative Report Section
"""


def build_narrative_section(narrative):

    report = []

    report.append("")
    report.append("=======================================================")
    report.append("ATHENA MARKET NARRATIVE")
    report.append("=======================================================")
    report.append("")
    report.append(narrative.get("summary", "No narrative available."))
    report.append("")
    report.append("=======================================================")

    return "\n".join(report)