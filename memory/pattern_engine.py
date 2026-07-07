"""
Athena Pattern Recognition Engine V2

Purpose:
Analyze Athena's historical memory records and provide
basic statistics plus early historical similarity intelligence.
"""

from memory.trade_database import load_memory_records


def _safe_number(value, default=0):
    if isinstance(value, (int, float)):
        return value
    return default


def _get_nested(record, keys, default=None):
    current = record

    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)

    if current is None:
        return default

    return current


def _calculate_similarity(current_record, past_record):
    """
    Compares the current market setup to a past saved setup.
    Returns a similarity score from 0 to 100.
    """

    score = 0
    max_score = 0

    comparison_rules = [
        ("market_environment.bias", 20),
        ("market_environment.trend", 20),
        ("market_environment.condition", 15),
        ("forecast.direction", 20),
        ("regime.regime", 15),
        ("should_buy", 10),
    ]

    for path, weight in comparison_rules:
        keys = path.split(".")

        if path == "should_buy":
            current_value = current_record.get("should_buy")
            past_value = past_record.get("should_buy")
        else:
            current_value = _get_nested(current_record, keys)
            past_value = _get_nested(past_record, keys)

        max_score += weight

        if current_value is not None and current_value == past_value:
            score += weight

    if max_score == 0:
        return 0

    return round((score / max_score) * 100, 2)


def analyze_patterns(current_record=None):
    """
    Reads all saved memory records and calculates
    statistics and similarity information.
    """

    records = load_memory_records()

    results = {
        "total_records": len(records),
        "buy_signals": 0,
        "wait_signals": 0,
        "average_score": 0,
        "average_confidence": 0,
        "similar_matches": [],
        "best_match_score": 0,
        "estimated_win_rate": 0,
        "quality": "NO REAL HISTORY FOUND YET",
    }

    if not records:
        return results

    total_score = 0
    total_confidence = 0

    for record in records:
        if record.get("should_buy"):
            results["buy_signals"] += 1
        else:
            results["wait_signals"] += 1

        total_score += _safe_number(record.get("overall_score", 0))
        total_confidence += _safe_number(
            record.get("forecast", {}).get("confidence", 0)
        )

    count = len(records)

    results["average_score"] = round(total_score / count, 2)
    results["average_confidence"] = round(total_confidence / count, 2)

    if current_record:
        matches = []

        for record in records:
            similarity = _calculate_similarity(current_record, record)

            if similarity >= 60:
                matches.append(
                    {
                        "similarity": similarity,
                        "should_buy": record.get("should_buy", False),
                        "overall_score": record.get("overall_score", 0),
                        "forecast_direction": record.get("forecast", {}).get(
                            "direction", "Unknown"
                        ),
                        "forecast_confidence": record.get("forecast", {}).get(
                            "confidence", 0
                        ),
                        "market_bias": record.get("market_environment", {}).get(
                            "bias", "Unknown"
                        ),
                        "market_trend": record.get("market_environment", {}).get(
                            "trend", "Unknown"
                        ),
                    }
                )

        matches = sorted(matches, key=lambda item: item["similarity"], reverse=True)

        results["similar_matches"] = matches[:5]

        if matches:
            results["best_match_score"] = matches[0]["similarity"]

            buy_matches = sum(1 for match in matches if match["should_buy"])
            results["estimated_win_rate"] = round((buy_matches / len(matches)) * 100, 2)

            if results["best_match_score"] >= 85:
                results["quality"] = "STRONG HISTORICAL MATCH"
            elif results["best_match_score"] >= 70:
                results["quality"] = "MODERATE HISTORICAL MATCH"
            else:
                results["quality"] = "WEAK HISTORICAL MATCH"

    return results


def format_pattern_report(results):
    lines = []

    lines.append("ATHENA PATTERN ENGINE")
    lines.append("-" * 30)

    lines.append(f"Analyses Stored: {results['total_records']}")
    lines.append(f"Buy Signals: {results['buy_signals']}")
    lines.append(f"Wait Signals: {results['wait_signals']}")
    lines.append(f"Average Overall Score: {results['average_score']}")
    lines.append(f"Average Forecast Confidence: {results['average_confidence']}")

    lines.append("")
    lines.append("Historical Similarity:")
    lines.append(f"Best Match Score: {results.get('best_match_score', 0)}%")
    lines.append(f"Estimated Win Rate: {results.get('estimated_win_rate', 0)}%")
    lines.append(f"Quality: {results.get('quality', 'UNKNOWN')}")

    matches = results.get("similar_matches", [])

    if matches:
        lines.append("")
        lines.append("Top Similar Setups:")

        for index, match in enumerate(matches, start=1):
            lines.append(
                f"{index}. Similarity {match['similarity']}% | "
                f"Bias: {match['market_bias']} | "
                f"Trend: {match['market_trend']} | "
                f"Forecast: {match['forecast_direction']} | "
                f"Confidence: {match['forecast_confidence']} | "
                f"Buy Signal: {match['should_buy']}"
            )
    else:
        lines.append("No similar historical setups found yet.")

    return "\n".join(lines)