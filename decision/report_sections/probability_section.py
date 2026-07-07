def format_reason_list(reasons):
    if not reasons:
        return "No probability reasons found."

    return "\n".join(f"- {reason}" for reason in reasons)


def build_probability_section(probability):
    probabilities = probability.get("probabilities", {})
    reasons = format_reason_list(probability.get("reasons", []))

    most_likely = probability.get("most_likely", "Unknown")
    most_likely = most_likely.replace("_", " ").title()

    return f"""
PROBABILITY ENGINE:
Bullish Continuation: {probabilities.get("bullish_continuation", "N/A")}%
Bearish Reversal: {probabilities.get("bearish_reversal", "N/A")}%
Range / Consolidation: {probabilities.get("range_consolidation", "N/A")}%
Pullback / Reversal Risk: {probabilities.get("pullback_reversal_risk", "N/A")}%

Most Likely Outcome:
{most_likely}

Probability Confidence:
{probability.get("confidence", "N/A")}%

Why Probability Engine Thinks This:
{reasons}
"""