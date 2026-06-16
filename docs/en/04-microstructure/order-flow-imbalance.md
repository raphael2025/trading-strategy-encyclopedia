# Order Flow Imbalance (OFI) / VPIN

> One-line: measure net buying vs selling pressure from the order book and the trade tape to anticipate the next, very-short-horizon price move. **Verdict: 🔶 Conditional** (a real edge, but the wrong audience).

## What it is

Two related microstructure signals. **Order Flow Imbalance (OFI)** is the net signed pressure at the top of book: it sums the changes in bid and ask sizes together with the trades that hit each side, so a wave of bid additions and aggressive buys produces a large positive OFI. **VPIN** (volume-synchronized probability of informed trading) buckets the tape by equal volume rather than by clock time and estimates the imbalance between buy and sell volume within each bucket — a proxy for *flow toxicity*, i.e. how likely it is that you are trading against someone better informed. Both are read off high-frequency Level-2 data, not candles.

## The claim

Price is moved by order flow, so if you can measure the imbalance *before* the book re-prices, you can predict the next tick. The OFI literature shows price changes line up tightly and contemporaneously with net order-book pressure; the VPIN literature argues that rising toxicity precedes volatility and adverse selection. The practitioner version: "watch the flow, front-run the move."

## The test

We evaluated OFI on high-frequency L2 order-book data for crypto perpetuals, scoring predictive power with **RankIC** against next-horizon returns, signals timestamped causally, and then re-checking what survives once you must actually *trade* it — taker fees, slippage, and the spread you cross all internalized.

- **RankIC ≈ 0.29 at the sub-second horizon.** This is genuinely strong — far above the ~0 RankIC that buries retail K-line ML and copy-trading. The signal is real; the book really does telegraph the next tick.
- **A retail taker nets ≈ −8 bps.** Crossing the spread, paying taker fees, and arriving microseconds late hands the entire edge — and then some — to whoever was already resting on the book.
- The edge does not decay because the prediction is wrong; it decays because **capturing it requires being the liquidity, not taking it.**

## Verdict: 🔶 Conditional

Real edge, wrong audience. The predictive content is legitimate and survives honest scoring — this is not a multiple-testing artifact like FVG retests or candlestick families. But the edge lives *inside the spread you must cross*. It is capturable only by participants who **provide** liquidity (earning maker rebates and queue priority) and act in microseconds with co-located, low-latency infrastructure. For them it is a working strategy; for a retail taker it is a guaranteed −8 bps per round trip. That is why it is 🔶 and not ✅: passing the RankIC test is necessary but not sufficient — the audience and execution model decide whether the edge is real money or a fee donation. Not for retail. The same logic applies to [spoofing/absorption detection](../00-verdict-index.md#microstructure): informative, but not executable at retail latency.

## Try it yourself

Reconstruct OFI from L2 updates, measure its RankIC against the next-horizon return — you should reproduce a strong, real number. Then run the *tradeable* returns of a taker who crosses the spread on each signal through [`deflate`](https://github.com/raphael2025/deflate) and watch net P&L sit firmly negative once cost is internalized. The gap between the two is the entire lesson. If you want the maker version, you need rebates, queue position, and microsecond latency — infrastructure, not a notebook.

## Sources

- Cont, Kukanov & Stoikov (2014), "The Price Impact of Order Book Events," *Journal of Financial Econometrics* — the OFI–price-change relationship.
- Easley, López de Prado & O'Hara (2012), "Flow Toxicity and Liquidity in a High-Frequency World," *Review of Financial Studies* — VPIN and flow toxicity.
- See also the broader cost story in [perpetuals & liquidations](../00-verdict-index.md) and the [Verdict Index · Microstructure](../00-verdict-index.md#microstructure).
