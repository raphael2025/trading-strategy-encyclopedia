# 16 verdicts · BTC + ETH + SOL + Multi (1d, 2020–2026)

Each row = a real backtest run through the deflate anti-overfitting gauntlet.

| Strategy | Asset | IS SR | OOS SR | DSR | PBO | Verdict |
|---|---|---:|---:|---:|---:|---|
| cs_momentum | BTCUSDT | 1.16 | 0.47 | 0.757 | 0.28 | ❌ OVERFIT (50%) |
| cs_momentum | ETHUSDT | 1.12 | 0.68 | 0.809 | 0.42 | ❌ OVERFIT (50%) |
| cs_momentum | SOLUSDT | 2.04 | 1.15 | 0.997 | 0.04 | ✅ ROBUST |
| cs_momentum_multi | BTC+ETH+SOL | 1.72 | 0.74 | 0.880 | 0.14 | ❌ OVERFIT (50%) |
| funding_carry | BTCUSDT | 0.70 | 0.39 | 0.650 | 0.00 | ❌ OVERFIT (50%) |
| funding_carry | ETHUSDT | 1.15 | 0.02 | 0.751 | 0.00 | ❌ OVERFIT (50%) |
| funding_carry | SOLUSDT | 1.09 | 0.57 | 0.854 | 0.00 | ❌ OVERFIT (50%) |
| grid_trading | BTCUSDT | -1.08 | -0.84 | 0.000 | 0.48 | ❌ OVERFIT (29%) |
| grid_trading | ETHUSDT | -0.63 | -0.81 | 0.001 | 0.48 | ❌ OVERFIT (29%) |
| grid_trading | SOLUSDT | -1.37 | -0.65 | 0.000 | 0.29 | ❌ OVERFIT (29%) |
| rsi_mr | BTCUSDT | 1.33 | -0.05 | 0.423 | 0.52 | ❌ OVERFIT (43%) |
| rsi_mr | ETHUSDT | 1.04 | 0.45 | 0.460 | 0.61 | ❌ OVERFIT (43%) |
| rsi_mr | SOLUSDT | 0.98 | -0.21 | 0.213 | 0.53 | ❌ OVERFIT (43%) |
| sma_trend | BTCUSDT | 1.49 | 0.67 | 0.860 | 0.73 | ❌ OVERFIT (43%) |
| sma_trend | ETHUSDT | 1.46 | 0.48 | 0.810 | 0.51 | ❌ OVERFIT (43%) |
| sma_trend | SOLUSDT | 1.68 | 0.87 | 0.924 | 0.70 | ❌ OVERFIT (43%) |

## Headline finding

**SOL cross-sectional momentum (lookback=20d, rebal=3d, long top-1) is the only strategy to clear the full deflate battery: DSR=0.997, PBO=0.04, walk-forward 80% positive.**

The full-3-asset variant (long top1 across BTC/ETH/SOL, rebal=3d) comes close: DSR=0.88, PBO=0.14 — both excellent, DSR just under the 0.95 threshold. Bootstrap + walk-forward both pass.

Grid-trading is the worst — DSR=0.00 on all 3 assets, worst bootstrap drawdown around −693%. The funding-carry proxy is borderline (PBO=0.00, but DSR ≤ 0.85 on all assets).
