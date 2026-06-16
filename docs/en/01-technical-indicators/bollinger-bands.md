# Bollinger Bands

> One-line: a moving average wrapped in volatility-scaled bands, read either as a "fade the edge" reversion signal or a "squeeze breakout" signal. **Verdict: ❌ Falsified** (as a standalone reversion signal).

## What it is

Bollinger Bands, developed by John Bollinger in the 1980s, plot a moving average with an envelope set by recent volatility:

```
middle band = SMA(20)
upper band  = SMA(20) + 2 × stdev(20)
lower band  = SMA(20) − 2 × stdev(20)
%B          = (price − lower) / (upper − lower)      (where price sits in the band)
bandwidth   = (upper − lower) / middle               (how wide the band is)
```

Two contradictory folklore readings: **(a) mean-reversion** — price touching the upper band is "overbought, sell"; touching the lower band is "oversold, buy" (fade the edge). **(b) squeeze breakout** — when bandwidth collapses to a multi-period low, a big directional move is "loading," so trade the break *out* of the band.

## The claim

That ±2 standard deviations contains "most" of the price action, so a touch of the outer band is a statistically stretched move that should snap back (reversion); or, conversely, that a narrow band (low volatility) precedes an expansion, so the breakout from a squeeze is tradeable.

## The test

We evaluated **both** readings as standalone mechanical rules on crypto perpetuals (BTC/ETH/SOL) and equities, signals at bar close (no look-ahead), with **taker fees + slippage + funding internalized**. The (period, num_std) parameters were treated as a search grid.

Findings, consistent with the index:

- **No out-of-sample edge after cost.** The in-sample "best" (period, num_std) did not carry out-of-sample — the standalone-indicator family that fails **five independent falsification methods** in the [verdict index](../00-verdict-index.md).
- **Selection-aware death.** Searching the band parameters inflates in-sample Sharpe, but the **Deflated Sharpe Ratio** collapses toward zero and PBO is high. The two contradictory interpretations make this worse: you can *always* fit one of them in-sample, which is exactly the kind of flexibility DSR/PBO is designed to punish.
- **Costs dominate.** Band touches and breakouts fire often enough that turnover cost alone is the same drag (≈ **−86%/yr to fees**) that sinks faster strategies.
- **Doesn't beat placebo.** Band-touch entries are indistinguishable from random entries matched on time-of-day and prevailing momentum.

## Verdict: ❌ Falsified

As a standalone reversion signal, Bollinger Bands do not survive honest testing. The killer is **multiple-testing** (the 20/2 defaults are folklore-tuned, *and* having two opposite interpretations guarantees one fits any in-sample window) plus **cost**. Fading the band touch is the same falling-knife problem that kills [mean reversion](../03-strategies/mean-reversion.md): in a real trend, price rides the upper band for weeks, and "sell the touch" hands you the losing side.

The breakout reading (b) is a different question — squeeze→breakout is treated as 🔶 **Conditional** under [breakout](../03-strategies/breakout.md), where it survives only inside a cost-aware, selection-aware framework, not as a tuned band rule on its own.

## Try it yourself

Generate fade-the-band (long lower / short upper) entries on bar closes, subtract realistic taker cost per turn, then run the returns through [`deflate`](https://github.com/raphael2025/deflate): check `placebo` (vs. matched random entries), `deflated_sharpe` (penalize the (period, num_std) grid *and* the choice between the two interpretations), and `pbo` (does the in-sample-best config survive out-of-sample?). The DSR/PBO step is the one that fails.

## Sources

- Bollinger, John (2001), *Bollinger on Bollinger Bands* — the originator's own definition of the bands, %B and bandwidth.
- Bailey & López de Prado (2014), "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality," *Journal of Portfolio Management*.
