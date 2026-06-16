# Cross-Sectional Momentum

> One-line: rank a liquid universe by recent return (combined with an illiquidity factor), go long the top quantile and short the bottom — relative, not absolute, momentum. **Verdict: ✅ Validated** (on the right universe).

## What it is

Where trend following asks "is *this* asset going up?", cross-sectional momentum asks "which assets are going up *relative to each other*?" You take a liquid universe, rank every name by its trailing return over a lookback window, go long the strongest quantile (say the top 20%) and short the weakest (the bottom 20%), then rebalance periodically. Adding an **illiquidity** factor — tilting toward names whose returns aren't already arbitraged flat — sharpens the spread.

## The claim

Winners keep winning and losers keep losing, cross-sectionally, over intermediate horizons. The same under-reaction and herding that produce time-series trends produce a relative ranking that persists long enough to harvest by holding the spread between the extremes — a market-neutral-ish bet that doesn't need the whole market to go up.

## The test

We ranked a **liquid universe**, traded the top/bottom 20%, combined **momentum + illiquidity** as a multi-factor score, timestamped at rebalance close (no look-ahead) with **fees + slippage + funding internalized**, and scored the factor/lookback choices selection-aware.

- **Sharpe ≈ 1.2**, clearing Deflated Sharpe and PBO — a real, diversified edge.
- **Universe-dependent.** On equity **mega-caps** the same factors are ❌ (DSR ≈ 0.004) — mega-caps are too efficiently arbitraged; the premium lives in small/mid-caps and in the liquid-but-less-arbitraged corners of crypto.
- **Combines beautifully.** Stacked with [trend following](trend-following.md) and funding carry, the blend reaches **Sharpe ≈ 1.7, DSR 0.93, drawdown ≈ −22%** — because the three sleeves have low mutual correlation.

## Verdict: ✅ Validated

It survives because it is diversified across many names, *relative* (so it doesn't depend on market direction), slow enough to clear cost, and selection-aware enough to pass DSR/PBO. Conditions: it only works on the right **universe** — the edge is structurally absent in hyper-efficient mega-caps (DSR ≈ 0.004), so a liquid-but-not-saturated universe is mandatory. Realistic expectation: a ~1.2 standalone Sharpe — which, like trend following, only just clears the equal-weight buy-and-hold benchmark (Sharpe ~1.11) on its own. Its real value is the **low correlation** it brings to a combined book; see the [verdict index](../00-verdict-index.md) for the combined sleeve.

## Try it yourself

Rank a liquid universe by trailing return plus an illiquidity tilt, form a long-top / short-bottom 20% portfolio, rebalance with realistic cost, then run through [`deflate`](https://github.com/raphael2025/deflate): `deflated_sharpe` (penalize the factor/lookback search), `pbo`, `placebo`. Then rerun on a mega-cap-only universe and watch the DSR collapse toward ~0 — that contrast shows the edge is universe-conditional, not universal.

## Sources

- Jegadeesh, N. & Titman, S. (1993), "Returns to Buying Winners and Selling Losers," *Journal of Finance* — the foundational cross-sectional momentum result.
- Asness, Moskowitz & Pedersen (2013), "Value and Momentum Everywhere," *Journal of Finance* — momentum across markets and asset classes.
- Amihud, Y. (2002), "Illiquidity and Stock Returns," *Journal of Financial Markets* — the illiquidity factor in the multi-factor score.
