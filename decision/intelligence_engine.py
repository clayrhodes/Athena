from decision.decision_matrix import evaluate_decision_matrix


def build_intelligence_report(scores, forecast, decision, buy_decision, entry, trade_plan):
    matrix = evaluate_decision_matrix(scores)

    overall = scores.get("overall_score", 0)
    grade = scores.get("trade_grade", "N/A")
    confidence = scores.get("confidence", "Unknown")

    reasons = []

    for row in matrix.get("passed", []):
        reasons.append(
            f"{row.get('label', 'Unknown')} passed with a score of {row.get('score', 'N/A')}."
        )

    warnings = []

    for row in matrix.get("failed", []):
        warnings.append(
            f"{row.get('label', 'Unknown')} failed with a score of {row.get('score', 'N/A')}."
        )

    environment = scores.get("environment", {})
    strategy = environment.get("strategy", "Wait for confirmation.")

    matrix_action = matrix.get("action", "NO TRADE")

    if matrix_action == "BUY NOW":
        recommendation = "BUY"
    elif matrix_action == "WAIT FOR ENTRY":
        recommendation = "WATCH FOR ENTRY"
    else:
        recommendation = "DO NOT TRADE"

    return {
        "overall_score": overall,
        "trade_grade": grade,
        "confidence": confidence,
        "recommendation": recommendation,
        "strategy": strategy,
        "forecast": forecast.get("summary", "No forecast available."),
        "reasons": reasons,
        "warnings": warnings,
        "entry_price": entry.get("entry_price", "N/A"),
        "stop_loss": trade_plan.get("stop_loss", "N/A"),
        "target_1": trade_plan.get("target_1", "N/A"),
        "target_2": trade_plan.get("target_2", "N/A"),
    }