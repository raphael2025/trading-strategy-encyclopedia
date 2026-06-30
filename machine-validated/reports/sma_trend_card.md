## sma_trend on BTCUSDT (2020-01-01 → 2026-06-18)

**Verdict:** ❌ Falsified by deflate (deflate confidence 43%)

| Metric | Value | Read |
|---|---|---|
| In-sample Sharpe | 1.49 | naive pick |
| Out-of-sample Sharpe | 0.67 | the real test |
| **Deflated Sharpe (DSR)** | 0.86 | < 0.95 → not significant after multiple-testing correction |
| **PBO (CSCV)** | 0.73 | ≥ 0.50 → in-sample best likely fails OOS |
| Walk-forward stability | 0% positive folds | |
| Bootstrap P(SR ≤ 0) | 0.00 | |
| Configs swept | 16 | n_trials honest |
| Best params | `{'fast': 10, 'slow': 100}` | |

### Why deflate said this

- Deflated Sharpe is 0.86 (< 0.95): after correcting for 16 trial(s) and fat tails, the edge is not convincingly positive.
- PBO is 0.73 (>= 0.50): the in-sample best configuration is no better than a coin flip out of sample.
- Bootstrap P(SR<=0) is 0.00: the Sharpe stays positive across resamples (selection-blind: a cherry-picked curve can still look good here).
- 80% of walk-forward folds are positive: performance is reasonably stable across time (selection-blind).

---

🔬 **Reproduce:**
```bash
git clone https://github.com/raphael2025/experiment-encyclopedia
cd experiment-encyclopedia
python -m experiments.runner --strategy sma_trend --symbol BTCUSDT
```

📲 Discussion & weekly verdicts: [Telegram — Raphael交易系统](https://t.me/+E3UdPtwlISVhZDc1)
