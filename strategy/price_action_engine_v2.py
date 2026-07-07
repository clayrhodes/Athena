import pandas as pd


def normalize_columns(df):
    df = df.copy()
    df.columns = [str(col).lower() for col in df.columns]
    return df


def find_swing_highs_lows(df, lookback=2):
    df = normalize_columns(df)

    df["swing_high"] = False
    df["swing_low"] = False

    for i in range(lookback, len(df) - lookback):
        current_high = df["high"].iloc[i]
        current_low = df["low"].iloc[i]

        left_highs = df["high"].iloc[i - lookback:i]
        right_highs = df["high"].iloc[i + 1:i + lookback + 1]

        left_lows = df["low"].iloc[i - lookback:i]
        right_lows = df["low"].iloc[i + 1:i + lookback + 1]

        if current_high > left_highs.max() and current_high > right_highs.max():
            df.loc[df.index[i], "swing_high"] = True

        if current_low < left_lows.min() and current_low < right_lows.min():
            df.loc[df.index[i], "swing_low"] = True

    return df


def classify_market_structure(df):
    df = df.copy()
    df["structure_label"] = ""

    last_swing_high = None
    last_swing_low = None

    for i in range(len(df)):
        if df["swing_high"].iloc[i]:
            current_high = df["high"].iloc[i]

            if last_swing_high is None:
                df.loc[df.index[i], "structure_label"] = "FIRST_HIGH"
            elif current_high > last_swing_high:
                df.loc[df.index[i], "structure_label"] = "HH"
            else:
                df.loc[df.index[i], "structure_label"] = "LH"

            last_swing_high = current_high

        if df["swing_low"].iloc[i]:
            current_low = df["low"].iloc[i]

            if last_swing_low is None:
                df.loc[df.index[i], "structure_label"] = "FIRST_LOW"
            elif current_low > last_swing_low:
                df.loc[df.index[i], "structure_label"] = "HL"
            else:
                df.loc[df.index[i], "structure_label"] = "LL"

            last_swing_low = current_low

    return df


def detect_bos_choch(df):
    df = df.copy()

    df["bos"] = ""
    df["choch"] = ""

    recent_swing_high = None
    recent_swing_low = None
    trend_bias = "neutral"

    for i in range(len(df)):
        close = df["close"].iloc[i]

        if df["swing_high"].iloc[i]:
            recent_swing_high = df["high"].iloc[i]

        if df["swing_low"].iloc[i]:
            recent_swing_low = df["low"].iloc[i]

        if recent_swing_high is not None and close > recent_swing_high:
            if trend_bias == "bearish":
                df.loc[df.index[i], "choch"] = "BULLISH_CHOCH"
            else:
                df.loc[df.index[i], "bos"] = "BULLISH_BOS"
            trend_bias = "bullish"

        if recent_swing_low is not None and close < recent_swing_low:
            if trend_bias == "bullish":
                df.loc[df.index[i], "choch"] = "BEARISH_CHOCH"
            else:
                df.loc[df.index[i], "bos"] = "BEARISH_BOS"
            trend_bias = "bearish"

    return df


def calculate_price_action_score(df):
    recent = df.tail(30)

    bullish_points = 0
    bearish_points = 0

    bullish_points += (recent["structure_label"] == "HH").sum() * 10
    bullish_points += (recent["structure_label"] == "HL").sum() * 10
    bullish_points += (recent["bos"] == "BULLISH_BOS").sum() * 15
    bullish_points += (recent["choch"] == "BULLISH_CHOCH").sum() * 20

    bearish_points += (recent["structure_label"] == "LH").sum() * 10
    bearish_points += (recent["structure_label"] == "LL").sum() * 10
    bearish_points += (recent["bos"] == "BEARISH_BOS").sum() * 15
    bearish_points += (recent["choch"] == "BEARISH_CHOCH").sum() * 20

    raw_score = 50 + bullish_points - bearish_points
    score = max(0, min(100, raw_score))

    return score


def run_price_action_engine_v2(df):
    df = find_swing_highs_lows(df)
    df = classify_market_structure(df)
    df = detect_bos_choch(df)

    score = calculate_price_action_score(df)

    latest_labels = df.tail(30)["structure_label"].tolist()
    latest_bos = df.tail(30)["bos"].tolist()
    latest_choch = df.tail(30)["choch"].tolist()

    bullish_count = latest_labels.count("HH") + latest_labels.count("HL")
    bearish_count = latest_labels.count("LH") + latest_labels.count("LL")

    if score >= 70:
        bias = "bullish"
    elif score <= 30:
        bias = "bearish"
    else:
        bias = "neutral"

    report = {
        "price_action_score": score,
        "price_action_bias": bias,
        "bullish_structure_count": bullish_count,
        "bearish_structure_count": bearish_count,
        "recent_bos": [x for x in latest_bos if x != ""],
        "recent_choch": [x for x in latest_choch if x != ""],
        "latest_structure_labels": [x for x in latest_labels if x != ""],
    }

    return report, df