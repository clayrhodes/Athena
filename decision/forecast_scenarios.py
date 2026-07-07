from decision.scenario_probability import calculate_scenario_probabilities


def build_forecast_scenarios(forecast):
    """
    Athena Forecast Scenario Engine

    Builds multiple possible market outcomes using
    dynamically calculated probabilities.
    """

    probabilities = calculate_scenario_probabilities(forecast)

    direction = forecast["direction"]

    if direction == "Bullish Continuation":

        return {
            "primary": {
                "probability": probabilities["primary"],
                "description": "Trend continues higher."
            },
            "secondary": {
                "probability": probabilities["secondary"],
                "description": "Pullback before continuation."
            },
            "failure": {
                "probability": probabilities["failure"],
                "description": "Bullish thesis fails."
            }
        }

    elif direction == "Bearish Continuation":

        return {
            "primary": {
                "probability": probabilities["primary"],
                "description": "Trend continues lower."
            },
            "secondary": {
                "probability": probabilities["secondary"],
                "description": "Bounce before continuation."
            },
            "failure": {
                "probability": probabilities["failure"],
                "description": "Bearish thesis fails."
            }
        }

    elif direction == "Bullish":

        return {
            "primary": {
                "probability": probabilities["primary"],
                "description": "Bull trend continues."
            },
            "secondary": {
                "probability": probabilities["secondary"],
                "description": "Temporary pullback."
            },
            "failure": {
                "probability": probabilities["failure"],
                "description": "Trend reverses bearish."
            }
        }

    elif direction == "Bearish":

        return {
            "primary": {
                "probability": probabilities["primary"],
                "description": "Bear trend continues."
            },
            "secondary": {
                "probability": probabilities["secondary"],
                "description": "Short-term relief rally."
            },
            "failure": {
                "probability": probabilities["failure"],
                "description": "Bear trend fails."
            }
        }

    else:

        return {
            "primary": {
                "probability": probabilities["primary"],
                "description": "Range continues."
            },
            "secondary": {
                "probability": probabilities["secondary"],
                "description": "Breakout develops."
            },
            "failure": {
                "probability": probabilities["failure"],
                "description": "Market becomes unpredictable."
            }
        }
