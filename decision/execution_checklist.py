from decision.decision_matrix import evaluate_decision_matrix


def build_execution_checklist(scores, forecast, probability, buy_decision):
    matrix = evaluate_decision_matrix(scores)

    checks = []

    for row in matrix.get("rows", []):
        checks.append({
            "name": row.get("label", "Unknown Check"),
            "passed": row.get("passed", False),
            "score": row.get("score", "N/A"),
            "minimum": row.get("minimum", "N/A"),
            "weight": row.get("weight", "N/A"),
        })

    return {
        "checks": checks,
        "passed": len(matrix.get("passed", [])),
        "total": len(matrix.get("rows", [])),
        "recommendation": matrix.get("action", "NO TRADE"),
        "readiness": matrix.get("readiness", 0),
    }