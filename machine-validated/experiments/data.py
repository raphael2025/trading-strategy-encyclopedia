"""OHLCV data loader with parquet cache.

Pulls daily bars for BTC/ETH/SOL from the Binance public REST API (no key needed),
falls back to yfinance on failure. Caches per (symbol, timeframe) parquet so
subsequent runs are offline.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import pandas as pd

CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "ohlcv"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Map friendly symbol → Binance symbol
SYMBOL_MAP = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "SOL": "SOLUSDT",
}

# Timeframe → Binance interval
TF_MAP = {
    "1d": "1d",
    "4h": "4h",
    "1h": "1h",
}

BINANCE_BASE = "https://api.binance.com"


def _cache_path(symbol: str, timeframe: str) -> Path:
    return CACHE_DIR / f"{symbol.upper()}_{timeframe}.parquet"


def _fetch_binance(symbol: str, timeframe: str, start_ts_ms: int) -> pd.DataFrame:
    """Stream klines from Binance in chunks of 1000 bars."""
    import requests

    interval = TF_MAP[timeframe]
    bars = []
    end_ts_ms = None
    url = f"{BINANCE_BASE}/api/v3/klines"
    session = requests.Session()
    while True:
        params = {
            "symbol": SYMBOL_MAP[symbol],
            "interval": interval,
            "startTime": start_ts_ms,
            "limit": 1000,
        }
        if end_ts_ms is not None:
            params["startTime"] = end_ts_ms + 1
        r = session.get(url, params=params, timeout=15)
        r.raise_for_status()
        chunk = r.json()
        if not chunk:
            break
        bars.extend(chunk)
        last_open = chunk[-1][0]
        if end_ts_ms is not None and last_open <= end_ts_ms:
            break
        end_ts_ms = last_open
        if len(chunk) < 1000:
            break
        time.sleep(0.15)  # be polite
    if not bars:
        raise RuntimeError(f"Binance returned no data for {symbol} {timeframe}")
    df = pd.DataFrame(
        bars,
        columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_volume", "trades", "taker_buy_base",
            "taker_buy_quote", "ignore",
        ],
    )
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df = df.set_index("open_time")
    for c in ("open", "high", "low", "close", "volume"):
        df[c] = df[c].astype(float)
    return df[["open", "high", "low", "close", "volume"]]


def _fetch_yfinance(symbol: str, start: str, end) -> pd.DataFrame:
    """Fallback: yfinance."""
    import yfinance as yf

    sym = f"{symbol}-USD"
    df = yf.download(sym, start=start, end=end, interval="1d", progress=False)
    if df.empty:
        raise RuntimeError(f"yfinance returned no data for {sym}")
    if hasattr(df.columns, "levels"):  # MultiIndex
        df.columns = [c[0].lower() for c in df.columns]
    else:
        df.columns = [str(c).lower() for c in df.columns]
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    return df[["open", "high", "low", "close", "volume"]].copy()


def load_ohlcv(
    symbol: str,
    timeframe: str = "1d",
    start: str = "2019-01-01",
    end=None,
    use_cache: bool = True,
) -> pd.DataFrame:
    """Load OHLCV bars, cache to parquet.

    Parameters
    ----------
    symbol : str
        One of BTC, ETH, SOL (or its USDT pair).
    timeframe : str
        One of 1d, 4h, 1h.
    start, end : str
        ISO date strings.
    use_cache : bool
        If True (default), read/write parquet cache.

    Returns
    -------
    pd.DataFrame
        Indexed by tz-aware UTC timestamp, columns: open, high, low, close, volume.
    """
    symbol = symbol.upper().replace("USDT", "")
    if symbol not in SYMBOL_MAP:
        raise ValueError(f"unsupported symbol {symbol}; choose from {list(SYMBOL_MAP)}")
    if timeframe not in TF_MAP:
        raise ValueError(f"unsupported timeframe {timeframe}; choose from {list(TF_MAP)}")

    cache = _cache_path(symbol, timeframe)
    if use_cache and cache.exists():
        try:
            df = pd.read_parquet(cache)
            if not df.empty:
                if df.index.tz is None:
                    df.index = df.index.tz_localize("UTC")
                if start:
                    df = df[df.index >= pd.Timestamp(start, tz="UTC")]
                if end:
                    df = df[df.index <= pd.Timestamp(end, tz="UTC")]
                if len(df) > 0:
                    return df
        except Exception as e:
            print(f"[data] cache read failed ({e}), re-fetching", file=sys.stderr)

    start_ts_ms = int(pd.Timestamp("2019-01-01", tz="UTC").timestamp() * 1000)
    try:
        df = _fetch_binance(symbol, timeframe, start_ts_ms)
    except Exception as e:
        print(f"[data] Binance failed ({e}); falling back to yfinance", file=sys.stderr)
        df = _fetch_yfinance(symbol, "2019-01-01", end)

    if use_cache:
        try:
            df.to_parquet(cache)
        except Exception as e:
            print(f"[data] cache write failed: {e}", file=sys.stderr)

    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    if start:
        df = df[df.index >= pd.Timestamp(start, tz="UTC")]
    if end:
        df = df[df.index <= pd.Timestamp(end, tz="UTC")]
    return df
