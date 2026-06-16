# Triangles, Flags & Wedges

> One-line: consolidation patterns — ascending/descending/symmetrical triangles, flags/pennants, rising/falling wedges — traded as continuation or breakout signals. **Verdict: ❌ (look-ahead + multiple-testing + cost); slow channel breakouts are the only conditional survivor.**

## What it is

These are the classic "the chart is coiling" formations:

- **Triangles** — converging trendlines. *Ascending*: flat top, rising lows. *Descending*: flat bottom, falling highs. *Symmetrical*: both lines converge ("coils").
- **Flags / pennants** — a small counter-trend channel (flag) or tiny triangle (pennant) after a sharp move, read as a pause before continuation. *High-and-tight flag*: forms after a ~90–100% spike in two months.
- **Wedges** — both lines slope the same way. *Rising wedge* (usually bearish), *falling wedge* (usually bullish).

The trade is to enter on the breakout in the expected direction, with a price target measured from the pattern's height.

## The claim

Compression stores "energy"; the breakout releases it into a measurable move. Bulkowski's *Encyclopedia of Chart Patterns* (3rd ed., 2021), the most-cited statistical source, ranks ~39 patterns on a large US-stock sample and reports figures like: ascending triangle up-break failure ~17%, avg gain ~43%; rectangle bottom failure ~15%, avg gain ~48%; symmetrical triangle ranked **36/39** ("performance is awful"); rising wedge down-break failure **51%**; pennant failure **~54%**, avg move only ~7%.

## The test

Note what Bulkowski's own numbers already say: average failure across patterns is ~22–25% (1 in 4–5), and the *worst* common ones (symmetrical triangle, wedge, pennant) are coin-flips. But the deeper problem is *how those stats are produced* and what happens under our gauntlet:

- **"Perfect trade" / hindsight selection.** Bulkowski's stats use cleanly-formed, hand-confirmed patterns. In real time you cannot know a triangle is "valid" (5-touch, no white space) until it has already resolved — that's [look-ahead bias](../../METHODOLOGY.md), the same killer as [head & shoulders](head-and-shoulders.md).
- **Multiple testing.** Dozens of named, tunable patterns × lookbacks guarantee some look great in-sample. Penalize the family with **Deflated Sharpe** and the edge deflates toward zero — selection-aware checks are decisive.
- **False breakouts + cost.** Crypto false-breakout rates run **35–50%** (vs ~20–25% in stocks) thanks to leverage, fragmented liquidity, and whales hunting the obvious level. Traded intraday with taker fees + slippage, the net result is negative; this is exactly why fast [breakout](../03-strategies/breakout.md) trading is ❌.

## Verdict: ❌ (with one conditional carve-out)

As discrete, hand-drawn signals these fail: the validating stats are hindsight, the pattern zoo invites overfitting, and crypto's false-breakout rate plus turnover cost finish them off. The **only** version that survives is a *slow channel/Donchian breakout traded as [trend following](../03-strategies/trend-following.md)* — which is 🔶 Conditional and works for the trend-persistence reason, not because the triangle "predicted" anything. Don't trade the shape; if you trade the breakout, trade it slow, vol-sized, and selection-aware.

## Try it yourself

Define one pattern *causally* (e.g., a Donchian breakout — a fully objective triangle/channel proxy) at two speeds: slow and intraday. Internalize cost and run [`deflate`](https://github.com/raphael2025/deflate) `placebo`, `deflated_sharpe` (penalize the lookback grid), `pbo`. The slow version looks like trend following and survives; the fast version dies on cost and placebo.

## Sources

- Bulkowski, T. N., *Encyclopedia of Chart Patterns*, 3rd ed. (2021); per-pattern stats at https://thepatternsite.com (rank index: /rank.html).
- Wikipedia — *Chart pattern*, *Technical analysis*.
- Bailey, Borwein, López de Prado & Zhu (2017), "The Probability of Backtest Overfitting" — the multiple-testing deflation that kills the pattern zoo.
