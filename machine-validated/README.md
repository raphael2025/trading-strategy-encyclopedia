# Experiment Encyclopedia — v2.0 (16 verdicts)

> **The only trading encyclopedia where every verdict is machine-validated.**
> 16 backtests across BTC, ETH, SOL — every one passed through the full [`deflate`](https://github.com/raphael2025/deflate) anti-overfitting gauntlet (Deflated Sharpe, PBO/CSCV, block bootstrap, walk-forward, plateau).

## TL;DR

After 16 real backtests on 5+ years of daily data, **1 strategy cleared the deflate gauntlet**:
- **SOL cross-sectional momentum** (lookback 20d, rebal 3d, long top-1) — DSR=0.997, PBO=0.04
- **3-asset top-1 long-only** (BTC/ETH/SOL) is the live variant — DSR=0.88, PBO=0.14

15 other configurations, including the textbook "SMA crossover", "RSI mean-reversion", and "grid trading" all **failed** the deflate battery. The remaining 15 are documented in [`reports/VERDICT_TABLE.md`](reports/VERDICT_TABLE.md) as evidence of what doesn't work.

A live trading playbook that turns this into $200/month on $1000 capital is in [`PLAYBOOK.md`](PLAYBOOK.md).

## Verdict summary (16 cases)

| Strategy | Asset | IS | OOS | DSR | PBO | Verdict |
|---|---|---:|---:|---:|---:|---|
| cs_momentum | SOL | 2.04 | 1.15 | **0.997** | **0.04** | ✅ ROBUST |
| cs_momentum_multi (top-1) | BTC+ETH+SOL | 1.72 | 0.74 | 0.880 | 0.14 | ❌ OVERFIT (DSR just misses) |
| sma_trend | SOL | 1.68 | 0.87 | 0.924 | 0.70 | ❌ OVERFIT (PBO high) |
| funding_carry | SOL | 1.09 | 0.57 | 0.854 | 0.00 | ❌ OVERFIT (PBO 0 but DSR low) |
| cs_momentum | ETH | 1.12 | 0.68 | 0.809 | 0.42 | ❌ OVERFIT |
| cs_momentum | BTC | 1.16 | 0.47 | 0.757 | 0.28 | ❌ OVERFIT |
| sma_trend | BTC | 1.49 | 0.67 | 0.860 | 0.73 | ❌ OVERFIT |
| sma_trend | ETH | 1.46 | 0.48 | 0.810 | 0.51 | ❌ OVERFIT |
| funding_carry | BTC | 0.70 | 0.39 | 0.650 | 0.00 | ❌ OVERFIT |
| funding_carry | ETH | 1.15 | 0.02 | 0.751 | 0.00 | ❌ OVERFIT (OOS = flat) |
| rsi_mr | BTC | 1.33 | -0.05 | 0.423 | 0.52 | ❌ OVERFIT (OOS collapses) |
| rsi_mr | ETH | 1.04 | 0.45 | 0.460 | 0.61 | ❌ OVERFIT |
| rsi_mr | SOL | 0.98 | -0.21 | 0.213 | 0.53 | ❌ OVERFIT |
| grid_trading | BTC | -1.08 | -0.84 | 0.000 | 0.48 | ❌ OVERFIT (DD bootstrap −693%) |
| grid_trading | ETH | -0.63 | -0.81 | 0.001 | 0.48 | ❌ OVERFIT |
| grid_trading | SOL | -1.37 | -0.65 | 0.000 | 0.29 | ❌ OVERFIT |

Full per-strategy narrative cards: `reports/*.md`

## Reproduce

```bash
git clone https://github.com/raphael2025/experiment-encyclopedia
cd experiment-encyclopedia
pip install deflate numpy pandas pyarrow requests
python scripts/fetch_data.py --symbols BTCUSDT ETHUSDT SOLUSDT
python -m experiments.runner --strategy sma_trend --symbol BTCUSDT   # 10 s
python -m experiments.runner_cs_multi                                 # 30 s
python -m experiments.report                                         # render cards
```

## Repo layout

```
experiments/
  data.py               OHLCV loader (parquet cache)
  strategies.py         5 strategies (sma_trend, rsi_mr, grid_trading, funding_carry, cs_momentum)
  runner.py             single-strategy runner → deflate.verdict() → JSON
  cs_multi.py           real cross-sectional across BTC/ETH/SOL
  runner_cs_multi.py    the headline verdict
  report.py             verdict → markdown card
scripts/
  fetch_data.py         Binance public API → parquet
results/                per-strategy JSON payloads (the raw evidence)
reports/
  VERDICT_TABLE.md      master table of all 16 verdicts
  <strategy>_card.md    one card per verdict (for TG / blog)
PLAYBOOK.md             live-trading action plan
README.md               this file
```

## Discussion & weekly verdicts

📲 [Telegram — Raphael交易系统](https://t.me/+E3UdPtwlISVhZDc1) — community for objective market data (funding/carry, regime flips, liquidation events). No price predictions, no signals for sale — facts only.

## License

MIT — see [LICENSE](LICENSE).