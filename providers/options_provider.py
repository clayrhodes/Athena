"""
Athena Options Provider V1

Purpose:
Provides normalized options flow data for Athena.

Supports:
- Offline mode
- Manual JSON testing
- Future live API integration
"""

import json
from pathlib import Path


OPTIONS_FILE = Path("data/options_flow.json")


def _offline(message):
    return {
        "connected": False,
        "provider": "Athena Options Provider V1",
        "status": "OFFLINE",
        "message": message,
        "trades": [],
    }


def get_options_flow():

    if OPTIONS_FILE.exists():

        try:

            with open(OPTIONS_FILE, "r") as file:
                data = json.load(file)

            return {
                "connected": True,
                "provider": "Manual Options Flow",
                "status": "ACTIVE",
                "message": "Loaded from options_flow.json",
                "trades": data.get("trades", []),
            }

        except Exception as e:
            return _offline(str(e))

    return _offline("options_flow.json not found")