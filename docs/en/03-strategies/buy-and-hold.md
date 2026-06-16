# Buy & Hold (Equal-Weight)

> One-line: buy a diversified basket and hold, rebalancing occasionally — no timing, no signals. **Verdict: ✅ Validated — a brutally hard baseline that most active strategies fail to beat.**

## What it is

Buy and hold is the absence of a trading strategy: pick a basket (e.g., equal-weight quality equities, or a small set of large-cap crypto), buy it, and hold through the cycle, optionally rebalancing back to target weights on a schedule. No entries, no exits, no indicators, no leverage. Equal-weight (rather than cap-weight) gives every name the same allocation and quietly harvests a rebalancing/diversification premium.

## The claim

The honest claim isn't that buy-and-hold is *clever* — it's that it's *cheap and hard to beat*. Near-zero turnover means near-zero cost; broad diversification means you capture the asset class's risk premium without single-name blowups; and the absence of decisions means no behavioral leakage. It exists in this repo as the **benchmark every active strategy must clear.**

## The test

On quality equities, equal-weight buy-and-hold posts a **Sharpe ~1.11** in our testing — and crucially it does so with almost no degrees of freedom, so there's nothing for Deflated Sharpe to penalize: it's not a fished result. That makes it the reference line in the [Verdict Index](../00-verdict-index.md). When an active strategy is run through the gauntlet, the question isn't "does it make money?" but "does it beat *this*, net of cost, after multiple-testing deflation?" Most don't.

In crypto the picture is more nuanced: drawdowns are far larger (−70%+ peak-to-trough is normal), so buy-and-hold there is high-Sharpe-in-good-regimes but tail-heavy; sizing and diversification (and pairing with uncorrelated edges like [carry](../08-crypto-specific/funding-rate-carry.md)) matter much more. The equity result is the clean, validated one.

## Verdict: ✅ Validated (and the benchmark)

Equal-weight buy-and-hold is a genuine ✅: it survives because it costs almost nothing, diversifies well, and can't be overfit. Its real role here is as the **competitor**. The meta-lesson of this whole encyclopedia is that complexity has to *earn its keep* by beating a near-free baseline after costs and selection effects — and the famous active strategies mostly don't. If you do nothing else, doing this (sized sensibly) beats the large majority of traders who churn signals and bleed fees.

## Try it yourself

Build an equal-weight, periodically-rebalanced basket, internalize the (tiny) rebalance cost, and compute its Sharpe with [`deflate`](https://github.com/raphael2025/deflate)'s `bootstrap` for an honest Sharpe/drawdown distribution. Then run *any* active strategy you like and check whether its DSR-adjusted, cost-internalized Sharpe actually exceeds this line. Usually it won't — that's the point.

## Sources

- Equal-weight vs cap-weight indexing literature (rebalancing premium); S&P "SPIVA" scorecards on active-vs-passive underperformance.
- DeMiguel, Garlappi & Uppal (2009), "Optimal Versus Naive Diversification" — the 1/N (equal-weight) portfolio is hard to beat out-of-sample.
- This repo's [position sizing](../06-risk-management/position-sizing-and-vol-targeting.md) entry — how to size a hold so drawdown is tolerable.
