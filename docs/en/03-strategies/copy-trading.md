# Copy Trading / Mirroring "Smart Money"

> One-line: mirror the trades of top leaderboard traders or tracked "smart money" wallets and ride their coattails. **Verdict: ❌ Falsified**.

## What it is

Copy trading turns someone else's positions into your signal. You pick traders from an exchange leaderboard, or you tag on-chain wallets that look sophisticated, and you replicate their entries and exits — either through a platform's auto-copy feature or by watching their fills and following. The "smart money confluence" variant goes further: when several tracked wallets take the same side at the same time, that agreement is treated as a stronger signal.

## The claim

Skill persists. If a trader topped the leaderboard or a wallet has a fat realized PnL, the reasoning goes, they have an edge you can borrow — so following them lets you free-ride on information, timing, or research you don't have. Confluence is sold as crowd-sourced conviction: many smart wallets, one direction, must mean something.

## The test

We ranked wallets and traders by historical performance, followed their forward entries, and measured the **forward predictive edge (RankIC)** of those rankings — de-biasing explicitly for survivorship, and accounting for the latency and slippage a real follower eats.

- **RankIC ≈ 0.** Past rank carries essentially no information about *forward* return. There is no persistence to follow.
- **Survivorship bias.** Leaderboards display today's lucky winners, not tomorrow's skilled ones; rank them yesterday and the cohort reshuffles.
- **You are the exit liquidity.** Following large entries means you fill *after* and *worse* than the trader; when they unwind, your copies are the orders they sell into.
- **Confluence adds nothing.** Multi-wallet agreement shows no forward persistence; identity and "quality" scores have **zero predictive power once de-biased**.

## Verdict: ❌ Falsified

The killer is a stack: **no persistence** (RankIC ≈ 0), **survivorship bias** (you're chasing realized luck), and **adverse selection** (you fill behind the leader and become their exit liquidity), all before latency and slippage finish the job. A ranking with zero forward information is not a strategy — it's a story told by the survivors. See the smart-money section of the [verdict index](../00-verdict-index.md) for the full de-biasing breakdown. The general lesson generalizes the individual-investor literature: visible past performance is a poor predictor of future performance, and copying it most reliably transfers *cost*, not edge.

## Try it yourself

Build a wallet/trader ranking from a *past* window, then compute the **RankIC** of that rank against *forward* returns on a held-out window with realistic follower latency and slippage applied to fills. Run it through [`deflate`](https://github.com/raphael2025/deflate) and watch the de-biased information coefficient sit at zero. Then repeat with a survivorship-corrected universe (include wallets that have since blown up) and watch any apparent edge disappear.

## Sources

- Barber, B. & Odean, T. (2000), "Trading Is Hazardous to Your Wealth," *Journal of Finance* — individual traders underperform; activity transfers wealth to costs.
- Carhart, M. (1997), "On Persistence in Mutual Fund Performance," *Journal of Finance* — top performers do not reliably persist.
- Brown, Goetzmann, Ibbotson & Ross (1992), "Survivorship Bias in Performance Studies," *Review of Financial Studies* — why leaderboards mislead.
