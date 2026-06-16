# Mega-Cap Cross-Sectional Factors

> One-line: running classic factors (momentum, value) on the largest, most-liquid names. **Verdict: ❌ — the factor edge lives in small/mid caps; mega-caps are too efficient (DSR ≈ 0.004).**

## What it is

Cross-sectional factor investing ranks a universe by a characteristic — 12-month momentum, value, quality — and goes long the top, short (or underweight) the bottom. It's the institutional workhorse and a documented historical premium. This entry is specifically about applying it to a **mega-cap** universe: the handful of giant, household-name stocks (or the top-few crypto assets), rather than the broad small/mid-cap cross-section where the academic premia were measured.

## The claim

That factor premia are universal, so you can run momentum/value on the safest, most-liquid, easiest-to-trade large caps and still collect the edge — with less liquidity risk than small caps.

## The test

We ran cross-sectional factors on a mega-cap universe through the full gauntlet. The result is a textbook ❌: the in-sample Sharpe looks plausible, but the **Deflated Sharpe Ratio ≈ 0.004** — i.e., once you penalize for how many factor/lookback combinations were tried, the probability that the true Sharpe is positive is essentially zero. The contrast is decisive against [cross-sectional momentum on a *liquid-but-not-saturated* universe](cross-sectional-momentum.md), which clears DSR/PBO at Sharpe ~1.2.

The mechanism is efficiency and breadth: factor premia are compensation for risk/frictions that are *strongest where arbitrage is hardest* — small and mid caps. Mega-caps are the most analyzed, most arbitraged, most liquid names on earth; whatever premium existed there is competed away. And a universe of only a few giant names has almost no cross-sectional *breadth*, so a "factor" portfolio is really a couple of concentrated bets dressed up as diversification — exactly the setup DSR is built to expose.

## Verdict: ❌

Mega-cap factor portfolios fail on multiple-testing: DSR ≈ 0.004 means the apparent edge is indistinguishable from a fished result. Factors are real, but they live where inefficiency and breadth live — not in the most efficient corner of the market. The lesson generalizes: a strategy that works on a broad, mildly-inefficient universe can completely die when you restrict it to the biggest, most-crowded names. Universe choice is part of the strategy, and the wrong universe turns a ✅ into a ❌.

## Try it yourself

Run the same factor ranking on (a) a broad liquid universe and (b) a mega-cap-only universe, internalize cost, and compute `deflated_sharpe` and `pbo` with [`deflate`](https://github.com/raphael2025/deflate), penalizing the factor/lookback grid you searched. You should see (a) survive and (b) collapse to DSR near zero — the universe is doing the work.

## Sources

- Bailey & López de Prado (2014), "The Deflated Sharpe Ratio" — the test that produces the ≈0.004.
- Fama & French; Jegadeesh & Titman (momentum) — where the premia were originally measured (broad cross-sections, not mega-caps only).
- This repo's [cross-sectional momentum](cross-sectional-momentum.md) — the surviving version, and the universe contrast.
