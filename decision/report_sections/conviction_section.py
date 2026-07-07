def format_reason_list(reasons):
    if not reasons:
        return "None"

    return "\n".join(f"- {reason}" for reason in reasons)


def build_conviction_section(conviction):
    strengths = format_reason_list(
        conviction.get("strengths", [])
    )

    warnings = format_reason_list(
        conviction.get("warnings", [])
    )

    return f"""
CONVICTION ENGINE:
Conviction Score: {conviction.get("conviction", "N/A")}
Verdict: {conviction.get("verdict", "Unknown")}
Recommended Action: {conviction.get("action", "Unknown")}

Strengths:
{strengths}

Warnings:
{warnings}
"""