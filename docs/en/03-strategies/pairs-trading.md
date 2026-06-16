# Pairs Trading & Statistical Arbitrage

> One-line: long one asset and short a cointegrated partner, betting the spread mean-reverts; market-neutral by construction. **Verdict: 🔶 Conditional — a real institutional edge that has decayed sharply and is fragile in crypto.**

## What it is

Pairs trading finds two assets whose prices share a long-run equilibrium (cointegration, not mere correlation), models the spread `= log(P_A) − β·log(P_B)`, standardizes it to a z-score, and trades the extremes: when `z` is high, short the outperformer and long the laggard; when `z` reverts toward 0, close. Because the legs offset, the book is roughly market-neutral. Statistical arbitrage generalizes this to many assets via cointegration baskets, PCA residuals, or an Ornstein-Uhlenbeck spread model (half-life `= ln 2 / κ`).

## The claim

That relative value is more stable than direction: two related assets may both rise or fall, but the *gap* between them oscillates predictably, giving a high-hit-rate, low-beta return stream uncorrelated with the market.

## The test

The edge is real but two things degrade it — time and crypto.

- **Decay.** The classic evidence (Gatev, Goetzmann & Rouwenhorst 2006: US stocks 1962–2002, ~11%/yr on six-month pairs) measured a premium that *largely closed after the early 2000s* as the trade got crowded (Do & Faff document the decline). What survives is thinner and more competitive — an institutional, execution-sensitive edge, not free money.
- **Crypto fragility.** Cointegration here is weak and unstable: BTC-derivative/alt pairs typically cointegrate only ~0.5–0.8, and the relationship *breaks* exactly when it matters — around halvings, listings, regulatory shocks, and de-pegs. Common-factor moves (the whole market dumps together) leave the spread flat while you take absolute losses on both legs. The short leg pays/earns funding on a perp, adding cost and a [funding-reversal](../08-crypto-specific/funding-rate-carry.md) risk. Liquidity in the weaker leg can vanish when you need to exit.
- **Selection.** Scanning hundreds of candidate pairs for the best historical cointegration is a multiple-testing exercise; the "best" pair is often the luckiest one, and **Deflated Sharpe / PBO** are the relevant checks — many crypto pairs that look great in-sample are out-of-sample garbage.

## Verdict: 🔶 Conditional

Pairs trading / stat-arb is a *genuine* relative-value edge — the cleanest non-directional idea after [carry](../08-crypto-specific/funding-rate-carry.md) — but it is **conditional**: it has decayed in equities since ~2002, and in crypto it's fragile (unstable cointegration, factor-shock risk, funding cost, thin exit liquidity) and easy to overfit across the pair-search. It can work for a disciplined desk with cheap execution, robust cointegration tests, hard stop-out on spread blowouts (> some σ) and on cointegration p-value breaks, and selection-aware validation. It is not a reliable retail "high-win-rate" machine.

## Try it yourself

Select pairs by cointegration (Engle-Granger ADF on residuals, or Johansen), trade a z-score band, internalize taker cost *and* funding on the short perp leg, then run [`deflate`](https://github.com/raphael2025/deflate) `deflated_sharpe` and `pbo` **penalizing the number of pairs you screened** — this is where most crypto stat-arb dies. Use `bootstrap` to see the spread-blowout tail.

## Sources

- Gatev, Goetzmann & Rouwenhorst (2006), "Pairs Trading: Performance of a Relative-Value Arbitrage Rule," *Review of Financial Studies* 19(3).
- Do & Faff, "Does Simple Pairs Trading Still Work?" — documents post-2002 decay.
- Avellaneda & Lee (2010), "Statistical Arbitrage in the US Equities Market," *Quantitative Finance* 10(7); Vidyamurthy, *Pairs Trading* (2004).
- Wikipedia — *Pairs trading*, *Cointegration*, *Ornstein–Uhlenbeck process*.
