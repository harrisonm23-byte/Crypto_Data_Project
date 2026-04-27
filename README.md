# Cryptocurrency Volume-Spike Research

Exploratory quant research on cryptocurrency pricing data — measuring the relationship between anomalous volume spikes and forward returns across major cryptocurrencies.

## Research Design

**Objective:** Test whether anomalous volume events in crypto predict short-term forward returns, after controlling for unconditional market drift.

**Methodology:** Event study framework. Identify days where trading volume exceeds 2x its trailing 30-day rolling mean, classify by price direction (up-spike vs down-spike), and measure excess forward returns at multiple horizons (1, 2, 3, 5, 7, 10, 15, 20, 25, 30 days). Excess return is defined as the spike-day forward return minus the unconditional forward return across all coin-days in the sample, isolating the signal from sample-period drift.

**Universe:** 9 cryptocurrencies — BTC, ETH, BNB, ADA, LINK, XRP, XLM, DOGE, AVAX.

**Data:** Daily OHLCV (Open, High, Low, Close, Volume) from 2019-01-01 to 2026-04-19 via yfinance. 2,666 daily observations per coin.

**Inputs and Variables:**
- Volume ratio: daily volume / 30-day rolling mean volume
- Spike threshold: volume ratio ≥ 2.0
- Direction classification: down-spike (close < open), up-spike (close ≥ open)
- Forward returns: close-to-close over hold period
- Transaction costs: 20 bps (basis points) round-trip for market orders

## Key Findings

### Excess Returns vs Unconditional Baseline

| t (days) | Uncond | Up-Spike Excess | t-stat | Down-Spike Excess | t-stat |
|----------|--------|-----------------|--------|-------------------|--------|
| 1        | 0.23%  | -0.09%          | -0.19  | +0.96%            | 1.67   |
| 2        | 0.46%  | +0.85%          | 1.17   | **+2.39%**        | **3.40** |
| 3        | 0.70%  | +1.76%          | 2.02   | +2.21%            | 2.46   |
| 5        | 1.20%  | +3.82%          | 2.29   | +1.56%            | 1.57   |
| 7        | 1.71%  | +4.46%          | 2.54   | +2.11%            | 1.83   |
| 10       | 2.53%  | **+6.07%**      | **2.91** | +2.80%          | 2.01   |
| 15       | 3.99%  | +7.27%          | 2.54   | +2.80%            | 1.45   |
| 20       | 5.52%  | +7.85%          | 2.46   | +2.51%            | 1.05   |
| 25       | 7.08%  | +9.84%          | 2.48   | +0.76%            | 0.23   |
| 30       | 8.79%  | +10.37%         | 2.46   | +0.14%            | 0.04   |

Two distinct signals:
- **Down-spike reversal:** Short-term mean-reversion, peaks at day 2 (t=3.40), decays to zero by day 25.
- **Up-spike momentum:** Persistent continuation, t-stats above 2.0 from day 5 onward.

### Backtest Results (net of 20 bps transaction costs)

| Strategy | Trades | Ann Return | Ann Vol | Sharpe | Max DD | Hit Rate |
|----------|--------|-----------|---------|--------|--------|----------|
| Down-spike H=2 | 314 | 1.35% | 1.15% | 1.18 | -1.31% | 58.6% |
| Up-spike H=10 | 324 | 3.02% | 2.00% | 1.51 | -1.87% | 55.2% |
| Combined 50/50 | 638 | 2.21% | 1.34% | 1.65 | -1.08% | 56.9% |

### Trade Frequency

| Signal | Total Trades | Trades/Year | BTC Trades/Year | ETH Trades/Year |
|--------|-------------|-------------|-----------------|-----------------|
| Down-spike | 314 | 44.0 | 2.1 | 2.7 |
| Up-spike | 324 | 45.2 | 2.5 | 3.2 |
| Combined | 638 | 89.2 | 4.6 | 5.9 |

Combined book has at least one position open 57% of the time.

### Year-by-Year Stability (Down-Spike H=2)

| Year | Trades | Mean Ret% | Hit Rate% | Sharpe | Max DD% |
|------|--------|-----------|-----------|--------|---------|
| 2019 | 26 | 0.14 | 57.7 | 0.03 | -0.55 |
| 2020 | 26 | 7.98 | 65.4 | 1.54 | -0.29 |
| 2021 | 46 | 7.40 | 60.9 | 3.09 | -0.38 |
| 2022 | 46 | 2.30 | 54.3 | 0.60 | -1.31 |
| 2023 | 57 | 1.75 | 52.6 | 1.56 | -0.53 |
| 2024 | 61 | 1.97 | 52.5 | 1.27 | -0.31 |
| 2025 | 39 | 1.59 | 69.2 | 0.74 | -0.41 |
| 2026 | 13 | 6.92 | 76.9 | 1.53 | -0.21 |

Positive mean return in every sample year. Signal magnitude is regime-dependent — stronger in volatile bull markets (2020–2021), more modest in bear/flat periods (2022–2024).

## Additional Analysis

### Volume Mean-Reversion Half-Life
AR(1) regression on log(volume / 30-day mean) shows half-lives of 1.2 days (BTC) to 2.4 days (XLM). Volume spikes in crypto decay fast.

### Volume Cycle Analysis (BTC, ETH, BNB only)
For large-cap coins, volume always returns to its 30-day mean within 60 days (zero regime shifts observed). Median time to mean-reversion: 4 days. Post-normalization forward returns show zero excess vs unconditional baseline (t-stats < 0.6) — the tradeable signal is in the spike itself, not the return-to-mean event.

## Project Structure

```
├── ingest.py                      # Data ingestion script
├── data/
│   ├── crypto_px.pkl              # Cached price data (gitignored)
│   └── exploration_results.txt    # Event study tables
└── output/
    ├── backtest_report.txt        # Full results report
    ├── backtest_metrics.csv       # Strategy metrics (machine-readable)
    ├── strategy_comparison.png    # P&L chart (all strategies)
    ├── pnl_curve.png              # P&L chart (down-spike H=2)
    ├── trades.csv                 # Per-trade detail (down-spike H=2)
    ├── trades_down_H{2,5,7,10}.csv
    └── trades_up_H10.csv
```

## Setup

```bash
pip install yfinance pandas numpy scipy matplotlib
python3 ingest.py  # pulls data from yfinance, caches to data/crypto_px.pkl
```

## Transaction Cost Assumptions

- Market orders: 20 bps round-trip (10 bps in, 10 bps out)
- Limit orders: 7 bps (not used in backtest)

## Caveats

- Signal frequency is low for large-caps (BTC ~2 trades/year); statistical power is largely driven by mid-cap coins
- Sample period (2019–2026) is predominantly bullish
- No position sizing optimization or leverage applied
- Trade return distribution is right-skewed (median +1.14%, mean +3.28%, max +88.62%). A small number of large bounces contribute meaningfully
