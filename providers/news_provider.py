"""
Athena News Provider V2

Live Finnhub news provider.

This provider:
- Reads FINNHUB_API_KEY from .env
- Pulls live market news
- Pulls SPY-related company news
- Fails safely if the API key is missing or the API is down
"""

import os
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv


load_dotenv()


class NewsProvider:
    def __init__(self):
        self.api_key = os.getenv("FINNHUB_API_KEY")
        self.provider_name = "Finnhub Live News"
        self.base_url = "https://finnhub.io/api/v1"
        self.connected = bool(self.api_key)

    def status(self):
        return {
            "connected": self.connected,
            "provider": self.provider_name,
            "api_key_loaded": bool(self.api_key),
        }

    def _safe_get(self, endpoint, params=None):
        if not self.api_key:
            return {
                "success": False,
                "error": "Missing FINNHUB_API_KEY in .env",
                "data": [],
            }

        if params is None:
            params = {}

        params["token"] = self.api_key

        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                timeout=10,
            )
            response.raise_for_status()

            return {
                "success": True,
                "error": None,
                "data": response.json(),
            }

        except Exception as error:
            return {
                "success": False,
                "error": str(error),
                "data": [],
            }

    def get_market_news(self, category="general", limit=10):
        result = self._safe_get(
            "news",
            {
                "category": category,
            },
        )

        articles = result.get("data", [])

        if not result["success"]:
            return {
                "connected": False,
                "provider": self.provider_name,
                "category": category,
                "headlines": [],
                "articles": [],
                "error": result["error"],
            }

        cleaned_articles = self._clean_articles(articles, limit)

        return {
            "connected": True,
            "provider": self.provider_name,
            "category": category,
            "headlines": [article["headline"] for article in cleaned_articles],
            "articles": cleaned_articles,
            "error": None,
        }

    def get_company_news(self, symbol="SPY", days_back=7, limit=10):
        today = datetime.now().date()
        start_date = today - timedelta(days=days_back)

        result = self._safe_get(
            "company-news",
            {
                "symbol": symbol,
                "from": str(start_date),
                "to": str(today),
            },
        )

        articles = result.get("data", [])

        if not result["success"]:
            return {
                "connected": False,
                "provider": self.provider_name,
                "symbol": symbol,
                "headlines": [],
                "articles": [],
                "error": result["error"],
            }

        cleaned_articles = self._clean_articles(articles, limit)

        return {
            "connected": True,
            "provider": self.provider_name,
            "symbol": symbol,
            "headlines": [article["headline"] for article in cleaned_articles],
            "articles": cleaned_articles,
            "error": None,
        }

    def get_news(self, symbol="SPY", limit=10):
        market_news = self.get_market_news(limit=limit)
        company_news = self.get_company_news(symbol=symbol, limit=limit)

        headlines = []
        articles = []
        errors = []

        if market_news.get("headlines"):
            headlines.extend(market_news["headlines"])

        if company_news.get("headlines"):
            headlines.extend(company_news["headlines"])

        if market_news.get("articles"):
            articles.extend(market_news["articles"])

        if company_news.get("articles"):
            articles.extend(company_news["articles"])

        if market_news.get("error"):
            errors.append(market_news["error"])

        if company_news.get("error"):
            errors.append(company_news["error"])

        cleaned_headlines = []
        seen = set()

        for headline in headlines:
            if headline and headline not in seen:
                cleaned_headlines.append(headline)
                seen.add(headline)

        return {
            "connected": bool(cleaned_headlines),
            "provider": self.provider_name,
            "symbol": symbol,
            "headline_count": len(cleaned_headlines),
            "headlines": cleaned_headlines[:limit],
            "articles": articles[:limit],
            "errors": errors,
        }

    def _clean_articles(self, articles, limit):
        cleaned = []

        for article in articles[:limit]:
            headline = article.get("headline") or article.get("summary") or "No headline"

            cleaned.append(
                {
                    "headline": headline,
                    "source": article.get("source", "Unknown"),
                    "summary": article.get("summary", ""),
                    "url": article.get("url", ""),
                    "datetime": article.get("datetime"),
                    "category": article.get("category", ""),
                    "image": article.get("image", ""),
                }
            )

        return cleaned