def build_executive_summary(
    intelligence,
    decision_matrix,
    conviction,
    risk,
    probability,
    entry,
    trade_plan,
    buy_decision,
):
    probabilities = probability.get("probabilities", {})
    most_likely = probability.get("most_likely", "Unknown").replace("_", " ").title()

    hard_blocks = decision_matrix.get("hard_blocks", [])
    failed_items = decision_matrix.get("failed", [])

    main_wait_reasons = []

    if hard_blocks:
        main_wait_reasons.extend(hard_blocks)
    else:
        for item in failed_items:
            main_wait_reasons.append(
                f"{item.get('label', 'Unknown')} is {item.get('score', 'N/A')} and needs {item.get('minimum', 'N/A')}."
            )

    if not main_wait_reasons:
        wait_text = "No major wait reasons."
    else:
        wait_text = "\n".join([f"- {reason}" for reason in main_wait_reasons])

    return f"""
================ ATHENA EXECUTIVE SUMMARY ================

Final Action:
{intelligence.get("recommendation", "N/A")}

Decision Matrix:
{decision_matrix.get("readiness", "N/A")}% readiness

Conviction:
{conviction.get("verdict", "N/A")} ({conviction.get("conviction", "N/A")}%)

Risk:
{risk.get("recommendation", "N/A")} / {risk.get("risk_rating", "N/A")}

Most Likely Scenario:
{most_likely} ({probabilities.get("bullish_continuation", "N/A")}% bullish continuation)

Best Entry:
{entry.get("entry_price", "N/A")}

Stop:
{trade_plan.get("stop_loss", "N/A")}

Main Target:
{trade_plan.get("target_2", "N/A")}

Why Athena Is Waiting:
{wait_text}

==========================================================
"""