# 03 · Strategies

Whole trading *strategies* — entry logic, holding rules, and exit discipline — tested under honest, causal timestamping with costs internalized and selection-aware deflation (DSR/PBO), not just indicators in isolation.

| Strategy | Verdict | Why |
|---|---|---|
| [Trend Following](trend-following.md) | ✅ | Rides persistence the way momentum actually exists; slow enough to clear cost, selection-aware. Sharpe ~1.1, ~36% win rate but ~6.5 payoff — the edge is in *not* cutting winners. |
| [Cross-Sectional Momentum](cross-sectional-momentum.md) | ✅ | Relative, diversified, low-correlation; Sharpe ~1.2 and clears DSR/PBO — but only on a liquid-but-not-saturated universe (mega-caps DSR ≈ 0.004). |
| [Breakout](breakout.md) | 🔶 | Real only as a slow, cost-aware channel breakout (effectively trend following); naive intraday "buy the breakout" dies to false breakouts + turnover cost. |
| [Mean Reversion](mean-reversion.md) | ❌ | In crypto's trending regime, fading extremes = catching a falling knife; net-negative after cost, no edge vs placebo. (Legitimate only in market-neutral pairs/stat-arb.) |
| [Copy Trading](copy-trading.md) | ❌ | RankIC ≈ 0, survivorship bias, and you fill behind the leader as their exit liquidity — a ranking with zero forward information is not a strategy. |

The survivors all do the same thing: they ride **momentum/persistence** in a slow, cost-aware, selection-aware way, and they diversify into **low-correlation combos** (trend + cross-sectional + carry reaches Sharpe ~1.7). The dead ones either **fight the trend** (mean reversion) or **chase mirages** (copy trading = being someone else's exit liquidity).

← Back to the [Verdict Index](../00-verdict-index.md).
