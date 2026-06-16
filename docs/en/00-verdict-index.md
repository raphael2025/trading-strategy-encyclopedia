# The Verdict Index

Every strategy/indicator at a glance. Tags: ✅ Validated · ❌ Falsified · 🔶 Conditional · ⚠️ Untested.
**Asset focus:** crypto perpetuals (BTC/ETH/SOL) and US equities, retail-executable, costs included. See [METHODOLOGY](../../METHODOLOGY.md).

> Read this as: *"does the edge survive once you stop fooling yourself?"* For most of the famous stuff, the answer is no — and that itself is worth knowing, because it stops you from bleeding fees on folklore.

## Prediction & signals

| Strategy | Verdict | Evidence (one line) |
|---|---|---|
| Standalone technical indicators (RSI/MACD/Bollinger/MA cross) as buy-sell signals | ❌ | Five independent falsification methods; no out-of-sample edge after cost. |
| Intraday / mid-frequency (≤15m) direction prediction | ❌ | Turnover cost alone ≈ −86%/yr; the "signal" is dwarfed by fees. |
| Machine-learning price prediction (retail, K-line features) | ❌ | RankIC ≈ 0; placebo not rejectable; out-of-sample collapse. |

## "Smart money" & copy-trading

| Strategy | Verdict | Evidence |
|---|---|---|
| Copy / mirror top leaderboard wallets | ❌ | RankIC ≈ 0; survivorship bias; following large entries = being exit liquidity. |
| Smart-money "confluence" signals (multi-wallet same-side) | ❌ | No persistence; identity/quality scores have zero predictive power once de-biased. |

## Mean reversion, SMC / ICT

| Strategy | Verdict | Evidence |
|---|---|---|
| Mean reversion / "buy the dip" in a trend | ❌ | In crypto's trending regime = catching a falling knife. |
| Liquidity provision / grid in trend | ❌ | Worse than flat; trend runs you over. |
| Supply/demand zones (SMC) | ❌ | No edge vs matched-placebo entries. |
| Fair Value Gap (FVG) retest | ❌ | Event study, 36 tests across 3 coins × horizons: nothing survives multiple-testing + out-of-sample. |
| Liquidity-sweep reversal ("stop hunt" fade) | ❌ | Triggered returns net-negative after cost; no edge vs placebo. |

## Microstructure

| Strategy | Verdict | Evidence |
|---|---|---|
| Order Flow Imbalance / VPIN | 🔶 | RankIC ~0.29 is **real** — but it's a maker/sub-second/HFT edge. Retail taker nets ≈ −8bps. Not for you. |
| Spoofing/absorption detection | 🔶 | Informative for HFT; not executable edge for retail latency. |

## Market mechanics (real mechanism ≠ tradeable edge)

| Topic | Verdict | Evidence |
|---|---|---|
| Liquidity hunts / stop hunting (trade the sweep) | ⚠️ real / ❌ as timing | Liquidation cascades and stop pools are real; sweep-fade entries don't beat placebo and bleed on intraday cost. Useful only defensively. |
| Institutional manipulation, detect-and-trade | ⚠️ real / ❌ as signal | Spoofing/wash/P&D are documented; profitable detection is HFT-latency or post-hoc forensics, not a retail edge. |
| Wyckoff accumulation/distribution (spring/upthrust) | ❌ as timing / ⚠️ as lens | Phases only labelable in hindsight; subjective and crowded; persistence is better captured by trend following. |

## Chart patterns (extended)

| Pattern | Verdict | Evidence |
|---|---|---|
| Triangles / flags / wedges | ❌ | Hindsight "perfect-trade" stats + multiple-testing + 35–50% crypto false-breakout rate; only slow channel breakout (= trend following) survives. |
| Harmonic patterns (Gartley/Bat/Crab…) | ❌ | Fibonacci tolerance bands fit anything; leg-labeling needs the future; no mechanism, no placebo-beating evidence. |
| Elliott Wave | ❌ | Unfalsifiable, infinitely revisable counts; look-ahead; nothing objective to backtest or deflate. |

## Trend, momentum, carry (the survivors)

| Strategy | Verdict | Evidence |
|---|---|---|
| Trend following (dual moving average, let profits run) | ✅ | Sharpe ~1.1; ~36% win rate but ~6.5 payoff ratio — the edge is in *not* cutting winners. |
| Cross-sectional momentum + illiquidity (liquid universe) | ✅ | Multi-factor, top/bottom 20%; Sharpe ~1.2. |
| Funding carry (cash-and-carry: long spot / short perp) | ✅ | Near risk-free funding harvest; very high Sharpe, but real tail risk — size ≤20%. **The cleanest honest edge in crypto.** |
| Combined (trend + cross-sectional + carry), low mutual correlation | ✅ | Sharpe ~1.7, **DSR 0.93**, drawdown ~−22% — best risk-adjusted form. |
| Equal-weight buy-and-hold (quality equities) | ✅ | Sharpe ~1.11 — a brutally hard-to-beat baseline. Complexity must prove it beats *this*. |
| Pairs trading / statistical arbitrage | 🔶 | Real relative-value edge but decayed since ~2002; in crypto, cointegration is unstable, factor shocks hit both legs, and the pair-search overfits (DSR/PBO decisive). |
| Grid trading / leveraged average-down (DCA bot) | ❌ | Profits in a range then the trend runs you over while you accumulate the loser; cost per rung. Investor DCA (cash-flow/behavioral) is a separate ⚠️/🔶 tool. |

## Risk management & execution

| Topic | Verdict | Evidence |
|---|---|---|
| Position sizing / vol-targeting for drawdown control | ✅ | Drawdown is a near-linear dial: halve size → halve drawdown, Sharpe/Calmar ~invariant. **This is how you control risk** — not clever timing filters. |
| Wide ATR trailing stop | 🔶 | Helps: cuts catastrophic reversals while preserving the fat right tail trend-following needs. |
| Tight stops / early take-profit / resistance-level exits | ❌ | Cuts the few big winners → destroys the payoff ratio the whole edge depends on. |
| Leverage as an "edge amplifier" | ❌ | A bankruptcy switch, not a multiplier. 10% capital × 50× → zero on a normal wick. Stay ≤1×. |
| Low-timeframe "better entry" timing after a higher-TF signal | ❌ | Adds whipsaw + missed moves; underperforms just acting on the signal. |

## Equities factors

| Strategy | Verdict | Evidence |
|---|---|---|
| Mega-cap cross-sectional factors (momentum/value on large caps) | ❌ | DSR ≈ 0.004 — factors live in small/mid caps; mega-caps too efficient. |

---

### The meta-lesson

> Across an exhaustive search, **most of what traders believe is folklore that dies under honest testing.** What survives is boring: follow trends, harvest carry, diversify uncorrelated edges, control size, and respect that a simple buy-and-hold is a fierce competitor. **Restraint beats effort.** The value of this index isn't a strategy — it's *not wasting years (and fees) on the dead ones.*

Want to test your own strategy against this same gauntlet? → **[`deflate`](https://github.com/raphael2025/deflate)**
