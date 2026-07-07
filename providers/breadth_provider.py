"""
Athena Breadth Provider V2

Purpose:
Provides normalized market breadth data to Athena.

Current support:
- Safe offline fallback
- Optional manual breadth file
- Ready for live provider connection later
"""

import json
from pathlib import Path


BREADTH_FILE = Path("data/market_breadth.json")


def _offline_response(message):
    return {
        "connected": False,
        "provider": "Athena Breadth Provider V2",
        "advancers": 0,
        "decliners": 0,
        "new_highs": 0,
        "new_lows": 0,
        "percent_above_20_sma": None,
        "percent_above_50_sma": None,
        "percent_above_200_sma": None,
        "status": "OFFLINE",
        "message": message,
    }


def _load_manual_breadth_file():
    if not BREADTH_FILE.exists():
        return None

    try:
        with open(BREADTH_FILE, "r") as file:
            data = json.load(file)

        return {
            "connected": True,
            "provider": "Manual Breadth File",
            "advancers": data.get("advancers", 0),
            "decliners": data.get("decliners", 0),
            "new_highs": data.get("new_highs", 0),
            "new_lows": data.get("new_lows", 0),
            "percent_above_20_sma": data.get("percent_above_20_sma"),
            "percent_above_50_sma": data.get("percent_above_50_sma"),
            "percent_above_200_sma": data.get("percent_above_200_sma"),
            "status": "LIVE",
            "message": "Market breadth loaded from local breadth file.",
        }

    except Exception as error:
        return _offline_response(
            f"Could not load manual breadth file: {error}"
        )


def get_market_breadth():
    """
    Returns normalized market breadth data.

    Athena expects:
    - advancers
    - decliners
    - new_highs
    - new_lows
    - percent_above_20_sma
    - percent_above_50_sma
    - percent_above_200_sma
    """

    manual_data = _load_manual_breadth_file()

    if manual_data:
        return manual_data

    return _offline_response(
        "No live breadth provider connected and no manual breadth file found."
    )