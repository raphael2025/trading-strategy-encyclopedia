# Fear & Greed Index

> One-line: a 0–100 sentiment composite labeled "extreme fear" to "extreme greed," sold as a contrarian timing signal — buy fear, sell greed. **Verdict: ❌ Falsified** (as a buy/sell signal).

## What it is

A single index, popularized for both crypto and equities (CNN / Alternative.me style), that blends several inputs into one number from 0 to 100: recent **volatility**, price **momentum**, **social/survey sentiment**, market **dominance/breadth**, and sometimes options or safe-haven demand. The reading is bucketed into labels from *extreme fear* through *neutral* to *extreme greed*.

## The claim

Pure contrarianism: "be greedy when others are fearful, and fearful when others are greedy." Extreme fear is supposed to mark capitulation bottoms (buy), extreme greed to mark euphoric tops (sell). The index is presented as a market-timing trigger.

## The test

We treated the extreme-fear and extreme-greed thresholds as **entry signals** on BTC and on equities, with readings timestamped causally (no look-ahead), **taker fees + slippage + funding internalized**, the threshold treated as a **search grid** (since "extreme" is a tunable cutoff), and the result compared against a matched **placebo** and against buy-and-hold.

- **The index is largely a lagging transform of recent price and volatility** — "greed" *is* high recent returns, "fear" *is* a recent drawdown plus high vol. Using it to time entries is therefore close to circular: you are conditioning on the move you wanted to predict.
- The thresholds are **tunable**, so an in-sample "best" cutoff is guaranteed; under selection-aware scoring that edge deflates.
- **Net of cost it does not beat the placebo, nor buy-and-hold.** Buying "extreme fear" in a downtrend is the same falling-knife problem that sinks [mean reversion / buying the dip](../03-strategies/mean-reversion.md).

## Verdict: ❌ Falsified

As a standalone, cost-aware **buy/sell signal**, the Fear & Greed Index does not survive: it is lagging and largely circular, its thresholds invite multiple-testing, and after cost it adds nothing over placebo or simply holding. The killer is that the index *is* a repackaging of recent price/vol — so as a timing tool it predicts the past.

**Honest positive:** it is a perfectly fine **descriptive thermometer**. As a risk thermostat — trim size when the gauge is pinned at euphoria, expect fragility at extremes — it is a sensible discipline aid, the same defensive use described in [cognitive biases](cognitive-biases.md) and operationalized through [position sizing & vol targeting](../06-risk-management/position-sizing-and-vol-targeting.md). A thermometer, not a trigger.

## Try it yourself

Pull the historical index, define entries at your chosen extreme thresholds, internalize cost, and run the returns through [`deflate`](https://github.com/raphael2025/deflate): scan the threshold and let `deflated_sharpe` penalize the grid, check `pbo`, and compare against `placebo` and buy-and-hold. Then regress the index on trailing returns and realized vol — once you see how much of it is just *recent price*, the circularity is obvious.

## Sources

- Baker & Wurgler (2006), "Investor Sentiment and the Cross-Section of Stock Returns," *Journal of Finance* — sentiment and the cross-section.
- The index itself is a public composite (CNN Business / Alternative.me) of volatility, momentum, and survey/social inputs — methodology published by its providers.
