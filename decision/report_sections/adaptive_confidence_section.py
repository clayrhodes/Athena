"""
Athena Adaptive Confidence Report Section
"""


def build_adaptive_confidence_section(confidence):

    report = []

    report.append("")
    report.append("=======================================================")
    report.append("ATHENA ADAPTIVE CONFIDENCE")
    report.append("=======================================================")
    report.append("")

    report.append(
        f"Confidence: {confidence.get('confidence', 0)}%"
    )

    report.append(
        f"Rating: {confidence.get('rating', 'Unknown')}"
    )

    report.append("")
    report.append("=======================================================")

    return "\n".join(report)