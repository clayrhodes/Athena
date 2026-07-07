def build_institutional_section(institutional):

    score = institutional.get("institutional_score", 0)
    bias = institutional.get("institutional_bias", "Unknown")
    confidence = institutional.get("institutional_confidence", "Unknown")
    reasons = institutional.get("institutional_reasons", [])

    report = "\n"
    report += "=======================================================\n"
    report += "ATHENA INSTITUTIONAL INTELLIGENCE\n"
    report += "=======================================================\n\n"

    report += f"Institutional Score: {score}/100\n"
    report += f"Institutional Bias: {bias}\n"
    report += f"Confidence: {confidence}\n\n"

    report += "Evidence:\n"

    if reasons:
        for reason in reasons:
            report += f"- {reason}\n"
    else:
        report += "- No significant institutional signals detected.\n"

    report += "\n"

    return report