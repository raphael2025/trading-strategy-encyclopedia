# Breakout

> One-line: enter when price breaks above a prior range high or below a prior range low — Donchian/channel breakouts and volatility-squeeze breakouts. **Verdict: 🔶 Conditional**.

## What it is

A breakout strategy waits for price to clear a reference level — the highest high of the last N bars (a Donchian channel), the edge of a price channel, or the upper/lower band after a period of compressed volatility (a "squeeze"). The break is taken as the signal that a new directional move has begun, and you enter in the direction of the break.

## The claim

Ranges represent equilibrium; a decisive break means the balance has tipped and a new trend is starting. Get in at the break and you catch the move from its inception, before the crowd. The volatility-squeeze version adds a timing story: tight bands mean coiled energy, and the expansion that follows is the trade.

## The test

We evaluated breakout entries on crypto perpetuals (BTC/ETH/SOL), timestamped at bar close (no look-ahead) with **taker fees + slippage + funding internalized**, and deliberately separated two species:

- **(a) Slow channel breakout.** A break of a long, slow Donchian/channel level is, mechanically, a *trend-following entry* — and it inherits the same modest, cost-surviving edge (Sharpe order ~1.1) when traded slow and sized by volatility.
- **(b) Fast / intraday "buy the breakout."** On low timeframes it is dominated by **false breakouts** (price pokes the level, sucks in entries, then reverses) and by **turnover cost** (≈ −86%/yr territory). Net-negative; no edge vs placebo; DSR collapses under the level/lookback search.

## Verdict: 🔶 Conditional

Breakout is real *only* as a slow, cost-aware variant — at which point it is essentially [trend following](trend-following.md) in different clothing, and survives for the same reasons (it rides persistence, clears cost, sits on a parameter plateau). Naive intraday breakouts are ❌: false breakouts plus turnover bleed them out. The **volatility-squeeze → breakout** case is the genuinely conditional one — it can work when the subsequent move is slow and trend-like, but it is not free; tested as a fast band-expansion trigger it behaves like the rest of the [Bollinger Band](../01-technical-indicators/bollinger-bands.md) family. Condition for the ✅ side: trade it slow, accept the same fat-tail / low-win-rate payoff profile as trend following, and never tighten it into an intraday signal.

## Try it yourself

Build two versions on bar closes — a slow channel breakout and a fast intraday one — apply realistic per-turn cost, and run both through [`deflate`](https://github.com/raphael2025/deflate): `deflated_sharpe` (penalize the lookback/level grid), `pbo`, and `placebo`. The slow version should clear the gauntlet (and look a lot like trend following); the fast version fails on cost and placebo. That contrast *is* the verdict.

## Sources

- Donchian, R. — origin of the channel-breakout rule that anchors the slow, trend-capturing variant.
- Moskowitz, Ooi & Pedersen (2012), "Time Series Momentum," *Journal of Financial Economics* — breakouts as momentum proxies; the survivor edge is the trend, not the break itself.
- Bailey, Borwein, López de Prado & Zhu (2017), "The Probability of Backtest Overfitting," *Journal of Computational Finance* — the test that kills the over-tuned intraday version.
