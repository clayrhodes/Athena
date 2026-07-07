from decision.decision_matrix import evaluate_decision_matrix


def build_conviction_engine(scores, forecast, probability):
    matrix = evaluate_decision_matrix(scores)

    conviction = matrix.get("readiness", 0)
    action = matrix.get("action", "NO TRADE")

    strengths = []
    warnings = []

    for row in matrix.get("rows", []):
        label = row.get("label", "Unknown")
        score = row.get("score", 0)
        minimum = row.get("minimum", 0)

        if row.get("passed", False):
            strengths.append(f"{label} supports the setup with a score of {score}.")
        else:
            warnings.append(f"{label} needs improvement. Score {score}, required {minimum}.")

    if conviction >= 90:
        verdict = "HIGH CONVICTION"
    elif conviction >= 80:
        verdict = "GOOD CONVICTION"
    elif conviction >= 70:
        verdict = "MEDIUM CONVICTION"
    else:
        verdict = "LOW CONVICTION"

    return {
        "conviction": conviction,
        "verdict": verdict,
        "action": action,
        "strengths": strengths,
        "warnings": warnings,
    }