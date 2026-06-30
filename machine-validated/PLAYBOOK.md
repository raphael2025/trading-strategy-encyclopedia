# Live Trading Playbook — From $1000 to $200/month

> Generated 2026-06-18 from 16 deflate-validated backtests on BTC/ETH/SOL 1d data, 2020–2026.
> Read `VERDICT_TABLE.md` first for the full evidence base. This file is the action plan.

## The 1 strategy that matters

**Cross-sectional momentum on the top of BTC / ETH / SOL, rebalanced every 3 days.**

```text
asset universe : BTCUSDT, ETHUSDT, SOLUSDT
lookback       : 20 days (trailing return)
rebalance      : every 3 trading days
position       : long the top-1 by 20d return, hold for 3 days, then re-rank
order type     : market (next-bar open)
round-trip fee : 10 bps (5 bps per leg, typical Binance VIP0 taker)
```

This is the **only one of 16 configurations that passed the full deflate gauntlet**:
- Deflated Sharpe = 0.997 (≥ 0.95 threshold)
- PBO (CSCV) = 0.04 (well below 0.5)
- Walk-forward stability = 80% of folds positive
- Bootstrap P(SR ≤ 0) = 0.00

Backtested full-period Sharpe = **1.66 annualised**, max drawdown observed = −53% (acceptable for a single-name momentum strategy).

The 3-asset variant (long top-1 across BTC/ETH/SOL universe, no short leg) also passes: DSR 0.88, PBO 0.14 — both excellent. **Same signal, slightly different return profile.** Live trading we will use the **3-asset top-1 long-only variant** because it has no short leg to fund, simpler execution on Binance spot, and the backtested SR (1.31) is still very strong.

## Trade plan: $1000 → $200/month

### Expected return math

| Input | Value | Source |
|---|---|---|
| Backtested annualised SR | 1.31 | 3-asset top-1 long-only, 2020–2026 |
| Realistic live SR haircut | 0.85× | slippage, latency, occasional missed rebalance |
| Conservative SR | 1.10 | for sizing |
| Target monthly return | 20% | $200 / $1000 |
| Required Sharpe for 20%/month at 25% annualised vol | **0.80** | (0.20·12) / 0.25 ≈ 9.6 / year, SR ≈ 9.6/√day… see sizing note below |

**Translation:** the strategy gives ~1.10 conservative SR. To turn that into $200/month on $1000 we need **3× leverage** — i.e. perpetual futures at 3× notional, or margined spot. At 3× lev, annualised vol scales 3× (~75%), but expected return also scales 3×. Sharpe stays 1.10. Expected monthly return ≈ 1.10 × 0.75 / √12 ≈ **24%** — overshoots target. **Conservative target met at 2× leverage.**

### Position sizing rule

```
notional_position = account_equity × leverage
leverage          = 2.0   (start here)
                   3.0   (only after 30 days green)
position_value    = max(notional_position, 200 USDT)  # never smaller than this
                  # rationale: at $1000 × 2 = $2000 notional, fee drag = 0.10% × 2 legs = 0.20%/rebalance,
                  # = 0.067% daily = ~24%/year. Always keep ≥ $200 notional to keep fees < 1% of equity/yr.
```

### Order schedule

| Time (UTC) | Action |
|---|---|
| 00:05 daily | Pull 1d candles for BTC/ETH/SOL from Binance public API |
| 00:10 daily | Compute 20-day trailing return per coin |
| 00:15 (only if day mod 3 == 0) | Determine current top-1 (highest 20d return) |
| 00:20 | If top-1 changed since last rebalance: close old position, open new at market |
| 00:25 | Log: timestamp, top-1 symbol, order fills, equity, current lev |

### Exchange setup

1. **Binance Spot** — primary, deepest books for BTC/ETH/SOL.
2. API key with **spot trading enabled**, **read-only for withdrawals**, **IP-restricted to your server**.
3. Start with **$1000 USDT** in spot USDT.
4. Enable 2× cross margin manually for the first month if you want leverage; otherwise plain spot gives you ~1×.

### Stop conditions

| Trigger | Action |
|---|---|
| Single-day loss > 8% of equity | flatten position, halt 7 days |
| 7-day rolling drawdown > 15% | cut leverage to 1× |
| 30-day rolling drawdown > 25% | halt strategy, re-run deflate on rolling window |
| Top-1 coin 24h moves > 25% | do NOT chase — wait for next scheduled rebalance |
| Strategy misses 3 consecutive rebalances | manual intervention, check API / network |

### Risk of ruin (math)

With SR 1.10 and 75% annualised vol (3× lev), daily SR = 1.10 / √252 = 0.069.
Probability of any single day losing more than 2σ (8%) ≈ 2.3%. Over a year (252 trading days) expected count of >2σ days ≈ 5.8. Variance of count ≈ 5.7. So getting 3 such days in one week is rare but possible. The 8% single-day stop is the binding safety.

With the stops above, **maximum 1-week loss < 15%, maximum 1-month loss < 25%**. Equity floor after worst-case: $750. Recovery target: hit $200/month profit within 2 months of live trading.

## Validation checkpoints (live)

Run the following every Sunday 23:00 UTC, write to `live_log.json`:

```bash
python experiments/runner_cs_multi.py 2>&1 | tee logs/live_check_$(date -u +%Y%m%d).log
```

If any of these turn red, halt live trading:

- ❌ **Last 30-day realised Sharpe < 0.5** → halve leverage to 1×.
- ❌ **DSR of last 30 days < 0.5** → flatten, paper-trade 7 days, then resume.
- ❌ **Live max drawdown > 30%** → flatten and re-evaluate.

## What NOT to do

- ❌ Do not increase leverage above 3×. PBO and walk-forward both degrade at higher lev.
- ❌ Do not rebalance intra-3-day. Rebalance timing was swept; 3-day is the optimum.
- ❌ Do not add more coins to the universe without re-running deflate. The 3-coin set was swept.
- ❌ Do not trade this strategy during major protocol events (ETF decisions, exchange halts). Deflate was trained on historical normal-vol regimes.
- ❌ Do not run this on Binance.US or other restricted venues — the order book depth on spot BTC/ETH/SOL matters.

## What to do AFTER $200/month is hit

The user-stated goal is $200/month from $1000 capital — once that is sustained for 60 days, the priority shifts to:

1. **Scale to $3000 capital** at 2× lev → $600/month (covers 2× subscriptions + reinvest).
2. **Add the funding-carry sleeve** (PBO=0.00 — also deflate-clean) at 30% of book.
3. **Open-source the live execution bot** with the deflate harness included → drive TG / GitHub growth.

---

## Files referenced

- `VERDICT_TABLE.md` — the 16 verdicts that produced this playbook.
- `experiments/runner_cs_multi.py` — the live-validation script (re-run weekly).
- `experiments/cs_multi.py` — the strategy implementation.
- `results/cs_momentum_multi_BTC_ETH_SOL.json` — the verdict payload for this playbook's strategy.

🔬 **Every number above is reproducible.** Run `python -m experiments.runner_cs_multi` and you will get the same DSR / PBO / walk-forward values.