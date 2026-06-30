## grid_trading on BTCUSDT (2020-01-01 → 2026-06-18)

**Verdict:** ❌ Falsified by deflate (deflate confidence 29%)

| Metric | Value | Read |
|---|---|---|
| In-sample Sharpe | -1.08 | naive pick |
| Out-of-sample Sharpe | -0.84 | the real test |
| **Deflated Sharpe (DSR)** | 0.00 | < 0.95 → not significant after multiple-testing correction |
| **PBO (CSCV)** | 0.48 | < 0.50 → IS winner survives OOS |
| Walk-forward stability | 0% positive folds | |
| Bootstrap P(SR ≤ 0) | 0.00 | |
| Configs swept | 9 | n_trials honest |
| Best params | `{'n_grids': 5, 'range_pct': 0.1}` | |

### Why deflate said this

- Deflated Sharpe is 0.00 (< 0.95): after correcting for 9 trial(s) and fat tails, the edge is not convincingly positive.
- Bootstrap P(SR<=0) is 1.00: the Sharpe is not reliably above zero under resampling.
- Only 0% of walk-forward folds are positive: performance is concentrated/unstable across time.
- PBO is 0.48 (< 0.50): the in-sample winner tends to hold up out of sample.

---

🔬 **Reproduce:**
```bash
git clone https://github.com/raphael2025/experiment-encyclopedia
cd experiment-encyclopedia
python -m experiments.runner --strategy grid_trading --symbol BTCUSDT
```

📲 Discussion & weekly verdicts: [Telegram — Raphael交易系统](https://t.me/+E3UdPtwlISVhZDc1)
