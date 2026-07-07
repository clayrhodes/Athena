"""
Athena Economic Calendar Engine V4

Safe calendar engine.

Purpose:
- Prevent Finnhub 403 errors from making the report messy.
- Keep Athena stable even when calendar provider access is denied.
- Prepare structure for a better economic calendar provider later.
"""

from providers.economic_provider import EconomicProvider
from news.calendar_events import (
    HIGH_IMPACT_EVENTS,
    MEDIUM_IMPACT_EVENTS,
    LOW_IMPACT_EVENTS,
)


def classify_event(event_name):
    name = str(event_name).lower()

    for event in HIGH_IMPACT_EVENTS:
        if event.lower() in name:
            return "HIGH"

    for event in MEDIUM_IMPACT_EVENTS:
        if event.lower() in name:
            return "MEDIUM"

    for event in LOW_IMPACT_EVENTS:
        if event.lower() in name:
            return "LOW"

    return "UNKNOWN"


def get_economic_calendar():
    provider = EconomicProvider()

    try:
        calendar = provider.get_calendar()
    except Exception as error:
        calendar = {
            "connected": False,
            "events": [],
            "error": str(error),
        }

    raw_events = calendar.get("events", []) or []
    provider_error = calendar.get("error")

    events = []
    highest_impact = "NONE"
    high_impact_today = False

    for event in raw_events:
        impact = classify_event(event.get("name", ""))

        clean_event = {
            "time": event.get("time", "Unknown"),
            "country": event.get("country", "Unknown"),
            "name": event.get("name", "Unknown Event"),
            "impact": impact,
        }

        events.append(clean_event)

        if impact == "HIGH":
            highest_impact = "HIGH"
            high_impact_today = True
        elif impact == "MEDIUM" and highest_impact != "HIGH":
            highest_impact = "MEDIUM"
        elif impact == "LOW" and highest_impact == "NONE":
            highest_impact = "LOW"

    if provider_error:
        status = "OFFLINE"
        calendar_connected = False
        volatility_warning = "Economic calendar provider is currently unavailable."
        trade_recommendation = (
            "Do not rely on calendar data yet. Manually check for CPI, FOMC, "
            "jobs reports, Fed speakers, and major Treasury events before trading."
        )
        confidence = 20

    elif high_impact_today:
        status = "LIVE"
        calendar_connected = True
        volatility_warning = "High-impact economic event detected. Expect possible volatility."
        trade_recommendation = "Use caution. Avoid entering right before major economic releases."
        confidence = 85

    elif highest_impact == "MEDIUM":
        status = "LIVE"
        calendar_connected = True
        volatility_warning = "Medium-impact economic event detected."
        trade_recommendation = "Trade normally, but watch for volatility near release times."
        confidence = 70

    elif events:
        status = "LIVE"
        calendar_connected = True
        volatility_warning = "Low-impact or unknown economic events detected."
        trade_recommendation = "Calendar risk appears manageable."
        confidence = 60

    else:
        status = "OFFLINE" if not calendar.get("connected") else "LIVE"
        calendar_connected = calendar.get("connected", False)
        volatility_warning = "No economic events returned by calendar provider."
        trade_recommendation = "No calendar-based warning available."
        confidence = 30

    return {
        "engine": "Athena Economic Calendar Engine V4",
        "status": status,
        "calendar_connected": calendar_connected,
        "events_today": events,
        "high_impact_event_today": high_impact_today,
        "highest_impact_level": highest_impact,
        "volatility_warning": volatility_warning,
        "trade_recommendation": trade_recommendation,
        "confidence": confidence,
        "provider_error": provider_error,
    }


def format_economic_calendar_section(calendar_data):
    lines = []

    lines.append("ATHENA ECONOMIC CALENDAR")
    lines.append("-" * 30)

    lines.append(f"Engine: {calendar_data.get('engine')}")
    lines.append(f"Status: {calendar_data.get('status')}")
    lines.append(f"Calendar Connected: {calendar_data.get('calendar_connected')}")
    lines.append(f"High Impact Event Today: {calendar_data.get('high_impact_event_today')}")
    lines.append(f"Highest Impact Level: {calendar_data.get('highest_impact_level')}")
    lines.append(f"Confidence: {calendar_data.get('confidence')}%")

    lines.append("")
    lines.append("Events Today:")

    events = calendar_data.get("events_today", [])

    if events:
        for event in events[:10]:
            lines.append(
                f"- {event.get('time')} | {event.get('country')} | "
                f"{event.get('name')} | {event.get('impact')}"
            )
    else:
        lines.append("- None available")

    lines.append("")
    lines.append(calendar_data.get("volatility_warning", "No calendar warning available."))
    lines.append("")
    lines.append(calendar_data.get("trade_recommendation", "No calendar recommendation available."))

    return "\n".join(lines)


def build_economic_calendar_section():
    calendar = get_economic_calendar()
    return format_economic_calendar_section(calendar)