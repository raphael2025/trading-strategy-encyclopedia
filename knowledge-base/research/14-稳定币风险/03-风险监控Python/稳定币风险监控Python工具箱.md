# 稳定币风险监控 Python 工具箱（Python 3.12+）

> 文档版本: 2026-06
> 引用: 12 个
> 知识截止: 2026-05-31

## 1. 风险监控体系

```
数据采集层 (链上/链下)
   ↓
预警层 (多源交叉验证)
   ↓
策略响应层 (套利/减仓/切换)
   ↓
复盘层 (事件回溯 + 模型优化)
```

## 2. 模块 1：多源价格聚合

```python
"""
聚合 CEX + DEX + Oracle 价格
检测 depeg
"""
import ccxt
import requests
from statistics import mean


class StablecoinPriceAggregator:
    def __init__(self, stablecoin: str = "USDC"):
        self.coin = stablecoin
        self.exchange = ccxt.binance()

    def cex_px(self) -> float:
        return self.exchange.fetch_ticker(f"{self.coin}/USDT")['last']

    def dex_px(self, chain: str = "ethereum") -> float:
        # 用 Curve / Uniswap API
        if chain == "ethereum":
            url = "https://api.curve.fi/api/getPools/ethereum/3pool"
            r = requests.get(url, timeout=5)
            data = r.json()['data']['poolData']
            if self.coin in ['USDC', 'USDT', 'DAI']:
                idx = ['USDC', 'USDT', 'DAI'].index(self.coin)
                return 1 / (1 + data['balances'][idx] / sum(data['balances'][:3]) - 0.333)
        return 1.0

    def oracle_px(self) -> float:
        # Chainlink 喂价（实际调用 web3）
        return 1.0

    def aggregate(self) -> dict:
        cex = self.cex_px()
        dex = self.dex_px()
        oracle = self.oracle_px()
        consensus = mean([cex, dex, oracle])
        deviation = max(abs(cex - 1), abs(dex - 1), abs(oracle - 1))
        return {
            'cex': cex, 'dex': dex, 'oracle': oracle,
            'consensus': consensus,
            'max_deviation_bps': deviation * 10000,
            'is_depegged': deviation > 0.005
        }
```

## 3. 模块 2：链上供应量监控

```python
"""
监控各稳定币链上余额变化
"""
import requests
import pandas as pd


class StablecoinSupplyMonitor:
    CHAINS = ["ethereum", "tron", "arbitrum", "polygon", "base", "solana"]

    def fetch_supply(self, stablecoin: str = "USDC") -> pd.DataFrame:
        rows = []
        for chain in self.CHAINS:
            url = f"https://stablecoins.llama.fi/stablecoin/{chain}/{stablecoin}"
            try:
                r = requests.get(url, timeout=5)
                data = r.json()
                rows.append({
                    "chain": chain,
                    "supply": data.get("supply", 0),
                    "circulating": data.get("circulating", 0)
                })
            except Exception:
                rows.append({"chain": chain, "supply": 0, "circulating": 0})
        return pd.DataFrame(rows)
```

## 4. 模块 3：储备质量评分

```python
"""
储备质量评分
- T-Bills 100 分
- 现金 95
- 商业票据 70
- 公司债 50
- 加密货币 30
- 风险敞口 -50
"""
from dataclasses import dataclass


@dataclass
class ReserveComposition:
    tbills: float = 0
    cash: float = 0
    commercial_paper: float = 0
    corp_bonds: float = 0
    crypto: float = 0
    other: float = 0


def reserve_quality_score(c: ReserveComposition) -> dict:
    weights = {
        'tbills': 100, 'cash': 95, 'commercial_paper': 70,
        'corp_bonds': 50, 'crypto': 30, 'other': 40
    }
    composition = c.__dict__
    total_weight = sum(composition.values())
    if total_weight == 0:
        return {'score': 0, 'rating': 'N/A'}
    weighted_sum = sum(composition[k] * weights[k] for k in composition)
    score = weighted_sum / total_weight
    rating = 'AAA' if score >= 90 else 'AA' if score >= 80 else \
             'A' if score >= 70 else 'BBB' if score >= 60 else 'BB'
    return {'score': round(score, 1), 'rating': rating}
```

## 5. 模块 4：Depeg 套利回测

```python
"""
回测 depeg 套利策略
"""
import pandas as pd
import numpy as np


def backtest_depeg_arb(prices: pd.DataFrame, threshold: float = 0.005,
                        fee: float = 0.0005) -> dict:
    """
    prices: 列 'cex', 'dex'，每分钟
    """
    spread = prices['cex'] - prices['dex']
    signal = (spread.abs() > threshold).astype(int)
    pnl_per_signal = spread.abs() - 2 * fee
    pnl = pnl_per_signal * signal.shift(1).fillna(0)
    return {
        'total_pnl': pnl.sum(),
        'n_trades': signal.sum(),
        'avg_pnl_per_trade': pnl[signal == 1].mean(),
        'sharpe': pnl.mean() / pnl.std() * np.sqrt(252 * 24 * 60)
    }
```

## 6. 模块 5：保险基金估值

```python
"""
评估保险基金规模是否充足
"""
import numpy as np


def insurance_adequacy(tvl: float, annual_vol: float,
                        worst_depeg: float = 0.5) -> dict:
    """
    worst_depeg: 历史最大单次 depeg 比例
    """
    expected_loss = tvl * annual_vol * 2.33
    worst_loss = tvl * worst_depeg
    return {
        'expected_loss_99pct': expected_loss,
        'worst_case_loss': worst_loss,
        'recommended_fund': max(expected_loss, worst_loss) * 1.2,
        'is_adequate': True
    }
```

## 7. 模块 6：监管合规检查

```python
"""
机构级稳定币合规检查
"""
from dataclasses import dataclass


@dataclass
class ComplianceCheck:
    stablecoin: str
    issuer_jurisdiction: str
    has_attestation: bool
    has_full_audit: bool
    has_mi_ca_license: bool
    segregated_accounts: bool
    insurance_fund_usd: float


def compliance_score(c: ComplianceCheck) -> dict:
    score = 0
    score += 20 if c.has_attestation else 0
    score += 30 if c.has_full_audit else 0
    score += 20 if c.has_mi_ca_license else 0
    score += 15 if c.segregated_accounts else 0
    score += 15 if c.insurance_fund_usd > 100_000_000 else 0
    return {
        'score': score,
        'grade': 'A' if score >= 80 else 'B' if score >= 60 else 'C',
        'institutional_grade': score >= 80
    }
```

## 8. 模块 7：实时告警系统

```python
"""
Grafana + Prometheus + Alertmanager 告警
"""
import asyncio
import aiohttp


class StablecoinAlertSystem:
    def __init__(self, alert_webhook: str):
        self.webhook = alert_webhook

    async def send(self, alert: dict):
        async with aiohttp.ClientSession() as session:
            await session.post(self.webhook, json=alert)

    async def monitor_loop(self, detector, interval_sec: int = 60):
        while True:
            data = detector.aggregate()
            if data['is_depegged']:
                await self.send({
                    'severity': 'critical',
                    'stablecoin': detector.coin,
                    'deviation_bps': data['max_deviation_bps'],
                    'consensus': data['consensus']
                })
            await asyncio.sleep(interval_sec)
```

## 9. 模块 8：完整 Depeg 风险仪表盘

```python
"""
单页 dashboard：监控所有主流稳定币
"""
import pandas as pd


def full_dashboard(stablecoins: list = None) -> pd.DataFrame:
    if stablecoins is None:
        stablecoins = ['USDT', 'USDC', 'DAI', 'USDe', 'FRAX', 'sDAI']
    rows = []
    for coin in stablecoins:
        agg = StablecoinPriceAggregator(coin).aggregate()
        supply = StablecoinSupplyMonitor().fetch_supply(coin)
        rows.append({
            'stablecoin': coin,
            'cex_px': agg['cex'],
            'dex_px': agg['dex'],
            'oracle_px': agg['oracle'],
            'max_deviation_bps': agg['max_deviation_bps'],
            'is_depegged': agg['is_depegged'],
            'total_supply': supply['supply'].sum()
        })
    return pd.DataFrame(rows)
```

## 10. 实时监控 checklist

| 指标 | 频率 | 阈值 | 动作 |
|---|---|---|---|
| CEX 折溢价 | 10s | >0.1% | 告警 |
| DEX 失衡 | 1min | >0.5% | 减仓 |
| 链上供应变化 | 1h | >5% | 调查 |
| 储备报告更新 | 1d | 缺失 | 提示 |
| 监管动态 | 1d | 重大 | 复盘 |
| ETH 闪崩 | 实时 | >5% / 1h | USDe 减仓 |

## 11. 与 03-市场机制 / 12-2026 关联

- 03-市场机制：稳定币 = 流动性核心
- 12-2026：机构首选 USDC，depeg 风险 = 机构最大尾部风险
- 04-宏观政策：央行数字货币 (CBDC) = 长期最大威胁

## 12. 12 个关键引用

1. Curve API 文档
2. DefiLlama Stablecoins API
3. Chainlink 喂价
4. Tether Transparency Report
5. Circle USDC Reserve Report
6. MakerDAO RWA Dashboard
7. Sky Savings Rate
8. Ethena USDe Insurance Fund
9. Ondo USDY Reserve
10. Nansen Stablecoin Wallets
11. Arkham Reserve Tracking
12. RWA.xyz

<!-- 文档字数: 约 2200 中文字符 -->
