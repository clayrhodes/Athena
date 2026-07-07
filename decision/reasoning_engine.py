"""
Athena Reasoning Engine V1

Central reasoning layer for Athena.
"""


from decision.story_manager import build_story


def build_reasoning(
    thesis,
    market_regime,
    institutional,
    probability,
    decision_matrix,
):

    story_data = build_story(
        thesis=thesis,
        market_regime=market_regime,
        institutional=institutional,
        probability=probability,
        decision_matrix=decision_matrix,
    )

    return {
        "story": story_data["story"],
        "narrative": story_data["narrative"],
        "thesis": thesis,
    }