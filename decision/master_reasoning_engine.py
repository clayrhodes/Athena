"""
Athena Master Reasoning Engine V1

Combines Athena's reasoning engines into
one unified decision context.
"""

from decision.reasoning_engine import build_reasoning
from decision.memory_similarity_engine import (
    build_similarity_report,
)
from decision.adaptive_confidence_engine import (
    build_adaptive_confidence,
)


def build_master_reasoning(
    thesis,
    market_regime,
    institutional,
    probability,
    decision_matrix,
):

    reasoning = build_reasoning(
        thesis=thesis,
        market_regime=market_regime,
        institutional=institutional,
        probability=probability,
        decision_matrix=decision_matrix,
    )

    similarity = build_similarity_report(
        thesis=thesis,
        probability=probability,
    )

    adaptive = build_adaptive_confidence(
        thesis,
        similarity,
    )

    return {
        "reasoning": reasoning,
        "similarity": similarity,
        "adaptive_confidence": adaptive,
    }