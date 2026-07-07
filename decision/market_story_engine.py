"""
Athena Market Story Engine V1

Creates Athena's final market story by combining
the outputs from every major intelligence engine.
"""


def build_market_story(
    thesis,
    narrative,
    probability,
    decision_matrix,
):

    story = []

    story.append(narrative.get(
        "summary",
        "No market narrative available.",
    ))

    story.append("")

    story.append(
        f"Most likely scenario: "
        f"{probability.get('most_likely', 'Unknown')}."
    )

    story.append(
        f"Decision Matrix readiness: "
        f"{decision_matrix.get('readiness', 0)}%."
    )

    if thesis.get("validated"):

        story.append(
            "Institutional thesis supports the current market bias."
        )

    else:

        story.append(
            "Institutional thesis requires additional confirmation."
        )

    return {
        "summary": " ".join(story)
    }