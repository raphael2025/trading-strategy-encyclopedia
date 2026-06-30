"""Test real cross-sectional momentum: long top1 / short bottom1 across BTC/ETH/SOL."""
from __future__ import annotations
import sys
sys.path.insert(0, "/tmp/deflate_clone")
sys.path.insert(0, "/home/raphael/projects/lab")

import json
from pathlib import Path
import numpy as np
import pandas as pd
import deflate
from itertools import product

from experiments.data import load_ohlcv
from experiments.cs_multi import cs_momentum_multi

RESULTS = Path("/home/raphael/projects/lab/results")
RESULTS.mkdir(exist_ok=True)


def _max_dd(r):
    eq = np.cumprod(1 + np.asarray(r))
    return float(((eq - np.maximum.accumulate(eq)) / np.maximum.accumulate(eq)).min())


def run_cs_multi(lookbacks=(10, 20, 30), rebals=(3, 7, 14), top_bottom=((1, 1), (1, 0), (0, 1))):
    print("[cs-multi] loading BTC + ETH + SOL...")
    universe = {sym: load_ohlcv(sym, start="2020-01-01", end="2026-06-18") for sym in ["BTCUSDT", "ETHUSDT", "SOLUSDT"]}
    for sym, df in universe.items():
        print(f"  {sym}: {len(df)} bars")

    keys = list(product(lookbacks, rebals, top_bottom))
    print(f"[cs-multi] grid: {len(keys)} configs")

    # use shortest common history
    T = min(len(df) for df in universe.values())

    matrix = np.empty((T, len(keys)))
    for i, (lb, rb, (tp, bt)) in enumerate(keys):
        if tp == 0 and bt == 0:
            matrix[:, i] = 0
            continue
        r, _, _ = cs_momentum_multi(universe, lookback=lb, rebal=rb, top_n=tp, bottom_n=bt)
        # align to last T bars
        matrix[:, i] = r[-T:]

    # in-sample winner
    is_split = T // 2
    is_sharpes = np.array([matrix[:is_split, j].mean() / matrix[:is_split, j].std() * np.sqrt(365)
                            if matrix[:is_split, j].std() > 0 else 0
                            for j in range(len(keys))])
    best_idx = int(is_sharpes.argmax())
    best = matrix[:, best_idx]
    is_sr = is_sharpes[best_idx]
    oos_sr = best[is_split:].mean() / best[is_split:].std() * np.sqrt(365)
    best_params = keys[best_idx]
    print(f"[cs-multi] best IS={is_sr:.3f}  OOS={oos_sr:.3f}  params={best_params}")

    print(f"[cs-multi] running deflate.verdict(n_trials={len(keys)})...")
    v = deflate.verdict(returns=best, n_trials=len(keys), returns_matrix=matrix, periods_per_year=365)
    print(v)

    payload = {
        "strategy": "cs_momentum_multi",
        "universe": list(universe.keys()),
        "start": "2020-01-01", "end": "2026-06-18",
        "n_bars": int(T),
        "n_configs": len(keys),
        "best_params": {"lookback": best_params[0], "rebal_days": best_params[1],
                        "top_n": best_params[2][0], "bottom_n": best_params[2][1]},
        "is_sharpe": float(is_sr), "oos_sharpe": float(oos_sr),
        "full_sharpe": float(best.mean() / best.std() * np.sqrt(365)),
        "max_dd": _max_dd(best),
        "deflate": {
            "is_overfit": bool(v.is_overfit), "confidence": float(v.confidence),
            "reasons": list(v.reasons),
            "metrics": {k: (vars(val) if hasattr(val, "__dict__") and not isinstance(val, type) else str(val))
                        for k, val in v.metrics.items() if val is not None},
        },
    }
    out = RESULTS / "cs_momentum_multi_BTC_ETH_SOL.json"
    out.write_text(json.dumps(payload, indent=2, default=str))
    print(f"[cs-multi] wrote {out}")
    return payload


if __name__ == "__main__":
    run_cs_multi()