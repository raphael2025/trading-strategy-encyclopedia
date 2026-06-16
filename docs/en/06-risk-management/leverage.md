# Leverage

> One-line: borrowing to take exposure larger than your capital — perp leverage of 10×, 50×, sold as a way to multiply a good strategy's returns. **Verdict: ❌ Falsified** (as an "edge amplifier").

## What it is

Leverage lets you control a notional position several times your posted margin. On crypto perpetuals this is dialed explicitly — 10×, 50×, 100× — meaning a small slice of capital backs a large position, with the exchange's liquidation engine standing by to force-close you when your margin falls below maintenance. The pitch is arithmetic: if a strategy returns X, then 10× leverage "returns 10X."

## The claim

That leverage is a multiplier on the returns of a positive-edge strategy — a free amplifier that turns a modest Sharpe into a large one.

## The test

This one doesn't need a fresh backtest; it needs honest geometry, and the verdict follows from the structure of compounding and liquidation.

- **Leverage is multiplicative on the *bad* path too.** Put 10% of capital at 50× and a perfectly ordinary wick — a ~2% adverse move, which is *100% of the margined notional* — wipes that position to **zero**. You are liquidated before the thesis has any chance to play out.
- **Zero is absorbing.** A single liquidation is permanent; there is no recovery path from ruin. This is what separates leverage from sizing — sizing scales you down and lets you continue, leverage can end the game outright.
- **Negative geometric drift.** Volatility drag plus path dependence mean that high leverage has *negative expected geometric growth even on a positive-edge strategy*: the arithmetic mean climbs while the compounded (geometric) outcome falls toward ruin. The optimal leverage is bounded — by Kelly — and retail "50×" sits orders of magnitude past that bound.

## Verdict: ❌ Falsified

As an edge amplifier, leverage is falsified. The killer is **ruin / geometric drag**: a single liquidation is absorbing, and zero is permanent, so any strategy run at high leverage carries a probability of total loss that compounds against you regardless of its edge. Leverage is a *bankruptcy switch, not a multiplier*. Conclusion: stay at **≤1×**, or a modest fractional-Kelly fraction at most. If you want more or less risk, that is what [position sizing & vol-targeting](position-sizing-and-vol-targeting.md) is for — sizing scales risk *and* survives; leverage scales risk *until it doesn't*. Even the cleanest crypto edge, [funding carry](../08-crypto-specific/funding-rate-carry.md), is sized to ≤20% of capital rather than levered to the moon, and the [liquidation mechanics](../08-crypto-specific/perpetuals-and-liquidations.md) are exactly why.

## Try it yourself

Take any positive-edge return stream and simulate it at 1×, 5×, 25×, 50×, including a liquidation rule (position dies if cumulative adverse move exceeds 1/leverage). Plot the *median* terminal wealth, not the mean: the mean is dragged up by impossible lucky paths while the median marches to zero as leverage rises. That gap between mean and median *is* volatility drag, and it is why leverage is not an amplifier.

## Sources

- Kelly, J. L. (1956), "A New Interpretation of Information Rate," *Bell System Technical Journal* — the bounded, growth-optimal leverage.
- Thorp, E. O., "The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market" — why running above optimal fraction lowers growth.
- Standard references on volatility drag and the gap between arithmetic and geometric mean returns.
