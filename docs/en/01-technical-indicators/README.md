# 01 · Technical Indicators

This section tests the most widely taught chart indicators as **standalone, mechanical buy/sell signals** — and, tested honestly with costs internalized and the parameter search counted, every one of them dies.

| Indicator | Doc | Verdict | Why |
|---|---|---|---|
| RSI | [rsi.md](./rsi.md) | ❌ Falsified | Tuned 30/70 thresholds don't generalize; fading "overbought" is a falling knife in a trend; dies to cost + multiple-testing. |
| MACD | [macd.md](./macd.md) | ❌ Falsified | The (12,26,9) defaults are a historical artifact; crossovers whipsaw in chop; a lagging difference of two MAs that dies to cost + multiple-testing. |
| Moving Averages | [moving-averages.md](./moving-averages.md) | ❌ Falsified | "Which pair?" — 50/200 is folklore-selected and the in-sample-best pair doesn't carry out-of-sample; dies to cost + multiple-testing. |
| Bollinger Bands | [bollinger-bands.md](./bollinger-bands.md) | ❌ Falsified | 20/2 is folklore-tuned, and two contradictory readings let you always fit one in-sample; fading the band is the same falling knife as mean reversion. |

**The meta-point:** standalone, tuned indicators are *selection-blind folklore* — they fool bootstrap and walk-forward because a cherry-picked config still looks good, but they collapse under DSR and PBO (which know how many configs you tried) and never clear realistic cost. The survivors are not different ingredients; they are the *same* raw ingredients — momentum, volatility — used inside a **selection-aware, cost-aware system** that rides trends instead of fading them. See the [verdict index](../00-verdict-index.md) for the full map.
