# 04 · Market Microstructure

Signals read from the order book and the trade tape — net pressure, toxicity, queue dynamics — evaluated for whether a *retail taker* can actually capture them after spread, fees, and latency.

| Signal | Verdict | Why |
|---|---|---|
| [Order Flow Imbalance / VPIN](order-flow-imbalance.md) | 🔶 | Real RankIC ~0.29 at sub-second horizon — but it is a maker/HFT-only edge; a retail taker crossing the spread nets ≈ −8 bps. |

Microstructure is the one family where the signal is often **genuinely predictive** — yet that is not the question that matters. These edges live *below the spread and beneath the latency floor*: capturing them means providing liquidity and acting in microseconds, so they belong to liquidity providers, not retail takers.

← Back to the [Verdict Index](../00-verdict-index.md).
