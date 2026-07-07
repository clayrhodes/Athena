"""
Athena Market Story Header
"""


def build_market_story_header(story):

    report = []

    report.append("")
    report.append("=======================================================")
    report.append("ATHENA MARKET STORY")
    report.append("=======================================================")
    report.append("")

    report.append(
        story.get(
            "summary",
            "No market story available.",
        )
    )

    report.append("")
    report.append("=======================================================")

    return "\n".join(report)