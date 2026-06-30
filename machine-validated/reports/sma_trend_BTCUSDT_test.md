### Empirical evidence (deflate battery)

- **Universe**: BTCUSDT daily, 2020-01-01 → 2026-06-18 (2361 bars).
- **Grid searched**: 16 configurations (best params: `{'fast': 10, 'slow': 100}`).
- **Annualised Sharpe**: 1.13.  **Deflated Sharpe**: 0.860 (n_trials=16, E[max SR]=0.037).
- **PBO (CSCV)**: 0.73.
- **Bootstrap**: P(SR≤0) = 0.00, SR 90% CI = [0.48, 1.78], realistic worst DD (1%) = -125.9%.
- **Walk-forward**: 80% of 5 folds positive, mean fold SR = 0.85.
- **Verdict**: **LIKELY OVERFIT ❌** (confidence 43%).

**Why:**
- Deflated Sharpe is 0.86 (< 0.95): after correcting for 16 trial(s) and fat tails, the edge is not convincingly positive.
- PBO is 0.73 (>= 0.50): the in-sample best configuration is no better than a coin flip out of sample.
- Bootstrap P(SR<=0) is 0.00: the Sharpe stays positive across resamples (selection-blind: a cherry-picked curve can still look good here).
- 80% of walk-forward folds are positive: performance is reasonably stable across time (selection-blind).

_Reproduction: `python -m experiments.runner --strategy sma_trend --symbol BTCUSDT --start 2020-01-01 --end 2026-06-18`._
