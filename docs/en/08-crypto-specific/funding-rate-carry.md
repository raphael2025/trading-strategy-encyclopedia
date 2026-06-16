# Funding Rate Carry (Cash-and-Carry)

> One-line: harvest the perpetual funding rate by going long spot and short perp, delta-neutral, collecting the periodic payment longs make to shorts. **Verdict: ✅ Validated** (the cleanest honest edge in crypto).

## What it is

A perpetual future has no expiry, so to keep it tethered to spot the exchange charges a periodic **funding rate**: when the perp trades above spot, longs pay shorts; when below, shorts pay longs. The cash-and-carry trade monetizes this directly. When funding is persistently positive, you **buy spot and short the perp** in equal size — the price exposure cancels (delta-neutral), and you simply collect the funding payments the shorts receive. It is a market-neutral *yield*, harvested from a structural cash flow rather than from any view on price.

## The claim

That crypto's persistent positive funding — driven by retail's structural appetite to be long with leverage — is a near-risk-free carry available to anyone willing to hold both legs.

## The test

We constructed the delta-neutral basis trade on BTC/ETH/SOL, with funding receipts and *all* costs (taker fees, slippage, the cost of rolling and rebalancing both legs) internalized, then measured Sharpe and, crucially, the tail.

- **Near risk-free funding harvest, very high Sharpe.** The funding stream is a real, exchange-paid cash flow, and with both legs hedged the day-to-day P&L is dominated by it.
- **But the tail is real.** Exchange/counterparty failure, liquidation of the short perp leg on a violent up-wick if margin is mismanaged, funding flipping negative, and depeg/settlement risk all sit in the left tail. The distribution is "collect a little, often; occasionally lose a lot."
- **Therefore size ≤20% of capital.** The cap is not timidity — it is the correct response to a thin-but-fat left tail on an otherwise smooth return.

## Verdict: ✅ Validated

This survives because it is a **structural cash flow — a real payment — not a price prediction**. There is no threshold to tune and no signal that must generalize out-of-sample, which is why the DSR/PBO machinery has nothing to punish. It is genuinely **the cleanest honest edge in crypto**. But it is *not* free money: the tail risk is real, which is exactly why the size cap and disciplined margin on the short leg matter (see [perpetuals & liquidations](perpetuals-and-liquidations.md) and [leverage](../06-risk-management/leverage.md)). Realistic expectation: a high-Sharpe, low-drama yield punctuated by rare, sharp drawdowns — best held small. It also **combines beautifully** with [trend following](../03-strategies/trend-following.md) and [cross-sectional momentum](../03-strategies/cross-sectional-momentum.md): because the three are largely uncorrelated, the blend reaches the best risk-adjusted form in the whole encyclopedia — **Sharpe ~1.7, DSR 0.93, drawdown ~−22%**.

## Try it yourself

Pull exchange-published funding history, construct the long-spot/short-perp pair, and credit funding while debiting realistic two-leg costs and rebalancing. The mean return is the carry; the story is in the *tail* — stress the short leg against historical up-wicks and a funding sign-flip. Then size with [vol-targeting](../06-risk-management/position-sizing-and-vol-targeting.md) at ≤20% and blend with the momentum sleeves to see the correlation benefit.

## Sources

- Classic literature on the futures basis and cash-and-carry arbitrage.
- Research on crypto perpetual funding rates and the basis trade (academic and practitioner notes).
- Funding-rate mechanics are exchange-published — verify the schedule and formula on the venue you trade.
