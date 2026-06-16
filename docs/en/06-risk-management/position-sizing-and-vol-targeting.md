# Position Sizing & Volatility Targeting

> One-line: size positions inversely to volatility so portfolio risk stays roughly constant, rather than holding a fixed quantity. **Verdict: ✅ Validated** (the legitimate way to control risk).

## What it is

Instead of betting a fixed number of contracts or a fixed dollar amount, you size each position so that its *expected risk* is constant. Concretely: estimate recent realized volatility, then scale exposure inversely — when an asset is calm you hold more, when it's wild you hold less — so the position's contribution to portfolio volatility hits a target (e.g. a fixed annualized vol, or a fixed fraction of capital risked per trade). The Kelly criterion sits underneath this idea: it gives the growth-optimal bet fraction, and in practice you run a *fraction* of full Kelly (half-Kelly or less) to trade away geometric growth for a far smoother path. Vol-targeting is the continuous, multi-asset generalization of that one dial.

## The claim

That sizing — not entry cleverness — is what controls drawdown and smooths the equity curve. A volatility-targeted book should keep its risk roughly stationary across regimes, and the operator should be able to dial total risk up or down without changing the underlying strategy.

## The test

We applied vol-targeting on top of the *validated* strategies ([trend following](../03-strategies/trend-following.md), cross-sectional momentum, funding carry), with no look-ahead in the vol estimate (sizing uses only past data) and costs internalized, then varied the size dial and measured drawdown against Sharpe and Calmar.

- **Drawdown is a near-linear dial.** Halve position size → roughly halve maximum drawdown. The relationship is close to proportional because, to first order, scaling every position by a constant scales the whole P&L path by that constant.
- **Risk-adjusted return is ~invariant.** Sharpe and Calmar stay essentially flat as you move the dial — you are changing the *scale* of returns and drawdowns together, not the ratio between them.
- **It adds survivability, not return.** Vol-targeting does not raise expected Sharpe; it makes the Sharpe you already have *holdable* through the noise, which is what actually lets a slow edge compound.

## Verdict: ✅ Validated

This survives because it isn't a prediction — it's an *identity about how risk scales*. There is no threshold to tune, no signal to overfit, nothing for the DSR/PBO machinery to punish; the result follows from arithmetic, not from a backtest that got lucky. That is exactly why it is more reliable than trying to time exits with clever filters: the filter has to be *right about the future*, whereas sizing only has to be *consistent*. Conditions: estimate vol causally (past data only), cap leverage (see [leverage](leverage.md)), and accept that this is a risk dial, not an alpha source. Realistic expectation: a smoother curve at a risk level you can actually live with — and the ability to hold a fat-tailed trend system through its long drawdowns instead of capitulating at the bottom.

## Try it yourself

Take a validated strategy's raw returns, scale each position by `target_vol / trailing_realized_vol` (using only past bars), and sweep the target. Plot max drawdown and Calmar against the target: drawdown should track the dial almost linearly while Calmar stays flat. There is nothing here to run through [`deflate`](https://github.com/raphael2025/deflate) for an *edge* claim — that's the point. Contrast this with [stop-losses](stop-losses.md), where tight stops claim to control risk but actually destroy the payoff ratio.

## Sources

- Kelly, J. L. (1956), "A New Interpretation of Information Rate," *Bell System Technical Journal* — the growth-optimal bet fraction.
- Thorp, E. O., "The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market" — fractional-Kelly in practice.
- Moskowitz, Ooi & Pedersen (2012), "Time Series Momentum," *Journal of Financial Economics* — volatility scaling inside a momentum book.
- AQR, "Volatility Targeting" research notes — drawdown and Sharpe behavior under vol-scaling.
