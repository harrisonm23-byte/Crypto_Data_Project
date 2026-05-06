# Crypto Volume-Spike Event Study

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

### Direct Signal Test (spike vs non-spike holding period returns)

Spike-day H-day returns compared against all non-spike H-day returns (spike observations excluded from the population). Welch's t-test and z-test. Returns are gross (pre-transaction costs) — the backtest results below apply 20 bps round-trip costs to confirm tradeability.

  | Signal | Period | Non-Spike Mean | Spike Mean | Excess | t-stat | p-val |
  |--------|--------|---------------|-----------|--------|--------|-------|
  | down_H2 | Train (2019–2022) | 0.59% | 4.77% | +4.18% | **3.44** | 0.0008 |
  | up_H10 | Train (2019–2022) | 3.43% | 10.30% | +6.87% | **2.22** | 0.028 |
  | down_H2 | Validation (2023+) | 0.24% | 2.39% | +2.15% | **3.45** | 0.0007 |
  | up_H10 | Validation (2023+) | 1.32% | 6.88% | +5.57% | **3.10** | 0.002 |
  | down_H2 | Full | 0.42% | 3.48% | +3.06% | **4.67** | 0.000 |
  | up_H10 | Full | 2.44% | 8.55% | +6.11% | **3.46** | 0.001 |

  Both signals are statistically significant in train and validation periods independently. Spike observations are excluded from the population to ensure a clean comparison.

### Backtest Results (net of 20 bps transaction costs)

| Strategy | Trades | Ann Return | Ann Vol | Sharpe | Max DD | Hit Rate |
|----------|--------|-----------|---------|--------|--------|----------|
| Down-spike H=2 | 314 | 1.35% | 1.15% | 1.18 | -1.31% | 58.6% |
| Up-spike H=10 | 324 | 3.02% | 2.00% | 1.51 | -1.87% | 55.2% |
| Combined 50/50 | 638 | 2.21% | 1.34% | 1.65 | -1.08% | 56.9% |

### Train/Validation Split

  Parameters discovered on the training set (2019–2022), then evaluated out-of-sample on the validation set (2023–present) with no changes to signal logic, thresholds, or hold periods.

  | Strategy | Period | Trades | Sharpe | Ann Return | Hit Rate | Alpha t-stat |
  |----------|--------|--------|--------|-----------|----------|-------------|
  | Down-spike H=2 | Train (2019–2022) | 144 | 1.22 | 1.61% | 59.0% | 2.16 |
  | Down-spike H=2 | **Validation (2023+)** | 170 | **1.15** | 1.10% | 58.2% | 1.55 |
  | Up-spike H=10 | Train (2019–2022) | 158 | 1.50 | 3.42% | 56.3% | 2.54 |
  | Up-spike H=10 | **Validation (2023+)** | 166 | **1.58** | 2.90% | 54.2% | 2.13 |
  | Combined 50/50 | Train (2019–2022) | 302 | 1.65 | 2.53% | 57.6% | 2.85 |
  | Combined 50/50 | **Validation (2023+)** | 336 | **1.73** | 2.01% | 56.2% |2.40 |

  Sharpe ratios and hit rates are stable or improved out-of-sample. The 50/50 weighting was set a priori (not optimized), avoiding look-ahead bias.

### Alpha / Beta vs BTC

  Computed via statsmodels OLS regression with proper standard errors on the intercept.

  | Strategy | Period | Daily Alpha (ann) | Alpha t-stat | Trade Alpha | Trade Alpha t |
  |----------|--------|------------------|-------------|-------------|--------------|
  | Down-spike H=2 | Full | 1.12% | **2.69** | 2.34% | **3.83** |
  | Down-spike H=2 | Train | 1.40% | **2.16** | 4.27% | **3.76** |
  | Down-spike H=2 | Validation | 0.79% | 1.55 | 0.62% | 1.13 |
  | Up-spike H=10 | Full | 2.31% | **3.33** | 5.47% | **3.34** |
  | Up-spike H=10 | Train | 2.73% | **2.54** | 7.76% | **2.69** |
  | Up-spike H=10 | Validation | 1.97% | **2.13** | 2.89% | 1.79 |
  | Combined 50/50 | Full | 1.73% | **3.73** | 3.89% | **4.42** |
  | Combined 50/50 | Train | 2.07% | **2.85** | 6.08% | **3.81** |
  | Combined 50/50 | Validation | 1.38% | **2.40** | 1.63% | 1.94 |

  Daily beta is near zero (~0.01) across all strategies, confirming returns are largely uncorrelated with BTC at the portfolio level.

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
    ├── signal_test_results.csv    # Direct signal test results
    ├── strategy_comparison.png    # P&L chart (all strategies)
    ├── pnl_curve.png              # P&L chart (down-spike H=2)
    ├── trades.csv                 # Per-trade detail (down-spike H=2)
    ├── trades_down_H{2,5,7,10}.csv
    └── trades_up_H10.csv
```

## Setup

```bash
pip install yfinance pandas numpy scipy matplotlib statsmodels
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
