# Liquidity Hunts (Liquidity Grabs)

> One-line: large players push price into a known cluster of resting orders — stops, liquidations, breakout entries — to fill their own size against the flow they trigger. **Verdict: ⚠️ Real mechanism, ❌ as a retail timing edge.**

## What it is

A "liquidity hunt" (also *liquidity grab* or *stop hunt*) is the idea that well-resourced participants — market makers, prop firms, on-chain whales — deliberately drive price to a level where lots of orders are stacked, so that triggering those orders creates instant liquidity they can trade against. The targets are not random prices; they are *visible, predictable pools*: prior highs/lows, round numbers, and especially the liquidation prices of leveraged perpetual positions.

The mechanic that makes crypto special is the **perpetual-futures liquidation cascade**. With 50–125× leverage available, a small adverse move forces margin-call liquidations, each of which is a market order that pushes price further, triggering the next tier — a self-reinforcing "death spiral." On 19 May 2021, BTC fell ~30% in 24 hours (≈$43k → ~$30k) with over $8B liquidated in a day; the trigger was news (Tesla, China), but the *mechanism* that did the damage was forced deleveraging of leveraged longs.

## The claim

Proponents — largely the SMC/ICT (Smart Money Concepts) school — claim you can see where liquidity is pooled (liquidation heatmaps like CoinGlass, order-book depth, round numbers, the Asian-session range) and *trade the sweep*: wait for price to spike through the level, grab the stops, and reverse — then enter in the reversal direction for a high-probability move. The story extends to the "CME gap fill" (the weekend gap in CME BTC futures, claimed to fill >90% of the time) and the "London/New York sweep of the Asian range."

## The test

This site already tested the most concrete tradeable version of this idea — the **liquidity-sweep reversal ("stop-hunt fade")** — in the [Verdict Index](../00-verdict-index.md): triggered returns are net-negative after cost and show **no edge versus matched-placebo entries** at the same time-of-day and momentum. The related [Fair Value Gap retest](../00-verdict-index.md) failed an event study of 36 tests across 3 coins × horizons. The reasons generalize:

- **Look-ahead bias.** "Liquidity got grabbed and reversed" is only labelable *after* the reversal. Timestamped causally — at the moment price pierces the level — you cannot tell a hunt-and-reverse from a genuine breakout that keeps going. The "high win rate" is hindsight selection.
- **No edge vs placebo.** Once you compare sweep-fade entries to random entries matched on volatility regime and time-of-day, the excess return collapses. The level being "obvious" cuts both ways: everyone fades it, so the reversal is already priced.
- **Cost.** These are intraday, high-turnover trades. Taker fees + slippage (slippage is *worst* exactly in the thin liquidity a hunt creates) dominate any residual signal.

The mechanism is real — liquidation cascades, spoofed support, CME gaps all genuinely happen and are worth understanding defensively. What is false is the leap from *"this mechanism exists"* to *"I can time entries off it for a net edge."*

## Verdict: ⚠️ Real mechanism / ❌ as a timing edge

Liquidity hunts are a true, documentable feature of leveraged 24/7 markets — knowing they exist is valuable **risk management** (it tells you *where not to put your stop* and *why not to use high leverage*). But as a *signal generator* it fails the gauntlet: the labels require hindsight, the entries don't beat placebo, and intraday turnover bleeds them out on cost. Use the concept defensively (size down near dense liquidation zones, avoid stops at the obvious level, cut leverage into events) — not as a money-making setup.

## Try it yourself

Build a sweep-fade rule on bar closes: mark prior-N high/low, enter the fade when price pierces and closes back inside, internalize taker cost + realistic slippage, and run it through [`deflate`](https://github.com/raphael2025/deflate) — `placebo` (random entries matched on time/vol), `deflated_sharpe` (penalize the level/lookback grid), `pbo`. Expect the placebo difference to vanish and DSR to collapse. That null result *is* the lesson.

## Sources

- Wikipedia — *Perpetual futures*, *Order book*, *Stop-loss order*, *Open interest* — mechanics of liquidation, depth, and stop conversion.
- Wikipedia — *Spoofing (finance)*, *Layering (finance)* — how fake "support/resistance" walls are constructed and why they're illegal in regulated venues.
- CoinGlass — *Liquidation Data / Heatmap* (https://www.coinglass.com/LiquidationData) — the public liquidation-cluster map; useful for *defense*, not a signal.
- Cong et al. (2022), *Crypto Wash Trading*, NBER WP 30783 (https://www.nber.org/papers/w30783) — on manufactured volume.
