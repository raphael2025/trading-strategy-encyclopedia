# Head and Shoulders

> One-line: a three-peak reversal pattern (left shoulder, higher head, right shoulder) said to flip a trend when price breaks the "neckline." **Verdict: ❌ Falsified.**

## What it is

Head and Shoulders (H&S) is the most famous reversal pattern in technical analysis. In an uptrend it draws as three peaks: a **left shoulder**, a higher **head**, and a lower **right shoulder** roughly level with the left. A trendline connecting the two intervening troughs is the **neckline**. The rule: when price closes below the neckline, the uptrend is over, and the **price target** is the vertical height from head to neckline, projected down from the break point. The mirror image — **inverse H&S** — is the bullish bottoming version (three troughs, deepest in the middle, break above the neckline).

## The claim

That H&S is a *high-probability* reversal signal: the completed pattern plus a neckline break reliably marks a trend change, with a measurable, tradeable target. Published "win rates" of 70–80%+ circulate widely in retail material and pattern encyclopedias.

## The test

The decisive issue is **when you are allowed to know the pattern exists.** A right shoulder is only a right shoulder *after* later bars confirm it stopped rising; the "head" is only the head once you have bars on both sides; the neckline is only drawable after both troughs print. So the only causally honest trade is **entry at the confirmed neckline break, with every swing point timestamped at the bar that actually confirms it — never in hindsight.**

We detected H&S algorithmically (swing-point pivots, parametrized by shoulder symmetry tolerance and minimum head prominence) on crypto perpetuals (BTC/ETH/SOL) and equities, with:

- **No look-ahead.** Pivots confirmed only after the required lookforward bars; entries at the close of the neckline-break bar.
- **Costs internalized** (taker fees + slippage + funding).
- **Matched placebo:** post-break returns compared to random entries matched on time-of-day and prevailing momentum.

Findings:

- **The hindsight inflation is the whole effect.** Marking the pattern with future knowledge (the textbook way) produces the famous high win rates. Timestamped causally, post-break returns are **not distinguishable from the matched placebo**, and net of cost they are flat-to-negative.
- **Infinitely tunable = multiple testing.** How symmetric must the shoulders be? How deep the head? What neckline slope? Each knob is a search dimension; something always looks good in-sample. The **Deflated Sharpe Ratio** penalizes the family size and collapses toward zero; **PBO** is high.

## Verdict: ❌ Falsified

The killer is **look-ahead bias.** H&S "works" in the literature because the pattern is identified after the fact, when the reversal has already happened — the recognition borrows the answer. Once the swing points and neckline are timestamped at honest confirmation time, there is no edge versus matched-placebo entries, and cost finishes it off. Multiple-testing across the pattern's tunable definitions seals the verdict. This is the same failure mode as the rest of the [SMC / zones family](../00-verdict-index.md): supply/demand zones, FVG retests, and liquidity sweeps all die to causal timestamping plus placebo. See also [candlestick patterns](candlestick-patterns.md), where the dominant killer shifts to multiple-testing.

## Try it yourself

Detect H&S with a fixed pivot rule, confirm each swing only after its lookforward window, enter at the neckline-break close, and net out realistic cost. Then run it through [`deflate`](https://github.com/raphael2025/deflate): `placebo` (vs. matched random entries), `deflated_sharpe` (penalize the symmetry/depth/slope grid you searched), and `pbo`. The first thing to break is placebo — once timing is honest, the pattern carries no information the placebo doesn't.

## Sources

- Edwards & Magee, *Technical Analysis of Stock Trends* — the canonical reference defining H&S and the neckline target rule.
- Lo, Mamaysky & Wang (2000), "Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation," *Journal of Finance* — the rigorous academic treatment of algorithmic pattern detection.
- Bulkowski, *Encyclopedia of Chart Patterns* — extensive pattern statistics; note that win-rate figures are compiled from hindsight-identified patterns.
- Bailey & López de Prado (2014), "The Deflated Sharpe Ratio," *Journal of Portfolio Management*.
