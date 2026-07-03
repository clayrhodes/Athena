def calculate_sma(data, period):
    return data["Close"].rolling(period).mean().iloc[-1]