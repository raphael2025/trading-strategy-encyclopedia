# Methodology — how every verdict is reached

A strategy doesn't get a ✅ because it made money in one backtest. It gets a ✅ because it **survived a gauntlet designed to kill false positives.** Here's the gauntlet.

## Why most backtests lie

Three quiet killers turn a losing strategy into a beautiful equity curve:

1. **Look-ahead bias.** Using information that wasn't available at decision time — the #1 way SMC/pattern backtests cheat (e.g. marking a swing high "now" when you only *know* it's a high two bars later).
2. **Cost & slippage ignored.** Many edges are real on paper and gone after taker fees, funding, and slippage. A 15-minute signal can turn an annualized +X% into −86% purely on turnover cost.
3. **Multiple testing (the big one).** Try 200 parameter sets and the best one *will* look great — by luck. This is the difference between "found an edge" and "data-snooped noise." Most published backtests are the winner of an unreported search.

A naive backtest catches none of these. Our gauntlet is built to catch all three.

## The gauntlet

Every entry is evaluated on these, in order. **Failing a selection-aware check (DSR / PBO) forces a ❌ regardless of how pretty the curve is.**

| Check | What it catches | Tool |
|---|---|---|
| **No-look-ahead construction** | Look-ahead bias — signals are timestamped at the bar where they are *confirmed*, not where they originate | causal feature engine |
| **Cost-internalized returns** | Fee/slippage/funding death | realistic exchange specs |
| **Placebo / permutation test** | "Is this better than a random entry at the same time-of-day & momentum?" | `deflate.placebo` |
| **Out-of-sample split** | In-sample overfitting; does it hold on unseen data? | walk-forward |
| **Deflated Sharpe Ratio (DSR)** | **Multiple testing** — is the Sharpe still significant after penalizing for *how many things you tried*? | `deflate.deflated_sharpe` |
| **PBO (CSCV)** | Probability that the in-sample-best config is out-of-sample garbage | `deflate.pbo` |
| **Block bootstrap** | The *real* distribution of Sharpe & max-drawdown (not the single lucky path) | `deflate.bootstrap` |
| **Parameter plateau** | Is the good result a broad plateau (robust) or an isolated spike (overfit)? | grid surface |

> **Selection-aware vs selection-blind:** bootstrap, walk-forward and placebo are *selection-blind* — a curve cherry-picked from a 300-config search still fools them. Only **DSR and PBO know how many times you rolled the dice.** That's why a failing DSR/PBO is an automatic ❌. This single insight is why most "validated" strategies elsewhere are not.

All of this is implemented in the open-source **[`deflate`](https://github.com/raphael2025/deflate)** library. Every verdict here links to the test that produced it — **you can reproduce it.**

## The honesty rules of this repo

- **We publish failures.** A source that only shows winners is marketing.
- **Claims need evidence.** No verdict without a reproducible test. Undocumented = `⚠️ Untested`, not `✅`.
- **"Validated" ≠ "will make you money."** It means *survived these tests on history*. Edges decay; markets adapt; the future is out-of-sample.
- **We synthesize and cite, never copy.** Sources are linked.

## What we deliberately do NOT publish

A small number of edges we've validated are kept private (they decay if crowded). This repo is about giving you an honest **map of what's real vs. folklore** — not handing out a turnkey money machine, because that doesn't exist.
