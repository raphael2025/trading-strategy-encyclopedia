# Wyckoff Accumulation & Distribution

> One-line: a century-old framework that reads price/volume "phases" as a "Composite Man" quietly accumulating before a markup and distributing before a markdown. **Verdict: ❌ as a tradeable timing method (look-ahead + subjective labeling); ⚠️ useful as a descriptive lens.**

## What it is

Richard Wyckoff (1873–1934) proposed that markets move through four repeating phases driven by a hypothetical large operator he called the **Composite Man**:

1. **Accumulation** — sideways range at a low after a downtrend; the operator quietly buys. Sub-events get names: *selling climax (SC)*, *automatic rally (AR)*, *secondary test (ST)*, and the *spring* (a brief false breakdown below the range that "shakes out" weak holders).
2. **Markup** — the uptrend; the range breaks upward on expanding volume.
3. **Distribution** — sideways range at a high; the operator quietly sells. Mirror events: *buying climax*, *upthrust (UT/UTAD)* — a false breakout above the range.
4. **Markdown** — the downtrend.

Wyckoff added three "laws" — supply/demand, cause/effect (range width predicts move size), and effort/result (volume vs price spread) — and the trading edge is supposedly to *buy the spring and sell the upthrust*, entering with the Composite Man rather than against him.

## The claim

That volume and range "footprints" reveal large-operator intent before price moves, so a trained reader can position ahead of the markup/markdown. The spring and upthrust are sold as high-probability, low-risk entry triggers.

## The test

Wyckoff phases are defined the same way [chart patterns](../02-chart-patterns/) are, and they inherit the same fatal flaws:

- **Look-ahead bias is structural.** You only *know* a range was "accumulation" after the markup happens; a "spring" is only a spring if price recovers — if it keeps falling it was just a breakdown. Labeling phases on a historical chart is hindsight; timestamped causally, the "signal" disappears. This is the single biggest reason [head & shoulders](../02-chart-patterns/head-and-shoulders.md) and SMC zones fail here.
- **Subjective and unfalsifiable as stated.** Phase boundaries, which swing is "the" spring, how wide a range "counts" — all are discretionary. A method with that many free choices will always fit the past and rarely beats a [matched placebo](../../METHODOLOGY.md) out-of-sample.
- **Crowding and cost.** The visible levels (range edges) are exactly where everyone places orders — making them prime [liquidity-hunt](liquidity-hunts.md) targets, not free entries.

We have not run a dedicated Wyckoff backtest (it's hard to even specify causally), but every component that *can* be tested — range-breakout fades, false-breakout reversals, volume-confirmation rules — has failed elsewhere in this repo on look-ahead, placebo, and cost.

## Verdict: ❌ as a timing method / ⚠️ as a lens

As a *vocabulary* for describing how ranges resolve and why volume matters, Wyckoff is genuinely useful and broadly correct: big players do accumulate quietly, and false breakouts at range edges are real. As a *mechanical edge*, it fails the gauntlet — the phases are only knowable in hindsight, the labeling is subjective enough to overfit anything, and the entry levels are crowded liquidity. Treat it as intuition, not a signal. The honest, testable cousins that *do* survive are slow [trend following](../03-strategies/trend-following.md) and [breakout](../03-strategies/breakout.md) — which capture "markup/markdown" persistence without pretending to read the Composite Man's mind.

## Try it yourself

Operationalize one rule unambiguously — e.g., "buy a confirmed spring: close back inside the range within K bars after piercing the range low" — timestamp at bar close, internalize cost, and run [`deflate`](https://github.com/raphael2025/deflate) `placebo` + `deflated_sharpe`. The hard part (and the tell) is that any *causal* definition strips away exactly the hindsight that made it look good.

## Sources

- Wikipedia — *Technical analysis*, *Chart pattern* — context for phase/footprint reading and its known biases.
- Wyckoff, R. D. — original course material on accumulation/distribution and the Composite Man (early 20th c.; secondary summaries).
- Bailey, Borwein, López de Prado & Zhu (2017), "The Probability of Backtest Overfitting," *Journal of Computational Finance* — why subjective, many-degree-of-freedom labeling overfits.
