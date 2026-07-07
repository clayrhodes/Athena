"""
Athena Report Manager

Central report coordinator.
"""

from decision.report_data import build_report_data
from decision.report_builder import build_report

from logs.logger import save_report


def build_and_save_report(
    executive_summary,
    market_intelligence,
    intelligence,
    narrative,
    market_story,
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
    adaptive_confidence,
    forecast,
    trend,
    trade,
    market,
):

    sections = build_report_data(
        executive_summary=executive_summary,
        market_intelligence=market_intelligence,
        intelligence=intelligence,
        narrative=narrative,
        market_story=market_story,
        news=news,
        economic_calendar=economic_calendar,
        decision_matrix=decision_matrix,
        conviction=conviction,
        risk=risk,
        checklist=checklist,
        probability=probability,
        market_regime=market_regime,
        institutional=institutional,
        institutional_thesis=institutional_thesis,
        adaptive_confidence=adaptive_confidence,
        forecast=forecast,
        trend=trend,
        trade=trade,
        market=market,
    )

    report = build_report(sections)

    print(report)

    save_report(report)

    return report