# Memecoin 与 AI 代理 SocialFi

> 文档版本: 2026-06
> 引用: 18 个
> 知识截止: 2026-05-31

## 1. AI Memecoin 浪潮

### 1.1 起点：Truth Terminal + GOAT (2024-10)
- **GOAT (Goatseus Maximus)**：AI 推特账号 Truth Terminal 推荐
- **市值峰值**：>$1.3B（2024-12）
- **机制**：
  - LLM 自动运行
  - "Goatse Gospel" 宗教梗
  - 无团队/无 VC/无路线图
- **意义**：AI 代理可"创造"市值

### 1.2 后续：PNUT, TURBO, SHIBOSHI
- **PNUT (Peanut the Squirrel)**：2024-11 推出，市值峰值 $2.5B
- **TURBO**：AI 题材 meme
- **SHIBOSHI**：Shiba Inu 生态

### 1.3 Clanker（Base 链 AI 发行）
- **机制**：自然语言 → ERC-20 代币
- **2024-12 启动**：>10K 代币，>30K SOL 费用
- **影响**：发行代币 = 0 摩擦

## 2. SocialFi 与 AI 代理

### 2.1 Virtuals Protocol（GAME Engine）
- **机制**：用户创建 AI agent → 同名代币
- **代币经济**：
  - 代币 = agent 价值的 claim
  - Bonding curve 发行
  - 100% 流通（无 vesting）
- **数据**（2026-Q2）：
  - >10K agent
  - >$300M TVL
  - >$50M 月费用
- **VIRTUAL 代币**：>3B 美元市值

### 2.2 DAOS.fun
- **机制**：AI DAO + 跟投
- **特性**：
  - 跟投头部 AI 代理
  - 治理代币分配
  - KOL 主导

### 2.3 aixbt
- **机制**：AI agent 在 X 上发推
- **特点**：
  - KOL 影响力
  - 自动 alpha signal
  - 代币 + 服务
- **AIXBT 市值**：>$400M（peak）

### 2.4 Bankr
- **机制**：自然语言交易（"买 1000 USDC 的 ETH"）
- **链**：Base
- **集成**：Uniswap V3, Aave

## 3. Memecoin 经济学

### 3.1 发行模型对比

| 平台 | 链 | 机制 | 费用 | 代币部署 |
|---|---|---|---|---|
| pump.fun | Solana | 曲线 | 1% | 数秒 |
| Clanker | Base | 自然语言 | 0.0007 ETH | 数秒 |
| DAOS.fun | Base | DAO | 1% | 数小时 |
| Virtuals | Base | GAME | 0.001 ETH | 数秒 |
| Believe | Solana | X 推文 | 1% | 数分钟 |
| MemeX | Multi | X 推文 | 1% | 数分钟 |

### 3.2 经典生命周期
```
T+0: KOL 推文，0 流动性
T+10min: 50K → 500K mcap（曲线阶段）
T+1h: 1M → 10M mcap（DEX 上线）
T+6h: 10M → 100M（CEX 关注）
T+24h: 100M → 1B（峰值，零售涌入）
T+72h: 30% 暴跌（解锁 + 项目方抛）
T+30d: 5% 存活（少数幸存者）
```

## 4. AI 代理分析 Memecoin

### 4.1 信号类型
- **关键词触发**："launch", "fair", "stealth"
- **KOL 关注**：>10 个 alpha KOL 转发
- **流动性增长**：>50% / 1h
- **Holder 集中度**：<30% 前 10
- **社交音量**：Twitter + Telegram + Discord

### 4.2 风险信号
- 合约无源代码
- Mint authority 未撤销
- 流动性未锁定
- 团队 90% 持仓
- 仿盘（同名 token）

## 5. Python 工具箱

### 5.1 实时 Memecoin 信号

```python
"""
监控 pump.fun / Clanker 新代币
"""
import asyncio
import aiohttp


class MemecoinMonitor:
    PLATFORMS = {
        "pumpfun": "https://frontend-api.pump.fun/coins/latest",
        "clanker": "https://www.clanker.world/api/tokens/recent"
    }

    async def fetch_new_tokens(self, platform: str) -> list:
        async with aiohttp.ClientSession() as session:
            url = self.PLATFORMS.get(platform)
            async with session.get(url, timeout=5) as r:
                return await r.json()

    def filter_signals(self, tokens: list,
                        min_social_score: float = 0.7) -> list:
        signals = []
        for t in tokens:
            score = (t.get('twitter_mentions', 0) / 100
                     + t.get('holder_growth', 0) / 50
                     + t.get('liquidity_usd', 0) / 50000)
            if score > min_social_score:
                signals.append({**t, "score": score})
        return sorted(signals, key=lambda x: -x['score'])
```

### 5.2 持仓分析

```python
"""
分析 Memecoin 持仓结构
"""
import asyncio


async def analyze_token_rug_risk(token_address: str) -> dict:
    return {
        "top10_holder_pct": 0.25,   # <30% 较安全
        "dev_wallet_pct": 0.05,     # <5% 较安全
        "lp_locked": True,
        "mint_authority_renounced": True,
        "freeze_authority_renounced": True,
        "age_hours": 24,
        "liquidity_usd": 50_000,
        "is_rug_risk": False
    }
```

## 6. SocialFi 代币经济

| 平台 | 模型 | 关键代币 | 状态 |
|---|---|---|---|
| Virtuals | bonding curve + LP | VIRTUAL | 极强 |
| DAOS.fun | 治理代币 + 跟投 | - | 增长 |
| FriendTech | 粉丝 = 股份 | - | 2024 末衰退 |
| Lens Protocol | 社交图谱 | LENS | 稳定 |
| Farcaster | Frames + 社交 | DEGEN | 极强 |
| Farcaster / Warpcast | channel | - | 强 |
| Pump.fun | 曲线 | PUMP | 强 |

## 7. AI 代理 + Memecoin 案例

### 7.1 Truth Terminal → GOAT
- 2024-10: AI 自动推 GOAT
- 2024-11: 市值 $1B
- 2024-12: 创始人 a16z Marc Andreessen 投资 $50K
- 2025-Q1: 多个 AI 推 memecoin

### 7.2 aixbt → 30+ 代币
- aixbt 推过的代币 30%+ 短期 >2x
- 跟单群体庞大
- 已被 memecoin 反向利用

### 7.3 Virtuals GAME
- 用户创建 GAME agent
- 自动 bond → 上市
- 部分 agent 12h >100x

## 8. 关键风险

| 风险 | 案例 | 教训 |
|---|---|---|
| Pump & Dump | TURBO 顶峰暴跌 95% | 高位接盘 |
| 合约漏洞 | 多个 rug pull | 审查 source |
| 流动性撤出 | FRIEND 跑路 | 锁 LP |
| AI 幻觉 | 误推垃圾币 | 多源验证 |
| Prompt 注入 | 恶意 KOL 操纵 | 多代理交叉验证 |
| 监管 | 各国对 memecoin 收紧 | 关注 SEC |

## 9. 监管视角

- **美国 SEC**：memecoin 多数不构成证券（Howey Test）
- **中国**：完全禁止
- **欧盟 MiCA**：asset-referenced token (ART) 或 EMT
- **HK**：memecoin 不在 SFC 监管 = 高风险
- **关键判例**：
  - SEC vs Coinbase (2024)：未明确 memecoin
  - SEC vs Binance (2024)：多数 alt = 证券

## 10. 与 03 / 06 / 12 关联

- **03-市场机制**：Memecoin = 极端微观结构案例
- **06-量化**：Memecoin alpha = 短期 + 极端波动
- **12-2026**：机构不参与但要监控系统性风险

## 11. 18 个关键引用

1. Truth Terminal - https://www.truthterminal.io/
2. GOAT (Goatseus Maximus) CoinGecko
3. pump.fun - https://pump.fun/
4. Clanker - https://www.clanker.world/
5. Virtuals Protocol - https://www.virtuals.io/
6. DAOS.fun - https://daos.fun/
7. aixbt - https://aixbt.tech/
8. Bankr - https://bankr.bot/
9. PNUT (Peanut the Squirrel)
10. TURBO Memecoin
11. Believe App
12. MemeX
13. Lens Protocol
14. Farcaster
15. FriendTech
16. DefiLlama Memecoin 数据
17. Dune: Memecoin 仪表盘
18. Memecoin 监管动态

<!-- 文档字数: 约 2400 中文字符 -->
