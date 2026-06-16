# Harmonic Patterns

> One-line: Fibonacci-ratio reversal patterns — Gartley, Bat, Butterfly, Crab, Shark, AB=CD — that mark a "Potential Reversal Zone." **Verdict: ❌ (curve-fitting + look-ahead + multiple-testing).**

## What it is

Harmonic patterns are multi-leg price structures (typically labeled X-A-B-C-D) that "qualify" only when their legs hit specific Fibonacci ratios:

| Pattern | Key ratios |
|---|---|
| **Gartley** | AB=CD, 0.618 retracement |
| **Bat** | 0.886 XA retracement |
| **Butterfly** | 1.272 / 1.618 extension |
| **Crab** | 1.618 extension |
| **Shark** | 0.886, 1.13 |
| **AB=CD** | 1.0 / 1.272 / 1.618 |
| **Three Drives** | 1.272, 1.618 |

Where the ratios converge is the **Potential Reversal Zone (PRZ)**; the trade is to fade price there, expecting a reversal, with stops just beyond the PRZ.

## The claim

That markets move in Fibonacci-proportioned swings, so when a structure matches the ratios within tolerance, the PRZ is a high-probability turning point. Proponents (Gartley's *Profits in the Stock Market*, later Scott Carney's *Harmonic Trading*) present them as precise, rule-based entries — more rigorous than freehand patterns because the ratios are "objective."

## The test

The "objectivity" is illusory and the structure is a textbook overfitting machine:

- **Tolerance bands = free parameters.** "0.618 ± tolerance," "1.618 ± tolerance," plus the choice of which swings count as X/A/B/C/D, give enormous discretion. With that many degrees of freedom you can find a "valid" harmonic on almost any chart in hindsight — and anything that flexible overfits the past and fails out-of-sample.
- **Look-ahead.** Point D (the entry) is only knowable once the structure has completed; labeling the swings requires seeing the future, just as with [head & shoulders](head-and-shoulders.md) and [Elliott Wave](elliott-wave.md).
- **Multiple testing.** Seven-plus named patterns × ratio tolerances × timeframes guarantee in-sample winners; **Deflated Sharpe** deflates the family to noise. No large-sample, peer-reviewed evidence shows harmonic entries beat a [matched placebo](../../METHODOLOGY.md) net of cost — and the KB's own source (Bulkowski) provides no harmonic-specific failure stats at all, only ratios from secondary references.
- **Fibonacci has no mechanism.** There is no documented reason price *should* reverse at 0.886 vs 0.85; it's numerology dressed as geometry.

## Verdict: ❌

Harmonic patterns combine every failure mode this repo catalogues: hindsight leg-labeling, tolerance bands that fit anything, a zoo of patterns that invites selection, and no causal mechanism — all on top of crypto's elevated false-reversal rate and trading cost. There is no credible evidence of an out-of-sample, cost-surviving, placebo-beating edge. The PRZ is most useful as a list of crowded levels that get [hunted](../07-market-mechanics/liquidity-hunts.md), not as a reliable turning point.

## Try it yourself

Pin down a single pattern with *fixed* ratio tolerances and an objective swing-detector, timestamp the entry at D's confirmation (no peeking), internalize cost, and run [`deflate`](https://github.com/raphael2025/deflate) `placebo` + `deflated_sharpe` across the pattern family. Watch DSR collapse once the number of patterns/tolerances tried is penalized.

## Sources

- Wikipedia — *Chart pattern* (harmonic section), *Technical analysis*.
- Gartley, H. M., *Profits in the Stock Market* (1935); Carney, S., *Harmonic Trading* (vols. 1–2) — primary harmonic references.
- Bailey, Borwein, López de Prado & Zhu (2017), "The Probability of Backtest Overfitting" — the deflation that kills tolerance-tuned pattern families.
