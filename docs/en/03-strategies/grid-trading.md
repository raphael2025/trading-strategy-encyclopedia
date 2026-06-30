# Grid Trading

> One-line: place a ladder of buy orders below and sell orders above current price, harvesting the spread as price oscillates within a range. **Verdict: ❌ in a trend (the trend runs you over); 🔶 only as range-bound, inventory-managed market making.**

## What it is

Grid trading lays a grid of limit orders across a price band: buy a slice on each step down, sell a slice on each step up. In a sideways market each completed buy-low/sell-high pair books a small profit, and the bot keeps cycling. Popular crypto bots (3Commas, exchange-native grid bots) automate it, often with `pyramiding`-style accumulation (many open positions at once) and sometimes a martingale add-on (increasing size on each further dip) — which dramatically raises blow-up risk.

## The claim

That you don't need to predict direction — you just need volatility within a range, and the grid monetizes the chop. Marketed as "set and forget passive income," especially for ranging alts.

## The test

This is the same animal as [liquidity provision / mean reversion](mean-reversion.md), and it carries the same verdict in the [Verdict Index](../00-verdict-index.md): **❌ in a trend — worse than flat, because the trend runs you over.**

- **Asymmetric payoff against a trend.** A grid sells its winners cheaply (closes longs on small bounces) and *accumulates* its losers (keeps buying all the way down). In crypto's strongly-trending regime that means you're long an ever-larger bag into a sustained decline — catching a falling knife with leverage. The small range profits are dwarfed by the one trend that breaks the band.
- **No directional edge, and cost on every rung.** Each fill pays fees/slippage; the strategy needs the range to oscillate enough to cover that turnover, and ranges don't announce themselves in advance. You only know it was "range-bound" in hindsight ([look-ahead](../../../METHODOLOGY.md)).
- **Martingale tail.** The add-on that makes the equity curve look smooth (buy more as it drops) is precisely what converts a drawdown into a liquidation.

## Verdict: ❌ (🔶 only as genuine range market making)

As a retail "passive income" bot, grid trading is ❌: it profits in calm ranges and then gives it all back (plus more) in the trend that eventually arrives, while paying cost on every rung. The *only* defensible version is professional, inventory-managed market making in a genuinely mean-reverting instrument with maker rebates and hard inventory/risk limits — which is 🔶 Conditional, latency- and rebate-dependent, and not the retail grid bot. If you want a non-directional crypto edge that actually survives, it's [funding carry](../08-crypto-specific/funding-rate-carry.md), not a price grid.

## Try it yourself

Backtest a grid across both a ranging window and a trending window with cost on every fill, and run [`deflate`](https://github.com/raphael2025/deflate) `bootstrap` (to see the fat left tail from the trend leg) and `placebo`. The ranging-only result is survivorship bias; over a full sample including trends, net-of-cost returns go negative.

## Sources

- This repo's [mean reversion](mean-reversion.md) entry — grid is mean reversion / liquidity provision in disguise; same falsification.
- TradingView Pine Script v5 — Strategies manual (grid uses `strategy.order()` with `pyramiding`): https://www.tradingview.com/pine-script-docs/en/v5/concepts/strategies/
- This repo's [funding-rate carry](../08-crypto-specific/funding-rate-carry.md) — the non-directional edge that *does* survive.
