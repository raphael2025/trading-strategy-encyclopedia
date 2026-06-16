# Candlestick Patterns

> One-line: named one-, two-, and three-candle shapes (doji, hammer, engulfing, morning/evening star…) said to predict short-term reversals or continuation. **Verdict: ❌ Falsified** (as standalone signals).

## What it is

Candlestick patterns encode the relationship between a bar's open, high, low, and close into named shapes:

- **Doji** — open ≈ close (tiny body): "indecision."
- **Hammer / shooting star** — small body with a long lower/upper wick: rejected move.
- **Bullish/bearish engulfing** — a body that fully engulfs the prior body: "momentum flip."
- **Morning / evening star** — a three-candle reversal sequence.

The framework comes from Japanese rice traders and was popularized in the West by Steve Nison. Dozens of named patterns exist, often paired with "confirmation" rules (e.g., a follow-through close).

## The claim

That these specific shapes carry short-term predictive content — that, say, a hammer at a low reliably precedes a bounce and an evening star precedes a drop.

## The test

Each pattern was encoded as a **mechanical signal** on crypto perpetuals (BTC/ETH/SOL) and equities. One thing candlesticks get *right*: a candle is only complete at its close, so signaling at bar close is causally clean — **no look-ahead here** (unlike [head and shoulders](head-and-shoulders.md), where hindsight pivot-marking is the killer). The real problem is the **size of the family**: dozens of named patterns × tunable confirmation rules = a huge search surface. We treated the whole set as one selection-aware experiment, with **costs internalized** and entries compared against **matched placebo** (random entries matched on time-of-day and momentum).

Findings:

- **Something always looks good in-sample.** With this many patterns and confirmation variants, in-sample winners are guaranteed by chance alone.
- **DSR collapses the family.** Once the **Deflated Sharpe Ratio** penalizes how many patterns/rules were tried, the in-sample stars deflate toward zero; PBO is high.
- **No edge vs placebo after cost.** Net of fees, the patterns' triggered returns are statistically indistinguishable from the matched-placebo entries. The predictive content is ~zero.

## Verdict: ❌ Falsified

The killer here is **multiple-testing + cost + no edge vs placebo** — not look-ahead. As standalone reversal/continuation signals, candlestick patterns do not survive: deflate for the family size and net out cost, and the edge is gone. This is consistent with the academic finding that candlestick strategies add no value once data-snooping is accounted for.

A fair caveat: some patterns are merely *descriptive* — a doji genuinely describes a session that closed where it opened, and a long lower wick genuinely describes intrabar rejection. That's a legitimate vocabulary for narrating a chart. It is *not* a verdict-changing edge. We mark the topic ❌ for its primary use — as a tradeable signal — while acknowledging the descriptive role is harmless.

## Try it yourself

Encode each pattern as a close-confirmed signal, treat the full pattern list as one search family, net out realistic cost, and run [`deflate`](https://github.com/raphael2025/deflate): `placebo`, `deflated_sharpe` (this is the load-bearing test — it must penalize the *whole* family, not one pattern), and `pbo`. The DSR step is where the family dies.

## Sources

- Nison, *Japanese Candlestick Charting Techniques* — the origin and standard catalog of candlestick patterns.
- Marshall, Young & Rose (2006), "Candlestick technical trading strategies: Can they create value for investors?" *Journal of Banking & Finance* — finds no value after accounting for data-snooping.
- Bailey & López de Prado (2014), "The Deflated Sharpe Ratio," *Journal of Portfolio Management*.
