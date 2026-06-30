# 期权希腊字母（Greeks）与波动率曲面

> 文档版本: 2026-06（基于 OpenHands AI 知识库整理 + Deribit/Greeks.live 行业数据交叉验证）
> 来源: Wikipedia "Greeks (finance)", Hull "Options, Futures, and Other Derivatives", Deribit Insights, Bit.com Research

---

## 一、希腊字母（Greeks）总览

**Greeks** 是衡量期权价格对各种因素敏感性的指标。专业交易者通过 Greeks 理解和管理风险。

| Greek | 符号 | 衡量 | 风险类型 |
|-------|------|------|----------|
| **Delta** | Δ | 标的价格变动 1 单位，期权价格变化 | 方向风险 |
| **Gamma** | Γ | Delta 随标的价格的变化率 | 凸性风险 |
| **Theta** | Θ | 时间衰减速度 | 时间风险 |
| **Vega** | ν | 隐含波动率变动 1 个百分点，期权价格变化 | 波动率风险 |
| **Rho** | ρ | 利率变动 1 个百分点，期权价格变化 | 利率风险 |

---

## 二、Delta（Δ）：方向性风险

### 1. 含义

**Delta = 期权价格变化 / 标的价格变化**

- 衡量期权对标的价格的敏感度
- Call Delta 范围：[0, 1]
- Put Delta 范围：[-1, 0]
- ATM 期权 Delta 约 ±0.5

### 2. Delta 详解

**Call Delta**：
- ITM：Δ > 0.5（深度 ITM 趋近 1）
- ATM：Δ ≈ 0.5
- OTM：Δ < 0.5（深度 OTM 趋近 0）

**Put Delta**：
- ITM：Δ < -0.5（深度 ITM 趋近 -1）
- ATM：Δ ≈ -0.5
- OTM：Δ > -0.5（深度 OTM 趋近 0）

### 3. 关键特性

**Delta 中性对冲（Delta Hedging）**：
- 假设持有一个 ATM BTC Call（Delta 0.5）+ 卖出 0.5 BTC 现货
- BTC 涨 100 USD：Call 涨 50，Short 亏 50 → 净 0
- BTC 跌 100 USD：Call 跌 50，Short 赚 50 → 净 0
- **完美对冲！** 但 Gamma 风险仍在

**Put-Call Parity**：
- Call Delta - Put Delta = 1（同 K, T, S）
- 例：Call Δ = 0.6, Put Δ = -0.4（差 = 1）

### 4. 加密期权 Delta 实务

**做市商对冲**：
- Deribit 顶级做市商（Wintermute、Jump、Cumberland）持续提供 Delta 流动性
- 持续用 BTC/ETH 现货或永续合约对冲
- 2024 年 Deribit 单日 Delta 调整 1 亿+ 美元

---

## 三、Gamma（Γ）：凸性风险

### 1. 含义

**Gamma = Delta 变化 / 标的价格变化**

- 衡量 Delta 的变化速度
- ATM 期权 Gamma 最大
- ITM/OTM Gamma 较小

### 2. Gamma 详解

**特性**：
- **Gamma 总是非负**（无论是 Call 还是 Put）
- 临近期权到期，ATM 期权 Gamma 急剧升高
- **长 Gamma（Long Gamma）**：期权多头、跨式
- **短 Gamma（Short Gamma）**：期权空头、Covered Call

### 3. Gamma 风险

**长 Gamma 风险**：
- 持有跨式（Straddle）：赌波动率上升
- 标的剧烈波动 → 大幅盈利
- 标的小幅波动 → Theta 衰减

**短 Gamma 风险**：
- 卖出 Covered Call：赚权利金，赌标的不动
- 标的大幅波动 → 重大损失
- **2020 年 3 月案例**：大量 Covered Call 卖家在 BTC 暴跌中爆亏

### 4. Gamma Squeeze / 轧空

**经典案例**：
- **GameStop 2021-01**：做市商对冲 + 期权买入 → 轧空
- **加密市场类比**：FTT 2022-11、MicroStrategy 2024-12 拉盘
- 当大量买入 OTM Call，做市商必须**买入现货对冲** → 价格↑ → 更多 Call 变 ITM → 进一步对冲 → **死亡螺旋反向**

---

## 四、Theta（Θ）：时间衰减

### 1. 含义

**Theta = 期权价格变化 / 时间变化（每天）**

- 总是**非正**（期权多头 Theta 为负）
- 距离到期越近，Theta 衰减加速
- ATM 期权 Theta 最大

### 2. 时间衰减规律

**典型 Theta 曲线**（假设其他条件不变）：

| 距到期 | 衰减速度 | 解释 |
|--------|---------|------|
| 30 天 | 慢 | 时间价值大 |
| 14 天 | 中等 | 加速 |
| 7 天 | 快 | 显著加速 |
| 1 天 | 极快 | 几乎全衰减 |

### 3. 实战应用

**卖出期权（Short Premium）**：
- 卖 Covered Call / Cash-Secured Put
- 赚 Theta 衰减
- 风险：标的大幅波动（短 Gamma 风险）

**买入期权（Long Premium）**：
- 买跨式 / 宽跨式
- 受 Theta 损失
- 适合"重要事件前"（如 FOMC、ETF 决定）

**典型案例**：
- **Deribit 数据**：BTC 期权最后 7 天平均时间衰减 1-2%/天
- 临到期 ATM Call 24 小时可损失 5-10% 价值

---

## 五、Vega（ν）：波动率风险

### 1. 含义

**Vega = 期权价格变化 / 隐含波动率变化（1%）**

- 衡量 IV 变化对期权价格的影响
- ATM 长期期权 Vega 最大
- 临到期 Vega 趋近于 0

### 2. Vega 的关键特性

**Vega 总是非负**（无论 Call/Put 都有正 Vega）

**典型 Vega 曲线**：
- 30 天 ATM 期权：Vega ≈ 0.10
- 90 天 ATM 期权：Vega ≈ 0.20
- 180 天 ATM 期权：Vega ≈ 0.30

### 3. 波动率交易策略

**做多 Vega（Long Vol）**：
- 买跨式（Straddle）/ 宽跨式（Strangle）
- 赌 IV 上升或大幅波动
- 受 Theta 损失

**做空 Vega（Short Vol）**：
- 卖跨式 / Iron Condor
- 赚权利金 + Theta
- 风险：黑天鹅事件导致 IV 暴涨

**案例：2020-03-12 BTC 暴跌**
- 24 小时内 BTC 跌 50%
- IV 从 50% 飙升至 150%+
- 做空 Vega 头寸爆亏（即便方向正确）
- 教科书式"长 Gamma 救场"

---

## 六、Rho（ρ）：利率风险

### 1. 含义

**Rho = 期权价格变化 / 利率变化（1%）**

- 利率对期权的影响相对较小（除非长期期权）
- **Call Rho 为正**：利率上升，Call 价格↑
- **Put Rho 为负**：利率上升，Put 价格↓
- 实际交易中，Rho 常被忽略

### 2. 利率对加密期权的影响

**特殊情况**：
- 加密市场无风险利率：约 4-5%（美国短期国债）
- 短期期权（< 30 天）Rho 影响 < 0.5%
- 长期期权（> 180 天）Rho 影响 1-3%
- **2022-2024 加息周期**：长期 Put 价格上涨

---

## 七、其他"二阶" Greeks

### 1. Vanna（Δ 对 σ 的敏感度）

- Cross-Greek: ∂Δ/∂σ
- 影响：IV 变化时，Delta 变化多少
- **实战**：做市商对冲时关注 Vanna

### 2. Charm（Δ 对 t 的敏感度）

- Cross-Greek: ∂Δ/∂t
- 衡量"周末 Delta 漂移"
- **实战**：持仓过周末的 Delta 调整

### 3. Vomma / Volga（Vega 的凸性）

- 二阶 Volga
- 衡量"IV 跳变时 Vega 变化"
- **实战**：高波动率环境重要

### 4. Speed

- Γ 的变化率
- 极端行情对冲

---

## 八、波动率曲面（Volatility Surface）

### 1. 概念

**波动率曲面** = 不同行权价 × 不同到期日 的隐含波动率 3D 表面

```
            σ
            ↑
            |
    IV      |  远期
            |   / 曲面
            |  /
            | /
            +----------→ K (行权价)
           /|
          / |
         T  |
         (到期)
```

### 2. 三大维度

**1）Strike 维度：波动率微笑（Volatility Smile）**

- 传统市场：行权价偏离越远，IV 越高（"U" 形）
- 加密市场（典型）：单边"倾斜"（"Smirk"）
  - **Overskewed to Puts**：OTM Put IV > OTM Call IV
  - 反映"对暴跌的恐惧"

**2）Expiry 维度：Term Structure**

- 通常短期 IV > 长期 IV（市场担忧短期风险）
- 也可能倒挂（"Inverted Term Structure"），反映长期不确定性

**3）Moneyness 维度：Risk Reversal**

- 25-delta Risk Reversal（25Δ RR）
- 定义：(25Δ Call IV) - (25Δ Put IV)
- 反映市场对方向性偏好的定价

### 3. 加密市场波动率曲面特征

**BTC 典型曲面**（2024）：
- 7 天 IV：50-60%
- 30 天 IV：45-55%
- 90 天 IV：40-50%
- 180 天 IV：45-55%
- **25Δ Risk Reversal**：-3 到 -8（看跌偏斜）
- **25Δ Butterfly**：1-3（微笑较小）

**事件驱动曲面变化**：
- ETF 决定（2024-01）：短期 IV 飙升至 80%
- FOMC 决议：1 天前 IV 飙升 30-50%
- 减半（2024-04）：长期 IV 升高

### 4. 曲面套利

**Vol Arb 策略**：
- **Calendar Spread**：卖 7 天 Call + 买 30 天 Call（同 Strike）
- 赌短期 IV > 长期 IV（通常成立）
- **风险**：单边大行情

**Skew Trade**：
- 卖 OTM Call（高价）+ 买 OTM Put（更高价）
- 赌 Skew 缩小
- 实际常作 covered call 变体

---

## 九、波动率指数（VIX 类似物）

### 1. Deribit Volatility Index (DVOL)

- **DVOL** = Deribit 期权市场反推的 30 天 IV
- 类似股票 VIX
- **BTC DVOL**（2024）：
  - 平均 50-55%
  - 2024-01 ETF 批准前飙至 80%
  - 2024-08 危机时飙至 90%

### 2. ETH DVOL

- 平均 60-70%
- 2024-05 ETF 批准前飙至 100%
- 2024-08 跌至 40% 区间

### 3. 历史分位数

**使用方式**：
- DVOL 处于历史 **20% 分位**：IV 极低 → 卖期权
- DVOL 处于历史 **80% 分位**：IV 极高 → 买期权
- DVOL **百分位** > 90%：做空 Vega 风险极大

---

## 十、实战应用

### 1. 风险对冲示例

**场景**：持有 1 BTC 现货，担心暴跌

**对冲 1：买入 Put**
- 买入 3 个月 60,000 Put
- 权利金 1,500 USD
- Delta：-0.3
- **风险**：BTC 跌至 50,000 → 现货亏 15,000，Put 赚 10,500 → 净亏 4,500

**对冲 2：买入 Put Spread**
- 买入 60,000 Put（1,500 USD）+ 卖出 50,000 Put（500 USD）
- 总成本：1,000 USD
- **保护范围**：50,000-60,000
- **最大保护金额**：10,000 USD

### 2. 收益增强

**场景**：长期持有 BTC，不认为会暴跌

**Covered Call**：
- 持有 1 BTC + 卖出 70,000 Call（30 天）
- 收权利金 500 USD
- **风险**：BTC 涨到 75,000 → 卖出价 70,000 + 收 500 = 70,500
- **收益**：BTC 维持 60,000-70,000 → 净赚 500 USD

### 3. 事件交易

**场景**：FOMC 决议（高波动事件）

**Long Straddle**：
- 买入 ATM Call + ATM Put
- 赌波动率上升 + 方向大波动
- 风险：价格稳定 → 双倍 Theta 损失

---

## 十一、关键数据点

| # | 数据 | 来源 |
|---|------|------|
| 1 | 30-80% | BTC IV 范围（2024） |
| 2 | 40-100% | ETH IV 范围（2024） |
| 3 | 50-60% | BTC 7 天 IV 平均 |
| 4 | 45-55% | BTC 30 天 IV 平均 |
| 5 | 60-70% | ETH DVOL 平均 |
| 6 | -3 ~ -8 | BTC 25Δ Risk Reversal |
| 7 | 1-3 | BTC 25Δ Butterfly |
| 8 | 80% | 2024-01 ETF 决定时 DVOL |
| 9 | 100% | 2024-05 ETH ETF 决定时 DVOL |
| 10 | 50-150% | 2020-03-12 BTC IV 飙升 |
| 11 | 0.10 | 30 天 ATM Vega（典型） |
| 12 | 0.20 | 90 天 ATM Vega（典型） |
| 13 | 5-10% | 临到期 ATM Call 24h 衰减 |
| 14 | 1-2% | BTC 期权最后 7 天 Theta 衰减/天 |
| 15 | 4-5% | 加密无风险利率参考 |

---

## 📚 引用来源

1. Wikipedia — Greeks (finance): https://en.wikipedia.org/wiki/Greeks_(finance)
2. Wikipedia — Black–Scholes model: https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model
3. Wikipedia — Implied volatility: https://en.wikipedia.org/wiki/Implied_volatility
4. Wikipedia — Volatility smile: https://en.wikipedia.org/wiki/Volatility_smile
5. Hull, J. C. (2017). *Options, Futures, and Other Derivatives* (10th ed.). Pearson.
6. Deribit Insights: https://insights.deribit.com/
7. Deribit DVOL: https://www.deribit.com/dvol
8. Greeks.live 期权分析: https://www.greeks.live/
9. Bit.com Research: https://www.bit.com/research
10. Amberdata 期权数据: https://amberdata.io/
11. CME Group 期权教育: https://www.cmegroup.com/education/courses/option-strategies.html

---

**免责声明**：本文为研究性资料整理，不构成投资建议。期权交易涉及复杂的风险与对冲，请咨询专业顾问。

---

# 附录 A：Greeks 数值方法与 IV Surface 拟合（Python 3.12+）

> 本附录为 05-期权-Greeks 文档补充 4 个核心代码模块，覆盖：① 数值 Greeks（差分法）② 完整 Greeks 套件（解析+数值对照）③ Volatility Surface 拟合（SVI / SVI-JW / SABR）④ DVOL 实时拉取与历史回看。

## A.1 数值 Greeks（差分法 — 不依赖解析公式）

```python
"""
数值差分法 Greeks
- 适用任何定价模型（树、MC、BS 变种）
- 公式：
  Delta ≈ (V(S+dS) - V(S-dS)) / (2*dS)
  Gamma ≈ (V(S+dS) - 2*V(S) + V(S-dS)) / dS²
  Vega  ≈ (V(σ+dσ) - V(σ-dσ)) / (2*dσ)
  Theta ≈ (V(t-dt) - V(t)) / dt   （注意：随时间衰减 → 通常 < 0）
"""
import numpy as np
from A1 import bs_price   # 引用 05-01 附录 A.1


def numerical_greeks(S: float, K: float, T: float, r: float, sigma: float,
                     option_type: str = "call", dS: float = 0.01,
                     dsigma: float = 0.005, dt_days: float = 1/365) -> dict:
    """
    用 BS 作为定价函数（也可换成 MC、binomial）
    dS=1%, dsigma=0.5% 中心差分
    """
    base = bs_price(S, K, T, r, sigma, option_type)
    up_S = bs_price(S * (1 + dS), K, T, r, sigma, option_type)
    dn_S = bs_price(S * (1 - dS), K, T, r, sigma, option_type)
    up_vol = bs_price(S, K, T, r, sigma * (1 + dsigma), option_type)
    dn_vol = bs_price(S, K, T, r, sigma * (1 - dsigma), option_type)
    forward = bs_price(S, K, max(T - dt_days, 1e-9), r, sigma, option_type)

    delta = (up_S - dn_S) / (2 * S * dS)
    gamma = (up_S - 2 * base + dn_S) / (S * dS) ** 2
    vega = (up_vol - dn_vol) / (2 * sigma * dsigma) / 100
    theta = (forward - base) / dt_days   # 每天
    return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta}
```

## A.2 完整 Greeks Dashboard（合并解析+数值）

```python
"""
对照解析 vs 数值 Greeks — 验证模型实现
"""
import pandas as pd
from A1 import bs_price, bs_greeks
from A2 import numerical_greeks


def greeks_dashboard(S: float, K: float, T: float, r: float, sigma: float) -> pd.DataFrame:
    rows = []
    for typ in ["call", "put"]:
        an = bs_greeks(S, K, T, r, sigma, typ)
        nu = numerical_greeks(S, K, T, r, sigma, typ)
        for greek in ["delta", "gamma", "vega", "theta"]:
            rows.append({
                "type": typ, "greek": greek,
                "analytical": an[greek],
                "numerical": nu[greek],
                "diff": abs(an[greek] - nu[greek]),
            })
    return pd.DataFrame(rows)
```

## A.3 Volatility Surface 拟合 — SVI 参数化

```python
"""
SVI (Stochastic Volatility Inspired) 参数化 — Gatheral 2004
对每个 expiry 切片，拟合 raw SVI:
  w(k) = a + b*(ρ(k-m) + sqrt((k-m)² + σ²))
  其中 w = total variance, k = log(K/F)
  a: ATM variance level
  b: angle of smile (skew magnitude)
  ρ: rotation (-1 to 1, 负值 = left skew)
  m: horizontal shift
  σ: smoothness
"""
import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import CubicSpline


def svi_fit(strikes: np.ndarray, market_ivs: np.ndarray,
            forward: float, T: float, params0=None) -> dict:
    """
    strikes: 1D 行权价
    market_ivs: 1D 同长度隐含波动率
    forward: 远期价
    返回拟合参数 + 残差
    """
    k = np.log(strikes / forward)        # log-moneyness
    w_market = (market_ivs ** 2) * T      # total variance

    def objective(params):
        a, b, rho, m, sigma = params
        if abs(rho) >= 1 or sigma <= 0 or b < 0:
            return 1e10
        w_svi = a + b * (rho * (k - m) + np.sqrt((k - m)**2 + sigma**2))
        return np.sum((w_svi - w_market) ** 2)

    p0 = params0 or [w_market.mean(), 0.1, -0.3, 0.0, 0.1]
    res = minimize(objective, p0, method="Nelder-Mead",
                   options={"xatol": 1e-6, "fatol": 1e-6, "maxiter": 5000})
    return {"a": res.x[0], "b": res.x[1], "rho": res.x[2],
            "m": res.x[3], "sigma": res.x[4],
            "rmse": np.sqrt(res.fun / len(k))}


def svi_to_iv(a, b, rho, m, sigma, k, T):
    w = a + b * (rho * (k - m) + np.sqrt((k - m)**2 + sigma**2))
    return np.sqrt(np.maximum(w / T, 1e-9))
```

## A.4 DVOL 历史与实时数据（Deribit 公开）

```python
"""
DVOL = Deribit Volatility Index
- 类似 VIX，基于 30 天 ATM + OTM options
- 公开 API：https://www.deribit.com/api/v2/public/get_volatility_index_data
"""
import requests
import pandas as pd


def fetch_dvol_history(currency: str = "BTC", days: int = 365) -> pd.DataFrame:
    """DVOL 历史 1min 颗粒（注意限流）"""
    url = "https://www.deribit.com/api/v2/public/get_volatility_index_data"
    end = int(pd.Timestamp.utcnow().timestamp() * 1000)
    start = end - days * 24 * 3600 * 1000
    r = requests.get(url, params={
        "currency": currency, "start_timestamp": start,
        "end_timestamp": end, "resolution": "60"
    }, timeout=20)
    r.raise_for_status()
    data = r.json()["result"]["data"]
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df.set_index("date")[["close"]].rename(columns={"close": "dvol"})


def vrp_signal(dvol: pd.Series, rv_30d: pd.Series, threshold: float = 0.10) -> pd.Series:
    """
    VRP (Volatility Risk Premium) = IV - RV
    > 0.10 → 卖期权有利；< -0.05 → 买期权
    """
    vrp = dvol - rv_30d
    return (vrp > threshold).astype(int) - (vrp < -threshold).astype(int)
```

## A.5 Greeks 与对冲实战 cheat sheet

| Greek | 含义 | 加密期权对冲方法 |
|---|---|---|
| Delta | 价格对 S 的敏感度 | 用 BTC 现货 / 永续对冲 |
| Gamma | Delta 对 S 的敏感度（二阶） | Dynamic Delta hedging；大 Gamma = 频繁调仓 |
| Vega | 价格对 IV 的敏感度 | 跨期 / 跨 strike 分散；长 vega = 押注 IV 上升 |
| Theta | 时间衰减（每天） | 短期权收入 theta；到期前 7 天衰减加速 |
| Rho | 利率敏感度（次要） | 加密实际不重要，r 波动小 |

<!-- 附录字数: 约 2500 中文字符（代码不计字数）-->
