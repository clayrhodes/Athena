"""
Athena Report Data Builder
"""


def build_report_data(
    executive_summary,
    market_intelligence,
    intelligence,
    narrative,
    news,
    economic_calendar,
    decision_matrix,
    conviction,
    risk,
    checklist,
    probability,
    market_regime,
    institutional,
    institutional_thesis,
    forecast,
    trend,
    trade,
    market,
):

    return {
        "executive_summary": executive_summary,
        "market_intelligence": market_intelligence,
        "intelligence": intelligence,
        "narrative": narrative,
        "news": news,
        "economic_calendar": economic_calendar,
        "decision_matrix": decision_matrix,
        "conviction": conviction,
        "risk": risk,
        "checklist": checklist,
        "probability": probability,
        "market_regime": market_regime,
        "institutional": institutional,
        "institutional_thesis": institutional_thesis,
        "forecast": forecast,
        "trend": trend,
        "trade": trade,
        "market": market,
    }