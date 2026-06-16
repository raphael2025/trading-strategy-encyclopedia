# Mean Reversion ("Buy the Dip")

> One-line: assume price reverts to a mean — fade extreme deviations (z-score, Bollinger fade, "buy the dip"). **Verdict: ❌ Falsified** (as retail directional trading in crypto's trending regime).

## What it is

Mean reversion bets that price oscillates around some equilibrium and that large deviations from it tend to snap back. Mechanically: measure how far price has stretched from a rolling average — a z-score, a percentile, a band touch — and take the *opposite* side of the move. Price drops sharply below the mean, you buy ("oversold"); it spikes above, you sell ("overbought"). Retail packages this as "buy the dip."

## The claim

Overextensions are temporary. Panic and euphoria push price past fair value, liquidity providers step in to absorb the imbalance, and price reverts — so fading the extreme harvests a mean-reversion premium. It feels intuitive because every chart, in hindsight, is full of bounces.

## The test

We evaluated mechanical mean-reversion entries on crypto perpetuals (BTC/ETH/SOL): enter on extreme deviation from a rolling mean, with signals timestamped at bar close (no look-ahead) and **taker fees + slippage + funding internalized**. The deviation threshold was treated as a search grid so selection bias is measured honestly, and entries were compared against a matched placebo.

- **Net-negative after cost.** Fading extremes trades often and into the worst fills; turnover alone is corrosive (≈ −86%/yr territory on lower timeframes).
- **No edge vs placebo.** "Oversold" entries are statistically indistinguishable from random entries matched on time and momentum.
- **DSR collapses** once you account for the threshold search — the in-sample-best deviation level is out-of-sample noise, and PBO is high.

## Verdict: ❌ Falsified

In a trending regime, fading extremes is catching a falling knife: **oversold gets more oversold**, and the same persistent moves that pay [trend following](trend-following.md) run straight over the mean reverter — the two are mirror images, and crypto's regime favors the trend. The killer is the combination of **no edge vs placebo** and **cost**, with DSR finishing it off. Nuance worth keeping: mean reversion is *not* universally dead — in genuinely range-bound, market-neutral, statistical-arbitrage settings (cointegrated pairs, Ornstein–Uhlenbeck spreads) the reversion is structural and can be real. But as retail *directional* "buy the dip" in trending crypto, it is ❌. This is the same falling-knife dynamic that kills standalone [RSI](../01-technical-indicators/rsi.md) and [Bollinger Band](../01-technical-indicators/bollinger-bands.md) fades.

## Try it yourself

Generate long-on-oversold / short-on-overbought entries from a rolling z-score on bar closes, subtract realistic per-turn cost, then run through [`deflate`](https://github.com/raphael2025/deflate): `placebo` (vs. matched random entries), `deflated_sharpe` (penalize the threshold grid), `pbo`. The placebo and DSR steps are where directional dip-buying dies. To see the legitimate cousin, build a *spread* between two cointegrated assets and test reversion of the spread, not the price.

## Sources

- Ornstein, L. & Uhlenbeck, G. — the mean-reverting process underlying statistical-arbitrage spread models.
- Gatev, Goetzmann & Rouwenhorst (2006), "Pairs Trading: Performance of a Relative-Value Arbitrage Rule," *Review of Financial Studies* — where reversion legitimately lives (market-neutral, not directional).
- Bailey & López de Prado (2014), "The Deflated Sharpe Ratio," *Journal of Portfolio Management* — the selection-aware test the directional version fails.
