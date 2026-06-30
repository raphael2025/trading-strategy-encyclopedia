# Machine-Validated Results

Every verdict here is backed by a **reproducible run through the full anti-overfitting gauntlet** — not a screenshot, not a cherry-picked equity curve.

Each strategy is swept across a parameter grid, the in-sample best is picked, then judged by:

- **Deflated Sharpe Ratio (DSR)** — Sharpe corrected for how many configs you tried + fat tails. Bar: ≥ 0.95.
- **PBO / CSCV** — does the in-sample winner hold up out-of-sample, or is it a coin flip? Bar: < 0.50.
- **Walk-forward** — consecutive out-of-sample folds; % positive shows time stability.
- **Block bootstrap** — Sharpe confidence interval + realistic worst-case drawdown.

## The uncomfortable headline

> **Across 16 machine-validated strategies on BTC/ETH/SOL, exactly one cleared every gate.**
> Cross-sectional momentum on SOL (DSR 0.997, PBO 0.04). Everything else — SMA trend, RSI mean-reversion, funding carry, grid — failed DSR/PBO, OOS sign-flip, or cost.

And the deeper lesson the verdicts keep teaching: **a full-history DSR pass is necessary but not sufficient.** A strategy whose edge lives in one early regime can clear the gauntlet and still be negative in the most recent window — so the last gate is always *recent-regime + live paper*, never the backtest alone.

## What's here

| Path | What |
|------|------|
| [`OVERVIEW.md`](OVERVIEW.md) | How verdicts are produced + validation method |
| [`PLAYBOOK.md`](PLAYBOOK.md) | Live execution rules: position sizing, stop conditions, deployment gates |
| [`reports/`](reports/) | Per-strategy verdict cards |
| [`results/`](results/) | Raw verdict payloads (DSR/PBO/walk-forward/bootstrap metrics, JSON) |
| [`experiments/`](experiments/) | The validation harness — reproduce every verdict yourself |

The validation toolkit is open source: **[`deflate`](https://github.com/raphael2025/deflate)** — point it at your own returns.
