"""
Step 1: Data ingestion for crypto pricing research.
Pull daily OHLCV for 9 coins from yfinance, cache to data/crypto_px.pkl.
"""
import yfinance as yf
import pandas as pd
from pathlib import Path

TICKERS = [
    "BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "LINK-USD",
    "XRP-USD", "XLM-USD", "DOGE-USD", "AVAX-USD",
]
START = "2019-01-01"
OUT = Path("data/crypto_px.pkl")

# --- download ---
raw = yf.download(TICKERS, start=START, group_by="ticker", threads=True)

# reshape: MultiIndex columns (ticker, field) → keep as-is
# yfinance returns columns like (BTC-USD, Close), etc.
print(f"\nRaw shape: {raw.shape}")
print(f"Date range: {raw.index.min()} → {raw.index.max()}")
print(f"Columns levels: {raw.columns.names}\n")

# --- per-coin sanity ---
for tkr in TICKERS:
    sub = raw[tkr]
    n_rows = len(sub)
    n_nan = sub["Close"].isna().sum()
    first_valid = sub["Close"].first_valid_index()
    print(f"{tkr:>8s}  rows={n_rows:>5d}  NaN(Close)={n_nan:>4d}  first_valid={first_valid}")

# --- head / tail ---
close = raw.xs("Close", axis=1, level=1)
print("\n— Close prices head —")
print(close.head(3).to_string())
print("\n— Close prices tail —")
print(close.tail(3).to_string())

# --- save ---
raw.to_pickle(OUT)
print(f"\nSaved to {OUT}  ({OUT.stat().st_size / 1e6:.1f} MB)")
