import yfinance as yf

ticker = "XLK"

print("\n================ YAHOO PROBE ================\n")
print("Testing:", ticker)

data = yf.download(
    ticker,
    period="1mo",
    interval="1d",
    progress=False,
    auto_adjust=True,
    threads=False,
)

print(data)
print("\nEmpty:", data.empty)
print("\nColumns:", data.columns)