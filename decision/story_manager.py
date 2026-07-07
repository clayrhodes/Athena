"""
Athena Story Manager

Builds Athena's complete market story.
"""

from decision.market_story_engine import build_market_story
from decision.narrative_engine import build_market_narrative


def build_story(
    thesis,
    market_regime,
    institutional,
    probability,
    decision_matrix,
):

    narrative = build_market_narrative(
        thesis,
        market_regime,
        institutional,
    )

    story = build_market_story(
        thesis,
        narrative,
        probability,
        decision_matrix,
    )

    return {
        "narrative": narrative,
        "story": story,
    }