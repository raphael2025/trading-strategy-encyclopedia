# MACD (Moving Average Convergence Divergence)

> One-line: a momentum indicator built from the difference of two exponential moving averages, supposed to flag trend turns when its lines cross. **Verdict: ❌ Falsified** (as a standalone buy/sell signal).

## What it is

MACD, developed by Gerald Appel in the late 1970s, is a smoothed momentum transform. It tracks three series:

```
MACD line   = EMA(12) − EMA(26)        (fast EMA minus slow EMA of price)
signal line = EMA(9) of the MACD line
histogram   = MACD line − signal line
```

The folklore reading: a **bullish crossover** (MACD line crosses above the signal line) is a buy; a **bearish crossover** (crosses below) is a sell. Variants add **zero-line crosses** (MACD above/below 0) and **divergence** (price makes a new high, MACD doesn't).

## The claim

That the difference of a fast and a slow average measures shifting momentum, so the moment the fast component pulls away from the slow one you've caught a fresh trend early — buy the bullish cross, sell the bearish cross, and let the histogram confirm strength.

## The test

We evaluated MACD as a **standalone, mechanical crossover entry rule** on crypto perpetuals (BTC/ETH/SOL) and equities, signals timestamped at bar close (no look-ahead), with **taker fees + slippage + funding internalized**. The (12, 26, 9) parameters and a range of variants were treated as a search grid so selection bias is measured, not hidden.

Findings, consistent with the index:

- **No out-of-sample edge after cost.** The in-sample "best" parameter triple did not carry to the out-of-sample split — the same standalone-indicator family that fails **five independent falsification methods** in the [verdict index](../00-verdict-index.md).
- **Selection-aware death.** Tuning the three windows lifts in-sample Sharpe, but the **Deflated Sharpe Ratio** (penalizing for how many parameter sets were tried) collapses toward zero, and PBO is high — the in-sample-best config is out-of-sample noise.
- **Costs dominate.** MACD whipsaws relentlessly in chop, generating many round-trips; turnover cost alone is the same brutal drag that sinks mid-frequency direction prediction (≈ **−86%/yr to fees**).
- **Doesn't beat placebo.** Crossover entries are not distinguishable from random entries matched on time-of-day and prevailing momentum.

## Verdict: ❌ Falsified

As a standalone crossover signal, MACD does not survive honest testing. The killer is **multiple-testing** (the famous 12/26/9 are a tuned historical artifact — there is nothing special about those lengths, and they don't generalize) plus **cost** (crossovers fire constantly in sideways markets and bleed fees). MACD is a lagging, smoothed difference of two moving averages — structurally the same family as a [moving-average crossover](./moving-averages.md), and it dies the same way.

Note the important asymmetry: a **slow, cost-aware, selection-aware [trend-following](../03-strategies/trend-following.md) system** that happens to use moving averages can be ✅ (Sharpe ~1.1). That is *not* the same thing as "the MACD bullish cross is a buy." Trading the cross actively, on tuned defaults, fast enough to whipsaw, is selection-blind folklore — and that is what fails here.

## Try it yourself

Generate long-on-bullish-cross / short-on-bearish-cross entries on bar closes, subtract realistic taker cost per turn, then run the returns through [`deflate`](https://github.com/raphael2025/deflate): check `placebo` (vs. matched random entries), `deflated_sharpe` (penalize the (fast, slow, signal) grid you searched), and `pbo` (does the in-sample-best triple survive out-of-sample?). The DSR/PBO step is the one that fails.

## Sources

- Appel, Gerald — originator of MACD; see *Technical Analysis: Power Tools for Active Investors* (2005) for his own treatment.
- Bailey & López de Prado (2014), "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality," *Journal of Portfolio Management*.
