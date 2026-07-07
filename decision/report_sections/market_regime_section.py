# decision/report_sections/market_regime_section.py

def build_market_regime_section(market_regime):
    if not market_regime:
        return """
MARKET REGIME:
Status: Not Available
Summary: Market Regime Engine has not returned data yet.
"""

    notes = market_regime.get("notes", [])

    section = f"""
MARKET REGIME:
Regime: {market_regime.get("regime", "Unknown")}
Confidence: {market_regime.get("confidence", 0)}%

Bull Score: {market_regime.get("bull_score", 0)}
Bear Score: {market_regime.get("bear_score", 0)}
Chop Score: {market_regime.get("chop_score", 0)}
Danger Score: {market_regime.get("danger_score", 0)}

Summary:
{market_regime.get("summary", "No market regime summary available.")}

Regime Evidence:
"""

    if notes:
        for note in notes:
            section += f"- {note}\n"
    else:
        section += "- No regime evidence available.\n"

    return section