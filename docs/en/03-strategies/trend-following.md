# Trend Following

> One-line: ride established trends — enter in the direction of persistent price movement and hold while it lasts, cutting losers and letting winners run. **Verdict: ✅ Validated** (a real but modest edge).

## What it is

Trend following is the oldest systematic style there is. The rules are deliberately simple: when price establishes a direction — measured by a slow moving-average relationship, or by breaking out of a prior range — you enter with the trend and stay in until the trend reverses. There is no profit target. The defining feature is **asymmetry**: you cut losing positions quickly and small, and you let winning positions run far. The signal is just plumbing; the edge lives entirely in that asymmetric exit logic.

## The claim

Markets trend because participants under-react to information, then herd into it: news diffuses slowly, risk managers add to working positions, and momentum feeds on itself. Proponents argue you don't need to predict anything — you just need to be positioned in the direction of the move and capture the **fat right tail** of the return distribution, where a handful of enormous winners pay for a long string of small losses.

## The test

We evaluated trend following on crypto perpetuals (BTC/ETH/SOL) and on equities, with signals timestamped at bar close (no look-ahead) and **taker fees + slippage + funding internalized**. We deliberately used a *slow* timeframe so turnover stays low enough to clear cost, and we required the parameters to sit on a **robustness plateau** — a broad region where nearby settings all work — rather than a lone spike that screams overfit. The whole configuration search was scored selection-aware.

- **Sharpe ≈ 1.1**, surviving Deflated Sharpe and PBO. This is a genuine, if unspectacular, edge — not a backtest artifact.
- **Win rate ≈ 36%, payoff ratio ≈ 6.5.** You lose roughly two trades out of three. The edge is *entirely* in the size of the rare winners.
- Because the edge is the payoff ratio, **tight stops and early take-profit destroy it** — they amputate the fat tail that pays for everything else (see [stop-losses](../06-risk-management/stop-losses.md)).

## Verdict: ✅ Validated

Trend following survives because it uses momentum the way it actually exists — as *persistence* you ride, not as an extreme you fade — and it is slow enough to clear cost and selection-aware enough that the DSR/PBO penalty doesn't kill it. Conditions: trade it slow, size by volatility ([position sizing & vol targeting](../06-risk-management/position-sizing-and-vol-targeting.md)), and never clip the winners. Realistic expectation: many small losses, long flat stretches, and a few large wins that arrive unpredictably — psychologically brutal to hold. Honesty check: a Sharpe of ~1.1 only marginally beats equal-weight buy-and-hold of quality equities (Sharpe ~1.11), so trend following earns its place by diversification, not by dominance.

## Try it yourself

Build a slow directional signal on bar closes, hold with no profit target until reversal, subtract realistic per-turn cost, then run the returns through [`deflate`](https://github.com/raphael2025/deflate): check `deflated_sharpe` (penalize every parameter you scanned), `pbo` (does the in-sample-best survive out-of-sample?), and `placebo`. It should clear all three — and watch the Sharpe collapse the moment you add a take-profit. Combine with [cross-sectional momentum](cross-sectional-momentum.md) and funding carry for the low-correlation version that reaches Sharpe ~1.7.

## Sources

- Moskowitz, Ooi & Pedersen (2012), "Time Series Momentum," *Journal of Financial Economics* — the academic backbone of trend following.
- Hurst, Ooi & Pedersen / AQR, "A Century of Evidence on Trend-Following Investing" — long-horizon, multi-asset robustness.
- Covel, M., *Trend Following* — popular synthesis of the practitioner tradition.
