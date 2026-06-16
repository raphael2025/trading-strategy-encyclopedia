# Wyckoff Schematics (Chart-Pattern View)

> One-line: the springs, upthrusts, and trading-range schematics of the Wyckoff method, as drawn on a price chart. **Verdict: ❌ as a timing pattern (look-ahead + subjectivity).**

## What it is

This entry covers the *chart-pattern* face of Wyckoff: the textbook **accumulation** and **distribution** schematics and their named events — *selling/buying climax, automatic rally/reaction, secondary test, spring (false breakdown), upthrust/UTAD (false breakout), sign of strength/weakness, last point of support*. Traders draw these on the chart and try to enter on the spring (long) or upthrust (short). For the full method, laws, and the "Composite Man" framing, see [Wyckoff accumulation & distribution](../07-market-mechanics/wyckoff-accumulation-distribution.md) in Market Mechanics.

## The claim

That the schematic tells you, *while the range is still forming*, whether smart money is accumulating or distributing — so a spring is a high-probability long entry and an upthrust a high-probability short, with a tight stop just beyond the false-break.

## The test

As a chart pattern it inherits the standard pattern killers:

- **Look-ahead.** A "spring" is only a spring if price recovers back into the range; if it keeps falling, it was a breakdown. You can't tell which at the moment of the pierce — labeling it requires the future. Same structural flaw as [head & shoulders](head-and-shoulders.md), [triangles](triangles-flags-wedges.md), and [Elliott Wave](elliott-wave.md).
- **Subjectivity.** Which range, which low is "the" spring, how deep a pierce qualifies — all discretionary, so the schematic fits the past and overfits out-of-sample.
- **Crowded levels + cost.** Range edges are exactly where stops cluster, making them prime [liquidity-hunt](../07-market-mechanics/liquidity-hunts.md) targets; fading them intraday loses to fees and slippage, like every other [false-breakout fade](../00-verdict-index.md) tested here.

## Verdict: ❌

The Wyckoff schematic is a useful *picture* of how ranges sometimes resolve, but as a mechanical entry it fails: the spring/upthrust labels are hindsight, the drawing is subjective, and the levels are crowded liquidity. The persistence it gestures at (markup/markdown) is captured honestly by slow [trend following](../03-strategies/trend-following.md) and [breakout](../03-strategies/breakout.md). See the [Market-Mechanics entry](../07-market-mechanics/wyckoff-accumulation-distribution.md) for the broader framework and the same verdict.

## Try it yourself

Encode "spring = close back inside the range within K bars of piercing the range low," timestamp causally, add cost, and run [`deflate`](https://github.com/raphael2025/deflate) `placebo` + `deflated_sharpe`. The causal definition removes the hindsight that made it look good.

## Sources

- Wikipedia — *Technical analysis*, *Chart pattern*.
- Wyckoff, R. D. — original accumulation/distribution schematics (early 20th c.; secondary summaries).
- Bailey, Borwein, López de Prado & Zhu (2017), "The Probability of Backtest Overfitting."
