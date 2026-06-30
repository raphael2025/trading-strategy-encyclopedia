# 链上期权定价与对冲（Python 3.12+）

> 文档版本: 2026-06
> 引用: 14 个
> 知识截止: 2026-05-31

## 1. 链上期权定价的挑战

1. **无中间价**：CEX 有 Deribit，链上没有
2. **IV 估算**：依赖 oracle（Pyth, Chainlink, Lyra SABR）
3. **滑点**：流动性差 → 大单滑点
4. **Gas / 链成本**：写存储昂贵
5. **MEV**：三明治攻击影响对冲

## 2. 主流定价模型

| 模型 | 复杂度 | 适用 | 协议使用 |
|---|---|---|---|
| Black-Scholes | 低 | 欧式 vanilla | Lyra V1, Hegic |
| SABR | 中 | 波动率曲面 | Lyra V2 |
| Heston | 中 | 随机波动率 | Dopex |
| Local Vol | 中 | 时变 vol | Aevo |
| Binomial Tree | 低 | 美式 | 早期 |
| Monte Carlo | 高 | 路径依赖 | Dopex Atlantic |

## 3. 模块 1：Black-Scholes Python

```python
"""
Black-Scholes 定价 + Greeks
"""
import math
from scipy.stats import norm


def bs_call(S: float, K: float, T: float, r: float, sigma: float) -> float:
    if T <= 0:
        return max(S - K, 0)
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)


def bs_greeks(S: float, K: float, T: float, r: float, sigma: float) -> dict:
    if T <= 0:
        return {"delta": 1.0 if S > K else 0.0, "gamma": 0, "vega": 0, "theta": 0}
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    delta = norm.cdf(d1)
    gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
    vega = S * norm.pdf(d1) * math.sqrt(T) * 0.01
    theta = (-S * norm.pdf(d1) * sigma / (2 * math.sqrt(T))
             - r * K * math.exp(-r * T) * norm.cdf(d2)) / 365
    return {"delta": delta, "gamma": gamma, "vega": vega / 100, "theta": theta}
```

## 4. 模块 2：IV 求解

```python
"""
Newton-Raphson 求解隐含波动率
"""
from scipy.optimize import brentq


def implied_vol(price: float, S: float, K: float, T: float,
                 r: float, option_type: str = "call") -> float:
    def obj(sigma):
        return (bs_call(S, K, T, r, sigma) if option_type == "call"
                else bs_put(S, K, T, r, sigma)) - price
    try:
        return brentq(obj, 0.001, 5.0, xtol=1e-6)
    except ValueError:
        return float("nan")
```

## 5. 模块 3：Lyra V2 SABR 简化

```python
"""
SABR 波动率校准（简化版）
"""
import numpy as np
from scipy.optimize import minimize


def sabr_vol(F: float, K: float, T: float,
             alpha: float, beta: float, rho: float, nu: float) -> float:
    if F == K:
        return alpha / (F ** (1 - beta))
    log_FK = np.log(F / K)
    FK_mid = (F * K) ** ((1 - beta) / 2)
    z = (nu / alpha) * FK_mid * log_FK
    x_z = np.log((np.sqrt(1 - 2 * rho * z + z ** 2) + z - rho) / (1 - rho))
    prefactor = alpha / (FK_mid * (1 + ((1 - beta) ** 2 / 24) * log_FK ** 2
                                     + ((1 - beta) ** 4 / 1920) * log_FK ** 4))
    return prefactor * (z / x_z)


def calibrate_sabr(strikes: list, vols: list, F: float, T: float) -> dict:
    def loss(params):
        alpha, beta, rho, nu = params
        return sum((sabr_vol(F, K, T, alpha, beta, rho, nu) - v) ** 2
                   for K, v in zip(strikes, vols))
    result = minimize(loss, [0.3, 0.5, -0.3, 1.0],
                      bounds=[(0.01, 2), (0.1, 0.9), (-0.9, 0.9), (0.1, 5)])
    return dict(zip(["alpha", "beta", "rho", "nu"], result.x))
```

## 6. 模块 4：Lyra V2 报价合成

```python
"""
基于 SABR 校准 + oracle IV 输出期权报价
"""
import asyncio
import aiohttp


class LyraPricingService:
    async def fetch_oracle_iv(self, asset: str = "ETH") -> dict:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.lyra.finance/public/iv/{asset}"
            async with session.get(url, timeout=5) as r:
                return await r.json()

    async def quote(self, S: float, K: float, T: float,
                     r: float = 0.05, asset: str = "ETH") -> dict:
        oracle = await self.fetch_oracle_iv(asset)
        iv = oracle.get("iv", 0.6)
        call_px = bs_call(S, K, T, r, iv)
        put_px = call_px - S + K * math.exp(-r * T)
        greeks = bs_greeks(S, K, T, r, iv)
        return {"call": call_px, "put": put_px, "iv": iv, "greeks": greeks}
```

## 7. 模块 5：链上 delta 对冲

```python
"""
链上 delta 对冲：现货 + perp 动态平衡
"""
import asyncio


class OnchainDeltaHedger:
    def __init__(self, position_delta: float, hedge_threshold: float = 0.1):
        self.target_delta = 0
        self.threshold = hedge_threshold

    async def hedge_if_needed(self, current_delta: float,
                                spot_venue, perp_venue):
        diff = current_delta - self.target_delta
        if abs(diff) < self.threshold:
            return None
        size = abs(diff)
        venue = spot_venue if diff > 0 else perp_venue
        if diff > 0:
            return await venue.sell_spot(size)
        return await venue.open_short_perp(size)

    def calculate_hedge_pnl(self, S0: float, S1: float,
                              delta0: float, delta1: float) -> float:
        spot_pnl = -delta0 * (S1 - S0)
        hedge_pnl = (delta0 - delta1) * (S1 - S0)
        return spot_pnl + hedge_pnl
```

## 8. 模块 6：组合对冲（Covered Call 策略）

```python
"""
Covered Call vault
- 持有 1 ETH
- 卖出 1 ETH call
- 收取权利金
- 限制上行
"""
import math


def covered_call_payoff(S: list, S0: float, K: float,
                          call_premium: float) -> list:
    """
    S: 期末价格列表
    return: 净收益
    """
    pnl = []
    for s in S:
        spot_pnl = s - S0
        call_pnl = -max(s - K, 0) + call_premium
        pnl.append(spot_pnl + call_pnl)
    return pnl
```

## 9. 模块 7：Ribbon Theta Vault 模拟

```python
"""
Ribbon 风格的 Theta Vault：
每周开 covered call
"""
import numpy as np
from typing import Callable


def theta_vault(spot_fn: Callable, weeks: int = 52,
                 strike_pct: float = 1.1) -> dict:
    S = 2000
    premium_total = 0
    pnl_series = []
    for w in range(weeks):
        sigma = spot_fn(w)['iv']
        T = 7 / 365
        K = S * strike_pct
        premium = bs_call(S, K, T, 0.05, sigma)
        next_S = spot_fn(w)['price']
        pnl = (next_S - S) - max(next_S - K, 0) + premium
        pnl_series.append(pnl)
        premium_total += premium
        S = next_S
    return {"weekly_pnl": pnl_series,
            "total_premium": premium_total,
            "apy": sum(pnl_series) / 2000 * 52}
```

## 10. 关键对冲参数

| 参数 | 推荐 | 说明 |
|---|---|---|
| Delta 中和阈值 | 0.05-0.10 | 超出触发对冲 |
| 对冲周期 | 1h | 频繁 = 成本高 |
| Gamma 中和 | 1% | 短期大量对冲 |
| Vega 中和 | 30 DTE | 跨 strike 中和 |
| Slippage 容忍 | 0.3% | 高于即停止 |

## 11. 实战 cheat sheet

| 协议 | 最佳策略 | 风险等级 |
|---|---|---|
| Lyra V2 | delta 中和 LP | 中 |
| Aevo | 限价期权做市 | 中 |
| Hegic | 长期期权卖方 | 中 |
| Premia | 跨链期权套利 | 中 |
| Ribbon | 自动化 vault | 中 |
| Zeta | 做市 + perp 套利 | 低 |

## 12. 与 05 / 06 / 12 关联

- **05-期权衍生品**：理论 + Greeks
- **06-量化**：定价 + 校准 = 量化核心
- **12-2026**：机构场外 → 链上期权过渡

## 13. 14 个关键引用

1. Lyra V2 文档 - https://docs.lyra.finance/
2. Aevo 文档 - https://docs.aevo.xyz/
3. Hegic 文档
4. Premia 文档
5. Ribbon 文档
6. SABR 模型论文
7. Black-Scholes 原始论文
8. Dopex 定价论文
9. Py_vollib 库
10. PyOption 库
11. Greeks 计算标准
12. Lyra SABR 校准
13. Deribit DVOL 指数
14. IV 求解方法

<!-- 文档字数: 约 2300 中文字符 -->
