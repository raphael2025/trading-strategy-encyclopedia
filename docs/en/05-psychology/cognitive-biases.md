# Cognitive Biases in Trading

> One-line: the catalog of systematic mental errors — loss aversion, recency, overconfidence, FOMO — that traders are told to "master" in order to win. **Verdict: ⚠️ Not a signal** (useful for discipline, not prediction).

## What it is

A well-documented set of decision errors that recur in markets:

- **Loss aversion / the disposition effect** — sell winners too early, hold losers too long.
- **Recency bias** — over-weight the most recent bars and extrapolate them.
- **Confirmation bias** — seek evidence that supports the position you already hold.
- **Overconfidence** — over-trade and over-size after a good run.
- **Anchoring** — fixate on an entry price or a round number.
- **FOMO** — chase moves that have already happened.
- **Gambler's fallacy** — expect a reversal "because it's due."
- **Sunk-cost** — add to a loser to justify the original decision.

## The claim

The pop-trading framing is seductive: "master your psychology and you'll win." It treats emotional control as the missing edge — as if removing your biases would, on its own, produce a return stream.

## The test / the reality

There is nothing to backtest. **Knowing about confirmation bias is not a signal** — it does not generate entries, it has no RankIC, it cannot be scored selection-aware because it makes no prediction about price. Reframing the claim honestly dissolves it: psychology is not alpha.

But it is genuinely useful in the other direction — as **risk and process**, not prediction:

- The disposition effect is precisely the behavior that **destroys the [trend-following](../03-strategies/trend-following.md) payoff ratio**: cutting the rare ~6.5 payoff winners early (a ~36% win-rate strategy) amputates the fat tail that pays for everything. The bias attacks exactly the mechanism the edge depends on.
- Overconfidence and FOMO show up as over-sizing — neutralized by rules-based [position sizing & vol targeting](../06-risk-management/position-sizing-and-vol-targeting.md), not by willpower.
- The defense against all of them is **precommitment**: written rules, mechanical [stop-losses](../06-risk-management/stop-losses.md), and fixed sizing decided before the trade, when you are calm.

## Verdict: ⚠️ Not a signal (useful for discipline, not prediction)

The value of bias-awareness is **defensive**: it keeps you from sabotaging edges you already have. It is not **predictive**: it will never tell you what to buy. Be honest about which half you are using — confusing the two is itself a bias.

## Try it yourself

You can't backtest a bias, but you can backtest its *cost*. Take a validated trend-following return stream, then re-simulate it with a disposition-effect overlay — take profits early on winners, hold losers past the stop — and watch the Sharpe collapse as the payoff ratio erodes. Run both through [`deflate`](https://github.com/raphael2025/deflate). The behavioral leak is measurable even though the bias itself is not a signal.

## Sources

- Kahneman & Tversky (1979), "Prospect Theory: An Analysis of Decision under Risk," *Econometrica* — loss aversion.
- Odean (1998), "Are Investors Reluctant to Realize Their Losses?", *Journal of Finance* — the disposition effect.
- Barber & Odean (2000), "Trading Is Hazardous to Your Wealth," *Journal of Finance* — over-trading and overconfidence costs.
