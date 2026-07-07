from decision.decision_matrix import evaluate_decision_matrix


def clean_reason_text(text):
    return str(text).strip().rstrip(".")


def format_list(items):
    if not items:
        return "None"

    cleaned_items = [clean_reason_text(item) for item in items]
    return "; ".join(cleaned_items)


def should_buy_now(scores, decision):
    matrix = evaluate_decision_matrix(scores)

    failed_rows = matrix.get("failed", [])
    passed_rows = matrix.get("passed", [])
    hard_blocks = matrix.get("hard_blocks", [])

    passed_checks = [row.get("label", "Unknown Check") for row in passed_rows]
    failed_checks = [row.get("label", "Unknown Check") for row in failed_rows]

    if hard_blocks:
        wait_for = hard_blocks
    else:
        wait_for = [
            f"{row.get('label', 'Unknown')} above {row.get('minimum', 'N/A')}"
            for row in failed_rows
        ]

    readiness = matrix.get("readiness", 0)
    matrix_action = matrix.get("action", "NO TRADE")

    if matrix_action == "BUY NOW":
        answer = "YES"
        action = "BUY NOW"
        should_buy = True
        reason = (
            f"Decision Matrix readiness is {readiness}%. "
            "Athena has enough confirmation for entry."
        )

    elif matrix_action == "WAIT FOR ENTRY":
        answer = "NO"
        action = "WAIT"
        should_buy = False
        reason = (
            f"Decision Matrix readiness is {readiness}%. "
            f"Setup is promising, but Athena is waiting because: {format_list(wait_for)}."
        )

    else:
        answer = "NO"
        action = "NO TRADE"
        should_buy = False
        reason = (
            f"Decision Matrix readiness is only {readiness}%. "
            f"Failed checks: {format_list(failed_checks)}."
        )

    return {
        "answer": answer,
        "action": action,
        "should_buy": should_buy,
        "buy_readiness": readiness,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "wait_for": wait_for,
        "hard_blocks": hard_blocks,
        "reason": reason,
    }