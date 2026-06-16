# Dollar-Cost Averaging (DCA)

> One-line: invest a fixed amount on a fixed schedule regardless of price, smoothing your entry over time. **Verdict: ⚠️/🔶 — a sound behavioral/cash-flow tool, not an alpha source; "DCA bots" that average *down* into a position are a different, riskier thing.**

## What it is

There are two distinct things called "DCA," and conflating them causes most of the confusion:

1. **Investor DCA (the real one).** You have an income stream and invest a fixed dollar amount every period (e.g., $X every week) into a held basket. It's a *deployment schedule* for new cash, layered on top of [buy-and-hold](buy-and-hold.md).
2. **Trading-bot "DCA" (average-down).** A position is opened and then *added to* at lower prices to improve the average entry, expecting a bounce to exit the whole stack in profit. This is averaging into a loser — mechanically a martingale/grid cousin.

## The claim

For investor DCA: that splitting entries over time reduces timing risk and the impact of buying at a single bad price, and removes the emotional paralysis of "is now the right moment?" For bot DCA: that averaging down guarantees a profitable exit on any bounce.

## The test

These get opposite verdicts because they're different strategies.

- **Investor DCA vs lump-sum.** As an *edge*, DCA loses to lump-sum on average: markets drift up, so deploying gradually keeps cash idle and gives up expected return (studies repeatedly show lump-sum beats DCA the majority of the time). So DCA is **not alpha.** Its genuine value is (a) matching real cash flows — you invest as you earn — and (b) [behavioral](../05-psychology/cognitive-biases.md): a fixed schedule defeats the timing anxiety and FOMO/panic that wreck discretionary entries. On a no-look-ahead, cost basis it neither helps nor hurts the *return* much; it helps the *behavior*, which is real but not a backtestable price edge.
- **Bot average-down.** This is the dangerous one and it lands with [grid trading](grid-trading.md): ❌ in a trend. Adding size as price falls makes the equity curve look smooth right up until the move doesn't bounce, at which point you're maximally long into the worst outcome — a liquidation, especially with leverage.

## Verdict: ⚠️/🔶 (investor DCA) — ❌ (leveraged average-down)

Investor DCA is a legitimate, low-cost *discipline and cash-flow* tool — 🔶/⚠️: it won't beat lump-sum on expectation, but it reliably beats the *real-world alternative* of trying to time entries and flinching. Use it to deploy income into a [held basket](buy-and-hold.md). The trading-bot "average down into a position" version is a different, leverage-sensitive bet that fails the same way grids do — don't confuse the two.

## Try it yourself

Compare lump-sum vs periodic DCA deployment of the same capital over many rolling windows with [`deflate`](https://github.com/raphael2025/deflate) `bootstrap`; lump-sum's mean return is higher, DCA's entry-price variance is lower. Separately, simulate a leveraged average-down bot across a full sample including trends — the left tail is the story.

## Sources

- Constantinides (1979) and Vanguard, "Dollar-cost averaging just means taking risk later" — lump-sum beats DCA on average.
- This repo's [buy-and-hold](buy-and-hold.md) (what DCA deploys into) and [cognitive biases](../05-psychology/cognitive-biases.md) (the behavioral value).
- This repo's [grid trading](grid-trading.md) — the average-down bot's true family and failure mode.
