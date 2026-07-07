"""
Athena History Engine V1

Purpose:
Read Athena's historical memory records and provide
basic statistics for future analysis.

V1 focuses on loading and summarizing saved records.
"""

from memory.trade_database import load_memory_records


def get_history():
    """
    Returns every saved Athena memory record.
    """
    return load_memory_records()


def get_history_count():
    """
    Returns the number of saved analyses.
    """
    return len(get_history())


def get_latest_record():
    """
    Returns the newest saved record.
    """
    history = get_history()

    if not history:
        return None

    return history[-1]


def build_history_summary():
    """
    Returns a simple history summary.
    """

    history = get_history()

    summary = {
        "total_records": len(history),
        "latest_record": get_latest_record(),
    }

    return summary


def format_history_summary(summary):
    """
    Converts the history summary into readable text.
    """

    latest = summary.get("latest_record")

    lines = []

    lines.append("ATHENA HISTORY")
    lines.append("-" * 30)
    lines.append(f"Total Analyses: {summary.get('total_records', 0)}")

    if latest:
        lines.append("")
        lines.append("Latest Analysis")
        lines.append(f"Ticker: {latest.get('ticker', 'Unknown')}")
        lines.append(f"Timestamp: {latest.get('timestamp', 'Unknown')}")
        lines.append(f"Decision: {latest.get('decision', 'Unknown')}")
        lines.append(f"Overall Score: {latest.get('overall_score', 'Unknown')}")
        lines.append(f"Trade Grade: {latest.get('trade_grade', 'Unknown')}")
    else:
        lines.append("")
        lines.append("No history has been saved yet.")

    return "\n".join(lines)