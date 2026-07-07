def build_forecast_section(environment, forecast):
    return f"""
MARKET ENVIRONMENT:
Bias: {environment.get("bias", "Unknown")}
Trend: {environment.get("trend", "Unknown")}
Condition: {environment.get("condition", "Unknown")}
Strategy: {environment.get("strategy", "No strategy available")}

FORECAST:
Direction: {forecast.get("direction", "Unknown")}
Confidence: {forecast.get("confidence", "Unknown")}
Summary: {forecast.get("summary", "No forecast summary available")}
"""