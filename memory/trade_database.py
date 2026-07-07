"""
Athena Trade Database V1

Purpose:
Save Athena memory records to disk as JSON files.

This is the first real step toward Athena remembering every setup.
"""

import json
import os
from datetime import datetime


MEMORY_DATABASE_FOLDER = os.path.join("memory", "database")


def ensure_database_folder():
    """
    Makes sure the memory database folder exists.
    """

    if not os.path.exists(MEMORY_DATABASE_FOLDER):
        os.makedirs(MEMORY_DATABASE_FOLDER)


def build_memory_filename(ticker="SPY"):
    """
    Builds a clean timestamped filename.
    """

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    return f"{ticker}_{timestamp}.json"


def save_memory_record(record):
    """
    Saves one Athena memory record as a JSON file.
    """

    ensure_database_folder()

    ticker = record.get("ticker", "SPY")
    filename = build_memory_filename(ticker)
    filepath = os.path.join(MEMORY_DATABASE_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(record, file, indent=4)

    return filepath


def load_memory_records():
    """
    Loads all saved memory records.

    V1 loads every JSON file inside memory/database.
    """

    ensure_database_folder()

    records = []

    for filename in os.listdir(MEMORY_DATABASE_FOLDER):
        if filename.endswith(".json"):
            filepath = os.path.join(MEMORY_DATABASE_FOLDER, filename)

            with open(filepath, "r", encoding="utf-8") as file:
                record = json.load(file)
                records.append(record)

    return records


def count_memory_records():
    """
    Counts how many memory records Athena has saved.
    """

    records = load_memory_records()
    return len(records)