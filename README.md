<div align="center">

# Trading Strategies, Tested

### The only trading encyclopedia that tells you **what actually works** — with evidence.

**[English](README.md) · [中文](README.zh-CN.md) · [Русский](README.ru.md)**

</div>

---

Every trading strategy, indicator, and chart pattern — explained, then **rigorously tested** and given a verdict.

Most trading "knowledge" online tells you *how* a strategy works. Almost none tells you *whether it works*. This repo does. Every entry is run through a no-look-ahead backtest and an anti-overfitting gauntlet (placebo test, Deflated Sharpe, PBO, out-of-sample), and tagged with an honest verdict.

> **The uncomfortable truth we keep finding: most popular strategies don't survive once you account for costs, look-ahead bias, and the fact that you tried 200 things.** We show you the evidence either way.

## The verdict system

| Tag | Meaning |
|---|---|
| ✅ **Validated** | Survives out-of-sample + Deflated Sharpe + cost. A real, if usually small, edge. |
| ❌ **Falsified** | Looks good in a naive backtest; dies under placebo / OOS / cost / multiple-testing. |
| 🔶 **Conditional** | Real but only under specific conditions (e.g. maker-only, specific regime) — not for the average retail taker. |
| ⚠️ **Untested** | Documented for completeness; we haven't run it yet (PRs welcome). |

How we test (and how you can reproduce it): **[METHODOLOGY](METHODOLOGY.md)**. The validation toolkit is open source: **[`deflate`](https://github.com/raphael2025/deflate)** — point it at your own strategy's returns and find out if you're fooling yourself.

## 🔬 Going deeper — the evidence behind the verdicts

This repo now folds in three companion bodies of work:

- **[`machine-validated/`](machine-validated/)** — every verdict backed by a reproducible run through the full gauntlet (Deflated Sharpe, PBO/CSCV, walk-forward, block bootstrap). Includes the raw [verdict payloads](machine-validated/results/), per-strategy [reports](machine-validated/reports/), the [live execution PLAYBOOK](machine-validated/PLAYBOOK.md), and the [validation harness code](machine-validated/experiments/). *The honest punchline: across 16 machine-validated strategies, exactly one cleared every gate.*
- **[`knowledge-base/`](knowledge-base/)** — a deep crypto-perps trading knowledge system (技术分析 / 风控 / 市场机制 / 期权 / 链上 / 订单簿 / Alpha 挖掘), the reference layer under the verdicts.

> Together these answer not just *"does strategy X work?"* but *"what survives honest validation, and how do you build the gauntlet yourself?"*


## Start here

➡️ **[The Verdict Index — every strategy at a glance](docs/en/00-verdict-index.md)** — skip to the answer.

## Contents

- **[01 · Technical Indicators](docs/en/01-technical-indicators/)** — RSI, MACD, Bollinger, moving averages, 25+ indicators
- **[02 · Chart Patterns](docs/en/02-chart-patterns/)** — head & shoulders, triangles, harmonics, candlesticks
- **[03 · Strategies](docs/en/03-strategies/)** — trend following, mean reversion, momentum, breakout, grid, copy-trading
- **[04 · Market Microstructure](docs/en/04-microstructure/)** — order flow, OFI/VPIN, liquidity, spoofing
- **[05 · Trading Psychology](docs/en/05-psychology/)** — cognitive biases, fear/greed, discipline systems
- **[06 · Risk Management](docs/en/06-risk-management/)** — position sizing, vol targeting, leverage, drawdown control
- **[07 · Market Mechanics](docs/en/07-market-mechanics/)** — liquidity hunts, manipulation, stop runs
- **[08 · Crypto-Specific](docs/en/08-crypto-specific/)** — funding rates, basis/carry, perpetuals, liquidations

## Why trust this?

Because we publish our **failures**. We ran a large search across crypto strategies and most of what we tested — prediction signals, smart-money copying, technical indicators, retail order-flow — **failed honest validation**. We say so, with numbers. A source that only ever shows winners is selling you something. ([Read the philosophy →](METHODOLOGY.md#why-most-backtests-lie))

## Get the live verdicts & alerts

We publish objective market data (funding/carry opportunities, regime flips, liquidation events) — **facts, not price predictions** — in our community:

📲 **Telegram: [t.me/+E3UdPtwlISVhZDc1](https://t.me/+E3UdPtwlISVhZDc1)**  ·  🧪 **Validation tool: [`deflate`](https://github.com/raphael2025/deflate)**

## Contributing

Found a strategy we're missing? Open a PR. But the rule of this repo: **claims need evidence.** A strategy is `⚠️ Untested` until it's been through the gauntlet. See [CONTRIBUTING](CONTRIBUTING.md).

## Disclaimer

Educational and research content only. Nothing here is financial advice. "Validated" means *survived our tests on historical data* — it is **not** a promise of future returns. Trade at your own risk.

## License

Content: [CC BY 4.0](LICENSE) · Code examples: MIT. Sources are cited and linked; we synthesize and attribute, we do not republish others' copyrighted text.
