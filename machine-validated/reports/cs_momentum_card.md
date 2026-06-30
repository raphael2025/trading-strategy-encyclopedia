## cs_momentum on BTCUSDT (2020-01-01 → 2026-06-18)

**Verdict:** ❌ Falsified by deflate (deflate confidence 50%)

| Metric | Value | Read |
|---|---|---|
| In-sample Sharpe | 1.16 | naive pick |
| Out-of-sample Sharpe | 0.47 | the real test |
| **Deflated Sharpe (DSR)** | 0.76 | < 0.95 → not significant after multiple-testing correction |
| **PBO (CSCV)** | 0.28 | < 0.50 → IS winner survives OOS |
| Walk-forward stability | 0% positive folds | |
| Bootstrap P(SR ≤ 0) | 0.00 | |
| Configs swept | 9 | n_trials honest |
| Best params | `{'lookback': 10, 'top_k': 1}` | |

### Why deflate said this

- Deflated Sharpe is 0.76 (< 0.95): after correcting for 9 trial(s) and fat tails, the edge is not convincingly positive.
- Bootstrap P(SR<=0) is 0.02: the Sharpe stays positive across resamples (selection-blind: a cherry-picked curve can still look good here).
- 60% of walk-forward folds are positive: performance is reasonably stable across time (selection-blind).
- PBO is 0.28 (< 0.50): the in-sample winner tends to hold up out of sample.

---

🔬 **Reproduce:**
```bash
git clone https://github.com/raphael2025/experiment-encyclopedia
cd experiment-encyclopedia
python -m experiments.runner --strategy cs_momentum --symbol BTCUSDT
```

📲 Discussion & weekly verdicts: [Telegram — Raphael交易系统](https://t.me/+E3UdPtwlISVhZDc1)
