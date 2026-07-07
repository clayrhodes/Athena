"""
Athena Options Flow Report Section
"""


def build_options_flow_section(options_flow):
    lines = []

    lines.append("=======================================================")
    lines.append("ATHENA OPTIONS FLOW")
    lines.append("-------------------------------------------------------")

    lines.append(
        f"Condition: {options_flow.get('condition', 'UNKNOWN')}"
    )

    lines.append(
        f"Score: {options_flow.get('score', 0)}/100"
    )

    lines.append(
        f"Call Premium: {options_flow.get('call_premium', 0)}"
    )

    lines.append(
        f"Put Premium: {options_flow.get('put_premium', 0)}"
    )

    lines.append(
        f"Bullish Premium: {options_flow.get('bullish_premium', 0)}"
    )

    lines.append(
        f"Bearish Premium: {options_flow.get('bearish_premium', 0)}"
    )

    lines.append(
        f"Sweeps: {options_flow.get('sweep_count', 0)}"
    )

    lines.append(
        f"Blocks: {options_flow.get('block_count', 0)}"
    )

    lines.append(
        f"Unusual Activity Count: {options_flow.get('unusual_count', 0)}"
    )

    lines.append("")

    if options_flow.get("signals"):
        lines.append("Signals:")
        for signal in options_flow.get("signals", []):
            lines.append(f"- {signal}")

    if options_flow.get("warnings"):
        lines.append("")
        lines.append("Warnings:")
        for warning in options_flow.get("warnings", []):
            lines.append(f"- {warning}")

    lines.append("")
    lines.append(
        options_flow.get(
            "summary",
            "No options flow summary available.",
        )
    )

    return "\n".join(lines)