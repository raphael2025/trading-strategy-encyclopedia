# Elliott Wave Theory

> One-line: the claim that markets move in repeating 5-wave impulse + 3-wave corrective fractals, countable in advance. **Verdict: ❌ (subjective, unfalsifiable, look-ahead).**

## What it is

Ralph Nelson Elliott (1930s) proposed that crowd psychology drives prices in self-similar fractal "waves." A complete cycle is **5 waves in the direction of the trend (an impulse: 1-2-3-4-5) followed by 3 corrective waves (A-B-C).** Each wave subdivides into smaller waves of the same form, across all timeframes. A set of rules (wave 3 is never the shortest; wave 4 doesn't overlap wave 1; etc.) and Fibonacci relationships between wave lengths are used to "count" the current position and project the next move.

## The claim

That if you correctly identify where you are in the wave count, you know whether the next move is an impulse leg (trade with it) or a correction (fade or wait), and Fibonacci ratios give you targets. Proponents present it as a complete forecasting framework.

## The test

Elliott Wave is the canonical example of a theory that *cannot be put through the gauntlet honestly*, which is itself the verdict:

- **Unfalsifiable / infinitely flexible.** The rules permit so many alternate counts (and "extensions," "truncations," "diagonals") that almost any price path can be relabeled after the fact to fit. A theory that can explain every outcome predicts none. This is the opposite of what [our methodology](../../../METHODOLOGY.md) requires — a *causal, fixed* rule.
- **Look-ahead by construction.** "We were in wave 3" is a statement you can only make confidently *after* wave 3 completes. Real-time counts routinely get revised, which means the "signal" is a hindsight narrative, not a tradeable trigger — the same flaw as [Wyckoff](../07-market-mechanics/wyckoff-accumulation-distribution.md) and [harmonic patterns](harmonic-patterns.md).
- **No reproducible edge.** Because two analysts produce different counts on the same chart, there is no objective rule to backtest, no [placebo](../../../METHODOLOGY.md) comparison, and no Deflated-Sharpe number. Decades of practice have produced no large-sample, peer-reviewed evidence of an out-of-sample, cost-surviving edge.

## Verdict: ❌

Elliott Wave fails before it reaches a single cost calculation: it is subjective, endlessly revisable, and only "works" in hindsight. The kernel of truth — markets trend and correct, and persistence is real — is captured far more honestly by mechanical [trend following](../03-strategies/trend-following.md) and [cross-sectional momentum](../03-strategies/cross-sectional-momentum.md), which are objective, reproducible, and survive the gauntlet. If you can't write the rule down such that two people get the same trade, you can't test it, and if you can't test it, it stays ❌.

## Try it yourself

The exercise *is* the lesson: try to encode an Elliott count as a deterministic function of past prices only. You'll find every interesting decision (which swing starts wave 1, is this wave 4 or a new impulse) requires future information or a discretionary call. That irreducible subjectivity is why it can't clear [`deflate`](https://github.com/raphael2025/deflate) — there's nothing fixed to deflate.

## Sources

- Wikipedia — *Elliott wave principle*, *Technical analysis*.
- Elliott, R. N., *The Wave Principle* (1938); Frost & Prechter, *Elliott Wave Principle* (1978).
- Academic critiques of Elliott Wave's unfalsifiability and forecasting record (see *Technical analysis* references).
