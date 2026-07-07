"""
Athena DataHub V2

Purpose:
Centralize all provider data into one object.

Adds:
- timestamps
- provider health
- safe collection wrappers
- centralized provider status
"""

from datetime import datetime

from providers.provider_manager import ProviderManager


class AthenaDataHub:

    def __init__(self):

        self.providers = ProviderManager()

    def _timestamp(self):
        return datetime.now().isoformat(timespec="seconds")

    def _safe_collect(self, name, collector):

        try:
            data = collector()

            return {
                "name": name,
                "connected": data.get("connected", False) if isinstance(data, dict) else True,
                "status": data.get("status", "ACTIVE") if isinstance(data, dict) else "ACTIVE",
                "provider": data.get("provider", name) if isinstance(data, dict) else name,
                "timestamp": self._timestamp(),
                "error": None,
                "data": data,
            }

        except Exception as error:
            return {
                "name": name,
                "connected": False,
                "status": "ERROR",
                "provider": name,
                "timestamp": self._timestamp(),
                "error": str(error),
                "data": {},
            }

    def collect(self):

        market = self._safe_collect(
            "market",
            self.providers.get_market_data,
        )

        news = self._safe_collect(
            "news",
            self.providers.get_news,
        )

        calendar = self._safe_collect(
            "calendar",
            self.providers.get_calendar,
        )

        breadth = self._safe_collect(
            "breadth",
            self.providers.get_market_breadth,
        )

        options_flow = self._safe_collect(
            "options_flow",
            self.providers.get_options_flow,
        )

        return {
            "market": market.get("data", {}),
            "news": news.get("data", {}),
            "calendar": calendar.get("data", {}),
            "breadth": breadth.get("data", {}),
            "options_flow": options_flow.get("data", {}),

            "meta": {
                "timestamp": self._timestamp(),
                "providers": {
                    "market": market,
                    "news": news,
                    "calendar": calendar,
                    "breadth": breadth,
                    "options_flow": options_flow,
                },
            },
        }

    def health_report(self):

        data = self.collect()
        providers = data.get("meta", {}).get("providers", {})

        return {
            name: {
                "connected": item.get("connected", False),
                "status": item.get("status", "UNKNOWN"),
                "provider": item.get("provider", name),
                "timestamp": item.get("timestamp"),
                "error": item.get("error"),
            }
            for name, item in providers.items()
        }