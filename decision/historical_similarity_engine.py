"""
Athena Historical Similarity Engine V2

Uses Athena's real saved trade/report history when available.
Safely falls back if no history exists yet.
"""

import json
import os
from pathlib import Path


HISTORY_LOCATIONS = [
    "memory/trade_history.json",
    "memory/history.json",
    "logs/trade_history.json",
    "logs/athena_history.json",
]


def _safe_number(value, default=0):
    try:
        return float(value)
    except Exception:
        return default


def _load_history():
    records = []

    for location in HISTORY_LOCATIONS:
        path = Path(location)

        if not path.exists():
            continue

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list):
                records.extend(data)

            elif isinstance(data, dict):
                if isinstance(data.get("trades"), list):
                    records.extend(data["trades"])
                elif isinstance(data.get("history"), list):
                    records.extend(data["history"])
                else:
                    records.append(data)

        except Exception:
            continue

    return records


def _score_similarity(current, past):
    score = 0

    current_action = current.get("action")
    past_action = past.get("action") or past.get("final_action")

    if current_action and past_action and current_action == past_action:
        score += 20

    current_regime = current.get("market_regime")
    past_regime = past.get("market_regime")

    if current_regime and past_regime and current_regime == past_regime:
        score += 25

    current_readiness = _safe_number(current.get("readiness"))
    past_readiness = _safe_number(past.get("readiness"))

    if abs(current_readiness - past_readiness) <= 10:
        score += 20

    current_confidence = _safe_number(current.get("confidence"))
    past_confidence = _safe_number(past.get("confidence"))

    if abs(current_confidence - past_confidence) <= 10:
        score += 20

    current_bull = _safe_number(current.get("bull_probability"))
    past_bull = _safe_number(past.get("bull_probability"))

    if abs(current_bull - past_bull) <= 10:
        score += 15

    return score


def _was_winner(record):
    result = str(record.get("result", "")).lower()
    outcome = str(record.get("outcome", "")).lower()

    if result in ["win", "winner", "profit", "green"]:
        return True

    if outcome in ["win", "winner", "profit", "green"]:
        return True

    pnl = record.get("pnl", record.get("profit_loss", None))

    if pnl is not None:
        return _safe_number(pnl) > 0

    return None


def build_historical_similarity_report(thesis, probability, decision_matrix):
    history = _load_history()

    readiness = decision_matrix.get("readiness", 0)
    action = decision_matrix.get("final_action") or decision_matrix.get("action")
    bull_probability = thesis.get("bull_probability", 0)
    confidence = thesis.get("confidence", 0)
    market_regime = thesis.get("market_regime", "UNKNOWN")

    current_snapshot = {
        "action": action,
        "readiness": readiness,
        "bull_probability": bull_probability,
        "confidence": confidence,
        "market_regime": market_regime,
    }

    scored_matches = []

    for record in history:
        if not isinstance(record, dict):
            continue

        similarity_score = _score_similarity(current_snapshot, record)

        if similarity_score >= 50:
            scored_matches.append({
                "record": record,
                "similarity_score": similarity_score,
                "winner": _was_winner(record),
            })

    scored_matches.sort(key=lambda item: item["similarity_score"], reverse=True)

    best_matches = scored_matches[:20]
    matches_found = len(best_matches)

    known_results = [
        match for match in best_matches
        if match["winner"] is not None
    ]

    if known_results:
        wins = sum(1 for match in known_results if match["winner"] is True)
        estimated_win_rate = round((wins / len(known_results)) * 100, 1)
    else:
        estimated_win_rate = 0

    if matches_found >= 10 and estimated_win_rate >= 65:
        quality = "STRONG HISTORICAL PROFILE"
    elif matches_found >= 5 and estimated_win_rate >= 55:
        quality = "MODERATE HISTORICAL PROFILE"
    elif matches_found > 0:
        quality = "WEAK HISTORICAL PROFILE"
    else:
        quality = "NO REAL HISTORY FOUND YET"

    if matches_found == 0:
        summary = (
            "Athena did not find enough real saved trade history yet. "
            "Historical similarity will improve as Athena records more trades."
        )
    elif estimated_win_rate == 0:
        summary = (
            f"Athena found {matches_found} similar historical conditions, "
            "but those records do not contain completed win/loss results yet."
        )
    else:
        summary = (
            f"Athena found {matches_found} similar historical conditions with "
            f"an estimated {estimated_win_rate}% historical win rate."
        )

    return {
        "matches_found": matches_found,
        "estimated_win_rate": estimated_win_rate,
        "quality": quality,
        "best_similarity_score": best_matches[0]["similarity_score"] if best_matches else 0,
        "history_records_checked": len(history),
        "summary": summary,
    }