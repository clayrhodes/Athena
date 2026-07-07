def build_decision_matrix_section(decision_matrix):
    rows = decision_matrix.get("rows", [])
    hard_blocks = decision_matrix.get("hard_blocks", [])

    if not rows:
        matrix_lines = "No decision matrix rows found."
    else:
        lines = []

        for row in rows:
            symbol = "PASS" if row.get("passed", False) else "FAIL"

            lines.append(
                f"{symbol}: {row.get('label', 'Unknown')} | "
                f"Score: {row.get('score', 'N/A')} | "
                f"Required: {row.get('minimum', 'N/A')} | "
                f"Weight: {row.get('weight', 'N/A')}%"
            )

        matrix_lines = "\n".join(lines)

    if hard_blocks:
        hard_block_text = "\n".join(f"- {item}" for item in hard_blocks)
    else:
        hard_block_text = "None"

    return f"""
DECISION MATRIX:
Readiness: {decision_matrix.get("readiness", "N/A")}%
Matrix Action: {decision_matrix.get("action", "N/A")}
Earned Weight: {decision_matrix.get("earned_weight", "N/A")} / {decision_matrix.get("total_weight", "N/A")}

{matrix_lines}

HARD BLOCKS:
{hard_block_text}
"""