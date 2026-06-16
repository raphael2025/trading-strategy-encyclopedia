# Perpetuals & Liquidations

> One-line: how perpetual futures and their liquidation engines actually work — the playing field that makes funding carry possible and leverage lethal. **Verdict: ⚠️ Reference** (mechanics, not a strategy).

## What it is

A **perpetual future** ("perp") is a futures contract with no expiry date. Without a settlement date to anchor it to spot, the exchange uses the **funding rate** — a periodic payment between longs and shorts — to keep the perp price tethered to the underlying. Key mechanics:

- **Mark price vs. last price.** Liquidations and unrealized P&L are computed against a *mark price* (an index-anchored, manipulation-resistant reference), not the last traded print, so a single thin trade can't unfairly liquidate you.
- **Initial vs. maintenance margin.** Initial margin opens the position; maintenance margin is the floor. Drop below maintenance and you are liquidated.
- **Liquidation.** When margin falls below maintenance the engine force-closes the position into the market.
- **Cascades, ADL, insurance fund.** Forced selling pushes price further, triggering more liquidations — a **cascade**. An **insurance fund** absorbs shortfalls; when it can't, **auto-deleveraging (ADL)** closes winning counterparties to balance the book.

## The claim

None. This page is mechanism science — it describes the field of play so the verdicts elsewhere make sense, not a tradeable signal.

## The test

What's *measurable* here, rather than a strategy to validate:

- **Funding is real and harvestable.** It is an exchange-paid cash flow, which is what the validated [funding carry](funding-rate-carry.md) monetizes.
- **Liquidation clusters are real market events.** Cascades genuinely move price on short horizons — they are observable, not folklore.

But observability is not edge. Understanding perps and liquidations does **not** by itself hand you a signal. Naively "trading the liquidation levels" or hunting stop clusters does not survive honest testing — order-flow/[OFI](../04-microstructure/order-flow-imbalance.md) information is largely maker-only and arrives too late for a taker, and stop-hunt fades fail their falsification tests. What the mechanics *do* explain is the two things that matter: **why funding carry works** (the perp must be tethered, so someone pays to hold the popular side) and **why leverage is a bankruptcy switch** (the liquidation engine closes you at a mark-price threshold, before any thesis resolves).

## Verdict: ⚠️ Reference

Treat this as a map of the terrain, not a route. Knowing how the mark price, margin tiers, and liquidation engine behave is what keeps you on the right side of [leverage](../06-risk-management/leverage.md) and lets you run [funding carry](funding-rate-carry.md) without getting wicked out of the short leg. It is mechanics you must understand to not get liquidated — and nothing more.

## Sources

- Exchange documentation on perpetual swap design and liquidation engines (e.g., the original BitMEX perpetual swap specification; current venue docs on mark price, margin tiers, insurance fund, and ADL).
- Academic notes on perpetual futures pricing and the role of the funding rate in tethering perp to spot.
