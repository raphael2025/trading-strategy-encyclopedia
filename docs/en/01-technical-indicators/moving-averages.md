# Moving Averages & MA Crossovers

> One-line: smoothed averages of price (SMA/EMA) whose crossings — the "golden cross" and "death cross" — are sold as buy/sell signals. **Verdict: ❌ Falsified** (as a standalone, tuned crossover signal).

## What it is

A moving average smooths price over a lookback window. The two common forms:

```
SMA(N) = simple mean of the last N closes (equal weight)
EMA(N) = exponentially weighted mean (recent closes weighted more)
```

The crossover rule pairs a **fast** average with a **slow** one. When the fast crosses *above* the slow it's a **golden cross**; when it crosses *below* it's a **death cross**. The most quoted pair is 50/200.

## The claim

That a moving average filters out noise and reveals the underlying trend, so when the fast average overtakes the slow one momentum has flipped bullish (golden cross = buy), and when it drops below, bearish (death cross = sell). The 50/200 cross in particular is treated as a regime switch for the whole market.

## The test

We evaluated the MA crossover as a **standalone, mechanical entry rule** on crypto perpetuals (BTC/ETH/SOL) and equities, signals timestamped at bar close (no look-ahead), with **taker fees + slippage + funding internalized**. The (fast, slow) lengths were treated as a search grid so selection bias is measured honestly.

Findings, consistent with the index:

- **No out-of-sample edge after cost.** The in-sample "best" length pair did not carry to the out-of-sample split — the standalone-indicator family that fails **five independent falsification methods** in the [verdict index](../00-verdict-index.md).
- **Selection-aware death.** Searching length pairs inflates in-sample Sharpe, but the **Deflated Sharpe Ratio** (penalizing for how many pairs were tried) collapses toward zero and PBO is high — the in-sample-best pair is out-of-sample noise.
- **Costs dominate.** Crossovers whipsaw in range-bound markets; turnover cost alone is the same drag that sinks mid-frequency direction prediction (≈ **−86%/yr to fees**) on the faster pairs.
- **Doesn't beat placebo.** Crossover entries are indistinguishable from random entries matched on time-of-day and prevailing momentum.

## Verdict: ❌ Falsified

As a standalone, tuned crossover signal, the MA cross does not survive honest testing. The killer is **multiple-testing** (which pair? 50/200 is folklore-selected, not derived — and the in-sample-best pair doesn't generalize) plus **cost** (whipsaws in chop). "The golden cross is a buy" is selection-blind folklore.

**The crucial nuance — the indicator isn't evil, the framing is.** A moving average is a perfectly good *building block* of a validated [trend-following](../03-strategies/trend-following.md) system. The difference is everything about *how* it's used: validated trend following is **slow** (rides multi-month moves, not crossovers in chop), **cost-aware** (turnover budgeted), **selection-aware** (the parameter search is penalized, not cherry-picked), and lets winners run with asymmetric payoffs (Sharpe ~1.1, ~36% win rate, ~6.5 payoff ratio). The same raw ingredient (a smoothed price) lives inside both — only the standalone-tuned-signal framing dies here.

## Try it yourself

Generate long-on-golden-cross / short-on-death-cross entries on bar closes, subtract realistic taker cost per turn, then run the returns through [`deflate`](https://github.com/raphael2025/deflate): check `placebo` (vs. matched random entries), `deflated_sharpe` (penalize the (fast, slow) grid you searched), and `pbo` (does the in-sample-best pair survive out-of-sample?). The DSR/PBO step is the one that fails.

## Sources

- Classic technical-analysis references on simple/exponential moving averages and the 50/200-day cross (e.g. Murphy, *Technical Analysis of the Financial Markets*).
- Bailey & López de Prado (2014), "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality," *Journal of Portfolio Management*.
