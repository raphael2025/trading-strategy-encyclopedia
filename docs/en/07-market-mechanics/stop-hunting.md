# Stop Hunting

> One-line: price is pushed just far enough to trip a cluster of stop-loss orders, whose forced market exits accelerate the move and let the instigator fill against them. **Verdict: ⚠️ Real mechanism, ❌ as a retail timing edge.**

## What it is

A stop-loss order converts to a *market* order the instant its trigger price prints. Retail traders cluster stops at the obvious places — just below a prior low, just above a prior high, on round numbers. That cluster is a visible pool of guaranteed market orders. "Stop hunting" is the practice of nudging price through that level so the stops fire, adding fuel to the move (long stops become market *sells*, deepening a drop), then trading against the resulting flow or fading the overshoot.

It is the most basic form of a [liquidity hunt](liquidity-hunts.md). In crypto it is amplified because stop liquidations and *leverage* liquidations stack at the same obvious levels, and because stop orders fill at *market* — in the thin liquidity a hunt deliberately creates, the realized fill is often far worse than the trigger.

## The claim

Two claims, often conflated:

1. **Defensive (true-ish):** "Don't put your stop where everyone else does, because it'll get tagged." This is sound risk hygiene.
2. **Offensive (the tradeable claim):** "Anticipate the hunt — wait for the stop sweep, then enter the reversal." This is the one that has to survive testing, and it doesn't.

## The test

The offensive version is exactly the **liquidity-sweep reversal / stop-hunt fade** already falsified in the [Verdict Index](../00-verdict-index.md): net-negative after cost, **no edge versus a matched-placebo** entry. The failure modes:

- **You can't label it in advance.** A stop sweep that reverses and a stop sweep that *keeps going* (a real breakout) look identical at the moment of the sweep. Calling it a "hunt" is a post-hoc label — pure look-ahead bias.
- **It's crowded.** If the level is obvious enough that you can see the stops, so can everyone else, and the fade is already in the price. There's nothing left to harvest.
- **Cost and slippage.** Fading a violent sweep means taking the trade in the worst possible liquidity, at taker fees, on a short horizon. Turnover cost alone (~−86%/yr territory for the fast versions, per the index) swamps any residual signal.

## Verdict: ⚠️ Real mechanism / ❌ as a timing edge

Stop hunting genuinely happens; understanding it is good *defense*. But "trade the stop hunt" is a falsified setup — the entries don't beat placebo and don't survive cost. The actionable takeaway is purely defensive: place stops at structurally meaningful (not crowd-obvious) distances, size by volatility so a normal wick doesn't tag you, and keep leverage low so you aren't *yourself* the liquidity being hunted. See [stop-losses](../06-risk-management/stop-losses.md) and [position sizing](../06-risk-management/position-sizing-and-vol-targeting.md) for how to do that correctly.

## Try it yourself

Reproduce as in [liquidity-hunts](liquidity-hunts.md): code a stop-sweep-fade on bar closes, internalize taker cost and realistic (wide) slippage, and run [`deflate`](https://github.com/raphael2025/deflate)'s `placebo` and `deflated_sharpe`. The placebo difference will not be significant.

## Sources

- Wikipedia — *Stop-loss order* — confirms stop orders convert to market orders at the trigger, so fills degrade in thin liquidity.
- Wikipedia — *Order book*, *Bid–ask spread* — why clustered orders are visible and why slippage spikes during a sweep.
- CoinGlass — *Liquidation Heatmap* (https://www.coinglass.com/LiquidationData) — where leverage-stop clusters sit (defensive use only).
