"""Strategy registry + 5 implementable strategies.

Each strategy is a pure function: takes a DataFrame of OHLCV + named params,
returns a 1d np.ndarray of daily returns (net of round-trip cost in bps).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable
import numpy as np
import pandas as pd

_REGISTRY: dict[str, "StrategySpec"] = {}


@dataclass
class StrategySpec:
    name: str
    fn: Callable[..., np.ndarray]
    param_grid: dict[str, list]
    cost_bps: float = 5.0
    doc_slug: str = ""           # which docs/en/.../xxx.md this verdict feeds
    periods_per_year: int = 365  # 365 crypto daily, 252 equities
    description: str = ""


def register(spec: StrategySpec) -> StrategySpec:
    _REGISTRY[spec.name] = spec
    return spec


def get(name: str) -> StrategySpec:
    return _REGISTRY[name]


def all_strategies() -> list[StrategySpec]:
    return list(_REGISTRY.values())


# ---------- helpers ----------
def _sma(s: pd.Series, n: int) -> pd.Series:
    return s.rolling(n).mean()


def _rsi(s: pd.Series, n: int = 14) -> pd.Series:
    delta = s.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - 100 / (1 + rs)


def _cost_leg(pos: pd.Series, cost_bps: float) -> pd.Series:
    """Turnover cost: |Δposition| × cost_bps × price-return-of-underlying.
    Approx: subtract turnover × bps/1e4 from raw returns."""
    return pos.diff().abs().fillna(pos.abs()) * cost_bps / 1e4


# ---------- strategies ----------

def sma_trend(ohlcv: pd.DataFrame, fast: int = 20, slow: int = 100, cost_bps: float = 5.0):
    """Dual SMA crossover, long-only, hold to reversal. No look-ahead (signal at t uses MA up to t).
    `pos` is shifted by 1 bar to avoid using today's close for today's fill."""
    close = ohlcv["close"].astype(float)
    pos = (_sma(close, fast) > _sma(close, slow)).astype(float)
    pos = pos.shift(1).fillna(0.0)
    raw = close.pct_change().fillna(0.0)
    cost = _cost_leg(pos, cost_bps)
    return (raw * pos - cost).to_numpy()


def rsi_mean_reversion(ohlcv: pd.DataFrame, n: int = 14, low: float = 30, high: float = 70,
                       cost_bps: float = 5.0):
    """Buy when RSI<low, sell when RSI>high. Long-only."""
    close = ohlcv["close"].astype(float)
    rsi = _rsi(close, n)
    pos = (rsi < low).astype(float)
    pos = pos.where(rsi < high, 0.0).shift(1).fillna(0.0)
    raw = close.pct_change().fillna(0.0)
    cost = _cost_leg(pos, cost_bps)
    return (raw * pos - cost).to_numpy()


def grid_trading(ohlcv: pd.DataFrame, n_grids: int = 10, range_pct: float = 0.20,
                 cost_bps: float = 5.0):
    """Symmetric grid: rebalance to n_grids equal-size positions inside ±range_pct of MA50.
    Hold neutral on average (no edge by construction); included to confirm deflate flags it."""
    close = ohlcv["close"].astype(float)
    mid = close.rolling(50).mean()
    upper = mid * (1 + range_pct / 2)
    lower = mid * (1 - range_pct / 2)
    spacing = (upper - lower) / n_grids
    # Long bias proportional to deviation below mid (DCA-bot style)
    dev = (close - mid) / mid
    pos = (-dev / (range_pct / 2)).clip(-1, 1)  # -1 at lower bound, +1 at upper
    pos = pos.shift(1).fillna(0.0)
    raw = close.pct_change().fillna(0.0)
    cost = _cost_leg(pos, cost_bps) * 3  # grids turn over a lot
    return (raw * pos - cost).to_numpy()


def funding_carry(ohlcv: pd.DataFrame, funding_annual: float = 0.10, cost_bps: float = 5.0):
    """Cash-and-carry proxy: long spot, short perp = daily funding harvest (annualized).
    Delta-neutral in principle; here we approximate with spot return + funding cash flow minus costs.
    The 'edge' = funding cash flow minus holding costs (assumed small)."""
    close = ohlcv["close"].astype(float)
    raw = close.pct_change().fillna(0.0)        # spot leg
    funding_daily = funding_annual / 365         # perp leg yields this when short
    n = len(raw)
    funding = np.full(n, funding_daily)
    funding[0] = 0.0
    # Holding cost = 2 × taker fees / holding period (annualized) on both legs.
    holding_cost_daily = (2 * cost_bps / 1e4) * 365 / 365   # ≈ cost_bps × 2 / 1e4 per day
    pnl = raw + funding - holding_cost_daily
    # Synthesize small noise to mimic basis rebalancing drawdowns
    rng = np.random.default_rng(42)
    pnl = pnl + rng.normal(0, 0.001, n)
    return pnl


def cross_sectional_momentum(ohlcv: pd.DataFrame, lookback: int = 20, top_k: int = 2,
                              cost_bps: float = 5.0):
    """Single-asset proxy of cross-sectional momentum: long when own 20d momentum is in top quartile
    of its own trailing distribution (z>0.5), else flat. For multi-asset, replace with rank-of-returns."""
    close = ohlcv["close"].astype(float)
    mom = close.pct_change(lookback)
    # Use rolling median + MAD as crude 'cross-sectional' proxy
    med = mom.rolling(252, min_periods=60).median()
    mad = mom.rolling(252, min_periods=60).std()
    z = (mom - med) / mad
    pos = (z > 0.5).astype(float).shift(1).fillna(0.0)
    raw = close.pct_change().fillna(0.0)
    cost = _cost_leg(pos, cost_bps)
    return (raw * pos - cost).to_numpy()


# ---------- register ----------
register(StrategySpec(
    name="sma_trend", fn=sma_trend,
    param_grid={"fast": [10, 20, 30, 50], "slow": [100, 150, 200, 300]},
    doc_slug="03-strategies/trend-following",
    description="Dual SMA crossover, long-only, hold to reversal (the survivor baseline).",
))
register(StrategySpec(
    name="rsi_mr", fn=rsi_mean_reversion,
    param_grid={"n": [7, 14, 21], "low": [25, 30, 35], "high": [65, 70, 75]},
    doc_slug="01-technical-indicators/rsi",
    description="RSI mean-reversion, long-only (the retail favourite).",
))
register(StrategySpec(
    name="grid_trading", fn=grid_trading,
    param_grid={"n_grids": [5, 10, 20], "range_pct": [0.10, 0.20, 0.30]},
    doc_slug="03-strategies/grid-trading",
    description="Symmetric range grid with proportional rebalancing.",
))
register(StrategySpec(
    name="funding_carry", fn=funding_carry,
    param_grid={"funding_annual": [0.05, 0.10, 0.15, 0.20]},
    doc_slug="08-crypto-specific/funding-rate-carry",
    description="Cash-and-carry (long spot / short perp) funding harvest.",
))
register(StrategySpec(
    name="cs_momentum", fn=cross_sectional_momentum,
    param_grid={"lookback": [10, 20, 60], "top_k": [1, 2, 3]},
    doc_slug="03-strategies/cross-sectional-momentum",
    description="Cross-sectional momentum proxy via own-momentum z-score.",
))