# Stop-Losses

> One-line: protective exit rules meant to "cut losses and protect capital" — fixed/percentage stops, early take-profit, exiting at resistance, versus wide ATR-based trailing stops. **Verdict: ❌ Tight stops Falsified / 🔶 Wide ATR Conditional**.

## What it is

A stop is a pre-committed exit. Two very different families hide under the same word. **Tight stops** close the position after a small adverse move (a fixed percentage, a tick below support); their cousins are **early take-profit** (banking a small gain) and **exiting at a resistance level**. **Wide ATR trailing stops** sit far from price — a multiple of the Average True Range — and only fire on a large, structural reversal, ratcheting up as the trade works. The first family caps the *size* of any single move; the second family only catches *catastrophic* ones.

## The claim

That stops "cut losses short" and therefore protect capital. In retail teaching this is treated as unconditionally good: a tighter stop is presented as a safer, more disciplined trade.

## The test

We applied each stop type on top of the validated [trend-following](../03-strategies/trend-following.md) edge — a system that wins only **~36% of the time** but carries a **~6.5 payoff ratio** — with signals timestamped at bar close (no look-ahead) and costs internalized.

- **Tight stops / early take-profit / resistance exits = ❌.** They cut the few enormous winners *before* they mature. Because the entire expectancy lives in the fat right tail, amputating it converts a positive-expectancy system into a death-by-a-thousand-whipsaws system: you keep the 64% of small losses, throw away the rare wins that pay for them, and add turnover cost on top. The Sharpe collapses the moment a take-profit is bolted on.
- **Wide ATR trailing stop = 🔶 — it helps.** Set far enough out that ordinary noise can't reach it, it cuts the *catastrophic* reversal (the trend that violently rolls over) while leaving the right tail intact. It is tail insurance, not a profit rule.

## Verdict: ❌ Tight stops Falsified / 🔶 Wide ATR Conditional

The verdict splits entirely on **width**. The right question is never "stops good or bad?" but "does this stop amputate the right tail the edge depends on?" Tight stops do, and they are fatal to any fat-tailed momentum system; the killer is simple — **they destroy the payoff ratio**, which *is* the edge. A wide ATR trailing stop is conditional: it earns its keep as catastrophe protection, provided it's wide enough that normal volatility never trips it. Realistic expectation: do not reach for stops as your primary risk tool at all — the clean, mathematically reliable dial is [position sizing](position-sizing-and-vol-targeting.md), not exit timing. And note the trap: tight stops *feel* safe (they soothe [loss aversion](../05-psychology/cognitive-biases.md)) precisely while they bleed the strategy dry.

## Try it yourself

Run the validated trend system, then add (a) a tight percentage stop, (b) an early take-profit, and (c) a wide ATR trailing stop, costs internalized. Watch win rate rise and total return *fall* under (a)/(b) as the right tail is clipped, and watch (c) trim the worst drawdowns without gutting the big winners. Compare against simply lowering size via [vol-targeting](position-sizing-and-vol-targeting.md) — usually the better trade.

## Sources

- Kaminski, K. & Lo, A. W. (2014), "When Do Stop-Loss Rules Stop Losses?", *Journal of Financial Markets* — when stops help versus hurt.
- Moskowitz, Ooi & Pedersen (2012), "Time Series Momentum," *Journal of Financial Economics* — the fat-tailed payoff structure stops can amputate.
