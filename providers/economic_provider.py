"""
Athena Economic Provider V3

Provides:
- FRED macroeconomic data
- Finnhub live economic calendar
"""

import os
import requests
from dotenv import load_dotenv


load_dotenv()


class EconomicProvider:

    def __init__(self):
        self.fred_api_key = os.getenv("FRED_API_KEY")
        self.finnhub_api_key = os.getenv("FINNHUB_API_KEY")

        self.connected = bool(self.fred_api_key or self.finnhub_api_key)
        self.provider_name = "FRED + Finnhub Economic Provider"

        self.fred_url = "https://api.stlouisfed.org/fred/series/observations"
        self.finnhub_url = "https://finnhub.io/api/v1/calendar/economic"

    def status(self):
        return {
            "connected": self.connected,
            "provider": self.provider_name,
            "fred_api_key_loaded": bool(self.fred_api_key),
            "finnhub_api_key_loaded": bool(self.finnhub_api_key),
        }

    def _get_series_latest(self, series_id):
        if not self.fred_api_key:
            return None

        try:
            params = {
                "series_id": series_id,
                "api_key": self.fred_api_key,
                "file_type": "json",
                "sort_order": "desc",
                "limit": 1,
            }

            response = requests.get(self.fred_url, params=params, timeout=10)
            response.raise_for_status()

            observations = response.json().get("observations", [])

            if not observations:
                return None

            latest = observations[0]
            value = latest.get("value")

            if value == ".":
                return None

            return {
                "series_id": series_id,
                "date": latest.get("date"),
                "value": float(value),
            }

        except Exception:
            return None

    def get_macro_data(self):
        data = {
            "fed_funds_rate": self._get_series_latest("FEDFUNDS"),
            "cpi": self._get_series_latest("CPIAUCSL"),
            "unemployment_rate": self._get_series_latest("UNRATE"),
            "nonfarm_payrolls": self._get_series_latest("PAYEMS"),
            "consumer_sentiment": self._get_series_latest("UMCSENT"),
            "yield_curve_10y_2y": self._get_series_latest("T10Y2Y"),
        }

        connected_items = {
            key: value
            for key, value in data.items()
            if value is not None
        }

        return {
            "connected": bool(connected_items),
            "provider": self.provider_name,
            "data": data,
        }

    def get_calendar(self):
        if not self.finnhub_api_key:
            return {
                "connected": False,
                "provider": self.provider_name,
                "events": [],
                "error": "Missing FINNHUB_API_KEY",
            }

        try:
            params = {
                "token": self.finnhub_api_key,
            }

            response = requests.get(
                self.finnhub_url,
                params=params,
                timeout=10,
            )

            response.raise_for_status()
            data = response.json()

            events = data.get("economicCalendar", [])

            cleaned_events = []

            for event in events:
                cleaned_events.append(
                    {
                        "time": event.get("time", "Unknown"),
                        "country": event.get("country", "Unknown"),
                        "name": event.get("event", "Unknown Event"),
                        "actual": event.get("actual"),
                        "estimate": event.get("estimate"),
                        "previous": event.get("prev"),
                        "unit": event.get("unit", ""),
                    }
                )

            return {
                "connected": True,
                "provider": self.provider_name,
                "events": cleaned_events,
                "error": None,
            }

        except Exception as error:
            return {
                "connected": False,
                "provider": self.provider_name,
                "events": [],
                "error": str(error),
            }