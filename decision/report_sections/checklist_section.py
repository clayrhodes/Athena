def build_checklist_section(checklist):
    """
    Athena Execution Checklist Report Section
    """

    checks = checklist.get("checks", [])

    if not checks:
        checklist_lines = "No checklist items found."
    else:
        lines = []

        for check in checks:
            symbol = "PASS" if check.get("passed", False) else "FAIL"

            lines.append(
                f"{symbol}: {check.get('name', 'Unknown Check')}"
            )

        checklist_lines = "\n".join(lines)

    return f"""
EXECUTION CHECKLIST:
{checklist_lines}

Checklist Result:
{checklist.get("recommendation", "N/A")}

Checks Passed:
{checklist.get("passed", "N/A")} / {checklist.get("total", "N/A")}
"""