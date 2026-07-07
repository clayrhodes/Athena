"""
Athena Integration Manager

Combines Athena's reasoning systems into one
structure for the report and future decision engines.
"""

from decision.master_reasoning_engine import (
    build_master_reasoning,
)


def build_integration(
    thesis,
    market_regime,
    institutional,
    probability,
    decision_matrix,
):

    master = build_master_reasoning(
        thesis=thesis,
        market_regime=market_regime,
        institutional=institutional,
        probability=probability,
        decision_matrix=decision_matrix,
    )

    return {
        "reasoning": master["reasoning"],
        "similarity": master["similarity"],
        "adaptive_confidence": master["adaptive_confidence"],
    }