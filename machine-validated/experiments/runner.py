"""Run one strategy: grid sweep → best-in-sample pick → deflate.verdict() → JSON payload."""
from __future__ import annotations
import argparse, json, sys, time
from itertools import product
from pathlib import Path

import numpy as np
import deflate

from experiments.data import load_ohlcv
from experiments.strategies import get, all_strategies

RESULTS = Path("/home/raphael/projects/lab/results")
RESULTS.mkdir(parents=True, exist_ok=True)


def _sharpe(r: np.ndarray, ppy: int = 365) -> float:
    r = np.asarray(r, dtype=float)
    r = r[np.isfinite(r)]
    if r.std() == 0 or len(r) < 30:
        return 0.0
    return r.mean() / r.std() * np.sqrt(ppy)


def _max_dd(r: np.ndarray) -> float:
    r = np.asarray(r, dtype=float)
    eq = np.cumprod(1 + r)
    pk = np.maximum.accumulate(eq)
    dd = (eq - pk) / pk
    return float(dd.min())


def run(strategy: str, symbol: str = "BTCUSDT", start: str = "2020-01-01", end: str = "2026-06-18"):
    spec = get(strategy)
    ohlcv = load_ohlcv(symbol, start=start, end=end)
    print(f"[runner] loaded {symbol}: {len(ohlcv)} bars [{ohlcv.index[0].date()} → {ohlcv.index[-1].date()}]")

    # ---- parameter grid sweep ----
    keys = list(spec.param_grid.keys())
    combos = list(product(*[spec.param_grid[k] for k in keys]))
    print(f"[runner] strategy={strategy}  grid={len(combos)} configs  symbol={symbol}")

    T = len(ohlcv)
    matrix = np.empty((T, len(combos)), dtype=np.float64)
    for i, vals in enumerate(combos):
        params = dict(zip(keys, vals))
        matrix[:, i] = spec.fn(ohlcv, **params, cost_bps=spec.cost_bps)

    in_sample = T // 2
    is_sharpes = np.array([_sharpe(matrix[:in_sample, j], spec.periods_per_year) for j in range(len(combos))])
    best_idx = int(is_sharpes.argmax())
    best_params = dict(zip(keys, combos[best_idx]))
    best_returns = matrix[:, best_idx]
    full_sr = _sharpe(best_returns, spec.periods_per_year)
    oos_sr = _sharpe(best_returns[in_sample:], spec.periods_per_year)
    print(f"[runner] best IS={is_sharpes[best_idx]:.3f}  best OOS={oos_sr:.3f}  params={best_params}")

    # ---- deflate verdict ----
    print(f"[runner] running deflate.verdict(n_trials={len(combos)}) ...")
    t0 = time.time()
    v = deflate.verdict(
        returns=best_returns,
        n_trials=len(combos),
        returns_matrix=matrix,
        periods_per_year=spec.periods_per_year,
    )
    dt = time.time() - t0
    print(f"[runner] deflate took {dt:.1f}s")
    print(v)

    # ---- structured payload ----
    payload = {
        "strategy": strategy,
        "symbol": symbol,
        "start": start, "end": end,
        "n_bars": int(T),
        "n_configs": len(combos),
        "best_params": best_params,
        "is_sharpe": float(is_sharpes[best_idx]),
        "oos_sharpe": float(oos_sr),
        "full_sharpe": float(full_sr),
        "max_dd": _max_dd(best_returns),
        "deflate": {
            "is_overfit": bool(v.is_overfit),
            "confidence": float(v.confidence),
            "reasons": list(v.reasons),
            "metrics": {
                k: (vars(val) if hasattr(val, "__dict__") and not isinstance(val, type) else str(val))
                for k, val in v.metrics.items() if val is not None
            },
        },
        "doc_slug": spec.doc_slug,
        "description": spec.description,
    }

    out = RESULTS / f"{strategy}_{symbol}.json"
    out.write_text(json.dumps(payload, indent=2, default=str))
    print(f"[runner] wrote {out}")
    return payload


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strategy", required=True, choices=[s.name for s in all_strategies()])
    ap.add_argument("--symbol", default="BTCUSDT")
    ap.add_argument("--start", default="2020-01-01")
    ap.add_argument("--end", default="2026-06-18")
    args = ap.parse_args()
    run(args.strategy, args.symbol, args.start, args.end)


if __name__ == "__main__":
    main()