"""
Athena Calendar Events V1

Defines major market-moving economic events.

Future versions will pull this from a live economic calendar.
"""

HIGH_IMPACT_EVENTS = [
    "FOMC",
    "Federal Reserve",
    "Interest Rate Decision",
    "CPI",
    "Core CPI",
    "PPI",
    "Core PPI",
    "Nonfarm Payrolls",
    "Unemployment Rate",
    "GDP",
    "Powell Speech",
    "Jackson Hole",
    "PCE",
]

MEDIUM_IMPACT_EVENTS = [
    "Retail Sales",
    "PMI",
    "ISM Manufacturing",
    "Consumer Confidence",
    "Housing Starts",
    "Building Permits",
    "Existing Home Sales",
    "New Home Sales",
    "Treasury Auction",
]

LOW_IMPACT_EVENTS = [
    "Oil Inventories",
    "Natural Gas",
    "Wholesale Inventories",
]