"""
Athena Provider Manager V3

Purpose:
Central hub for all external data providers.
"""

from providers.economic_provider import EconomicProvider
from providers.news_provider import NewsProvider
from providers.market_provider import MarketProvider
from providers.breadth_provider import get_market_breadth
from providers.options_provider import get_options_flow


class ProviderManager:

    def __init__(self):

        self.market = MarketProvider()
        self.news = NewsProvider()
        self.economic = EconomicProvider()

    def get_market_data(self):
        return self.market.get_market_data()

    def get_news(self):
        return self.news.get_news()

    def get_calendar(self):
        return self.economic.get_calendar()

    def get_market_breadth(self):
        return get_market_breadth()

    def get_options_flow(self):
        return get_options_flow()

    def get_system_status(self):

        return {
            "market": self.market.status(),
            "news": self.news.status(),
            "economic": self.economic.status(),
            "breadth": self.get_market_breadth().get("status", "UNKNOWN"),
            "options_flow": self.get_options_flow().get("status", "UNKNOWN"),
        }