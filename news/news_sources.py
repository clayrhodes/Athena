"""
Athena News Sources

Defines the news providers Athena will eventually use.

V1 is configuration only.
"""

NEWS_SOURCES = [
    {
        "name": "Federal Reserve",
        "enabled": True,
        "priority": 10,
    },
    {
        "name": "U.S. Treasury",
        "enabled": True,
        "priority": 9,
    },
    {
        "name": "Bureau of Labor Statistics",
        "enabled": True,
        "priority": 9,
    },
    {
        "name": "Bureau of Economic Analysis",
        "enabled": True,
        "priority": 9,
    },
    {
        "name": "Yahoo Finance",
        "enabled": True,
        "priority": 8,
    },
    {
        "name": "Reuters",
        "enabled": True,
        "priority": 8,
    },
    {
        "name": "Bloomberg",
        "enabled": True,
        "priority": 8,
    },
    {
        "name": "MarketWatch",
        "enabled": True,
        "priority": 7,
    },
    {
        "name": "CNBC",
        "enabled": True,
        "priority": 7,
    },
]