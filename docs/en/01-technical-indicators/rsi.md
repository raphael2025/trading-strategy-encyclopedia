# RSI (Relative Strength Index)

> One-line: a 0–100 momentum oscillator that's supposed to flag "overbought" (>70) and "oversold" (<30) conditions. **Verdict: ❌ Falsified** (as a standalone buy/sell signal).

## What it is

RSI, introduced by J. Welles Wilder in 1978, measures the speed and magnitude of recent price changes. Over a lookback window (classically 14 periods) it computes the ratio of average up-moves to average down-moves and maps it to a 0–100 scale:

```
RS  = (average gain over N) / (average loss over N)
RSI = 100 − 100 / (1 + RS)
```

The folklore reading: RSI > 70 = "overbought, sell"; RSI < 30 = "oversold, buy." Variants add divergence (price makes a new high, RSI doesn't), centerline (50) crosses, and tuned thresholds.

## The claim

That an extreme RSI reading marks a stretched market about to revert, so fading the extreme (buy oversold / sell overbought) earns a mean-reversion premium. It is one of the most widely taught "entry signals" in retail trading.

## The test

We evaluated RSI as a **standalone, mechanical entry rule** on crypto perpetuals (BTC/ETH/SOL) and equities, with signals timestamped at bar close (no look-ahead), and **taker fees + slippage + funding internalized** in the returns. The threshold pair (the 30/70 levels) and the lookback N were treated as a search grid so we could measure selection bias honestly.

Findings, consistent with the index:

- **No out-of-sample edge after cost.** The in-sample "best" threshold/lookback did not carry to the out-of-sample split. This is the standalone-indicator family that fails **five independent falsification methods** in the [verdict index](../00-verdict-index.md).
- **Selection-aware death.** Tuning the thresholds inflates in-sample Sharpe, but the **Deflated Sharpe Ratio** (which penalizes for how many threshold/lookback combinations were tried) collapses toward zero. PBO is high — the in-sample-best config is out-of-sample noise.
- **Costs dominate.** On the lower timeframes where RSI fires most often, turnover cost alone is brutal — the same regime where mid-frequency direction prediction loses ≈ **−86%/yr to fees** before any "signal" is even discussed.
- **Doesn't beat placebo.** RSI entries are not distinguishable from random entries matched on time-of-day and prevailing momentum.

## Verdict: ❌ Falsified

As a standalone buy/sell signal, RSI does not survive honest testing. The killer is a combination of **multiple-testing** (the famous 30/70 levels are a tuned choice that doesn't generalize) and **cost** (it trades too often to clear fees). It is a *descriptive* transformation of recent returns — useful for talking about a chart — but it carries no exploitable, cost-surviving directional information on its own. Note the asymmetry: in a strong trend, "overbought" stays overbought for weeks, and fading it is exactly the falling-knife behavior that kills [mean reversion](../03-strategies/mean-reversion.md).

This is a verdict on RSI *alone as a signal* — not a claim that momentum information is worthless. The survivors ([trend following](../03-strategies/trend-following.md), [cross-sectional momentum](../03-strategies/cross-sectional-momentum.md)) use momentum the opposite way (ride it, don't fade it) inside a cost-aware, selection-aware framework.

## Try it yourself

Compute RSI(14) on bar closes, generate long-on-oversold / short-on-overbought entries, subtract realistic taker cost per turn, then run the returns through [`deflate`](https://github.com/raphael2025/deflate): check `placebo` (vs. matched random entries), `deflated_sharpe` (penalize the threshold grid you searched), and `pbo` (does the best in-sample threshold survive out-of-sample?). The DSR/PBO step is the one that fails.

## Sources

- Wilder, J. Welles (1978), *New Concepts in Technical Trading Systems* — the original RSI definition.
- Bailey & López de Prado (2014), "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality," *Journal of Portfolio Management*.
- Bailey, Borwein, López de Prado & Zhu (2017), "The Probability of Backtest Overfitting," *Journal of Computational Finance* (PBO/CSCV).
