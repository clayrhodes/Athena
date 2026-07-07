"""
Athena Historical Similarity Report Section V2
"""


def build_historical_similarity_section(similarity):

    report = []

    matches = similarity.get("similar_matches", [])
    matches_found = len(matches)

    report.append("")
    report.append("=======================================================")
    report.append("ATHENA HISTORICAL SIMILARITY")
    report.append("=======================================================")
    report.append("")

    report.append(f"Matches Found: {matches_found}")
    report.append(f"Best Match Score: {similarity.get('best_match_score', 0)}%")
    report.append(f"Estimated Win Rate: {similarity.get('estimated_win_rate', 0)}%")
    report.append(f"Quality: {similarity.get('quality', 'UNKNOWN')}")
    report.append("")

    if matches:
        report.append("Top Similar Setups:")

        for index, match in enumerate(matches, start=1):
            report.append(
                f"{index}. Similarity {match.get('similarity', 0)}% | "
                f"Bias: {match.get('market_bias', 'Unknown')} | "
                f"Trend: {match.get('market_trend', 'Unknown')} | "
                f"Forecast: {match.get('forecast_direction', 'Unknown')} | "
                f"Confidence: {match.get('forecast_confidence', 0)} | "
                f"Buy Signal: {match.get('should_buy', False)}"
            )

        report.append("")
        report.append("Summary:")
        report.append(
            "Athena found similar historical setups and is using them as supporting context."
        )
    else:
        report.append("Summary:")
        report.append(
            "Athena did not find enough similar saved market setups yet. "
            "Historical similarity will improve as Athena records more completed analyses."
        )

    report.append("")
    report.append("=======================================================")

    return "\n".join(report)