"""Real cross-sectional momentum: rank 3 cryptos by 20d return, long top, short bottom, weekly rebalance.

This is the genuine cross-sectional strategy (vs the single-asset proxy in strategies.py).
Lives in a separate file because it depends on a multi-asset loader, not a single symbol.

Output: net daily returns net of taker fees (10 bps round-trip) and weekly rebalance cost.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def cs_momentum_multi(universe: dict[str, pd.DataFrame], lookback: int = 20,
                      rebal: int = 7, top_n: int = 1, bottom_n: int = 1,
                      cost_bps: float = 10.0, fee_per_leg_bps: float = 5.0):
    """Long top_n cryptos by trailing `lookback` return, short bottom_n. Rebalance every `rebal` days.
    `universe` is dict {symbol: ohlcv_df}; all dfs must share a common DatetimeIndex.
    Returns a single pd.Series of daily portfolio returns (net of costs)."""
    # align
    common = None
    for sym, df in universe.items():
        idx = df.index if common is None else common.intersection(df.index)
        common = idx
    common = sorted(common)
    if not common:
        raise ValueError("No common timestamps across universe")

    closes = pd.DataFrame({sym: universe[sym].loc[common, "close"].astype(float) for sym in universe})
    rets = closes.pct_change().fillna(0.0)

    # momentum signal: trailing lookback return, computed daily
    mom = closes.pct_change(lookback)

    # rank on each day (use shift(1) so signal at t uses info up to t-1)
    rank = mom.shift(1).rank(axis=1, ascending=False, na_option="bottom")

    # position: long top_n, short bottom_n, equal weight, only on rebal days
    pos = pd.DataFrame(0.0, index=common, columns=closes.columns)
    for i, day in enumerate(common):
        if i % rebal != 0:
            pos.loc[day] = pos.iloc[i - 1] if i > 0 else 0.0
            continue
        r = rank.loc[day].dropna()
        if r.empty:
            continue
        longs = r.nsmallest(top_n).index   # rank 1 = top
        shorts = r.nlargest(bottom_n).index
        for sym in longs:
            pos.loc[day, sym] = 1.0 / top_n
        for sym in shorts:
            pos.loc[day, sym] = -1.0 / bottom_n

    # apply rebalance cost (delta in position × 2 legs × fee)
    dpos = pos.diff().abs().sum(axis=1).fillna(pos.abs().sum(axis=1))
    cost = dpos * (2 * fee_per_leg_bps) / 1e4

    # portfolio return = sum(pos * asset_returns) - cost
    port_ret = (pos.shift(1).fillna(0.0) * rets).sum(axis=1) - cost
    return port_ret.to_numpy(), pos, closes


def cs_momentum_multi_sr(universe, **kwargs):
    r, _, _ = cs_momentum_multi(universe, **kwargs)
    r = np.asarray(r)
    r = r[np.isfinite(r)]
    return r.mean() / r.std() * np.sqrt(365) if r.std() > 0 else 0.0