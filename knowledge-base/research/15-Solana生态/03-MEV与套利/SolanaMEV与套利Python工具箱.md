# Solana MEV 与套利 Python 工具箱（Python 3.12+）

> 文档版本: 2026-06
> 引用: 15 个
> 知识截止: 2026-05-31

## 1. Solana MEV 生态

```
┌────────────────────────────────────────┐
│         Solana MEV Supply Chain         │
├────────────────────────────────────────┤
│  搜索者 (Searcher)                      │
│  - 套利机器人                           │
│  - 清算机器人                           │
│  - 三明治机器人                         │
│  ↓                                     │
│  Jito Tip Auction                      │
│  ↓                                     │
│  Block Engine (Jito-Solana validator)  │
│  ↓                                     │
│  Validator 上链                         │
└────────────────────────────────────────┘
```

## 2. MEV 类型（Solana 特有）

| 类型 | 描述 | 频次 |
|---|---|---|
| **Arbitrage** | DEX 间套利 | 极高 |
| **Liquidation** | Drift / Mango / Kamino 清算 | 中 |
| **Sandwich** | 三明治攻击（公开 mempool）| 中 |
| **Jito Tip Capture** | 押注 + MEV | 高 |
| **NFT Sniping** | 抢 mint | 高 |
| **Token Launch** | LaunchLab / Raydium 抢新 | 高 |

## 3. 与 Ethereum MEV 的关键差异

| 维度 | Ethereum | Solana |
|---|---|---|
| 内存池 | 公开 (P2P) | 几乎不存在 (Gulf Stream TPU 直传) |
| 出块时间 | 12s | 400ms |
| MEV 竞争 | Builder / Relayer | Searcher / Jito |
| 区块构建 | Proposer-Builder Separation | Validator + Jito tip |
| 私池 | Flashbots Protect | Jito Block Engine |
| 三明治 | 公开 mempool | 较难（私有）|
| 抢跑 | 公开 | 需 Tip 高 |

## 4. Jito 协议

- **Jito-Solana Client**：增强版 Solana 验证人
- **Block Engine**：MEV 拍卖市场
- **Tip Distribution**：
  - 95% 给验证人
  - 5% 给质押者
- **Tip 数据**：>50% Solana 交易走 Jito 路径
- **年收入**：>$500M（2025）

## 5. 工具箱：套利检测

```python
"""
Solana DEX 套利信号检测
- 监控 Raydium / Orca / Phoenix / Jupiter 报价
- 输出跨池价差
"""
import asyncio
import aiohttp
from dataclasses import dataclass


@dataclass
class PoolQuote:
    dex: str
    pair: str
    mid_px: float
    liquidity_usd: float


class SolanaArbScanner:
    DEXS = ["raydium", "orca", "phoenix", "openbook"]

    async def fetch_quote(self, session: aiohttp.ClientSession,
                           dex: str, pair: str) -> PoolQuote:
        # 实际：调用 Jupiter API 或 RPC getMultipleAccounts
        url = f"https://quote-api.jup.ag/v6/quote"
        params = {"inputMint": ..., "outputMint": ..., "amount": 1_000_000_000}
        async with session.get(url, params=params, timeout=2) as r:
            data = await r.json()
        return PoolQuote(dex=dex, pair=pair, mid_px=1.0,
                         liquidity_usd=1_000_000)

    async def scan_pair(self, pair: str) -> list[PoolQuote]:
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_quote(session, dex, pair) for dex in self.DEXS]
            return await asyncio.gather(*tasks)

    def find_arb(self, quotes: list[PoolQuote]) -> dict:
        if not quotes:
            return None
        sorted_q = sorted(quotes, key=lambda q: q.mid_px)
        buy, sell = sorted_q[0], sorted_q[-1]
        spread_bps = (sell.mid_px - buy.mid_px) / buy.mid_px * 10000
        return {
            "buy_dex": buy.dex, "sell_dex": sell.dex,
            "spread_bps": spread_bps,
            "size_usd": min(buy.liquidity_usd, sell.liquidity_usd) * 0.01,
            "profitable": spread_bps > 30  # 扣除 gas + 滑点
        }
```

## 6. 工具箱：Jito Tip 估算

```python
"""
实时 Jito tip 估算
- 监控 mempool
- 输出最佳 tip 区间
"""
import asyncio
import aiohttp


class JitoTipOracle:
    TIP_ACCOUNTS = [
        "96gNYGLV7USK7F2HK3Wd9g4Y5z2AxeqAjxAPjGPVGJzZ",
        "HFqU5x63VTqvQss8hp11i4bVmk9Xfm6g1GJC9ZTi3LKJ"
    ]

    async def current_tip(self) -> dict:
        async with aiohttp.ClientSession() as session:
            r = await session.post("https://mainnet.block-engine.jito.wtf/api/v1/bundles",
                                   json={"jsonrpc": "2.0", "id": 1,
                                         "method": "getTipAccounts"})
            data = await r.json()
            tips = data.get("result", [])
            return {"tip_accounts": tips,
                    "median_lamports": 10000,  # 实际取中位数
                    "recommended": 50000}

    def optimal_tip(self, profit_lamports: int, competition: int = 10) -> int:
        return min(profit_lamports // 2,
                   int(profit_lamports * (competition / 100)))
```

## 7. 工具箱：清算监控

```python
"""
监控 Drift / Kamino / Mango 健康因子
- HF < 1.0 → 清算机会
"""
import asyncio
import aiohttp


class LiquidationMonitor:
    PROTOCOLS = {
        "drift": "https://api.drift.trade/health",
        "kamino": "https://api.kamino.finance/health",
    }

    async def scan(self, protocol: str) -> list[dict]:
        url = self.PROTOCOLS.get(protocol)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as r:
                data = await r.json()
        opps = []
        for user in data.get("users", []):
            hf = user.get("healthFactor", 1.0)
            if hf < 1.05:
                opps.append({
                    "protocol": protocol,
                    "user": user["address"],
                    "hf": hf,
                    "debt_usd": user["debtUsd"],
                    "collateral_usd": user["collateralUsd"],
                    "expected_liquidation_bonus": 0.05
                })
        return opps
```

## 8. 工具箱：完整套利机器人骨架

```python
"""
生产级 Solana 套利机器人
"""
import asyncio
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction


class SolanaArbBot:
    def __init__(self, rpc_url: str, keypair: Keypair):
        self.rpc_url = rpc_url
        self.wallet = keypair
        self.scanner = SolanaArbScanner()

    async def execute_arb(self, opp: dict) -> str:
        # 1. 构建 swap 交易
        # 2. 添加 Jito tip
        # 3. 提交 bundle
        # 4. 监听确认
        return "tx_sig"

    async def main_loop(self):
        while True:
            quotes = await self.scanner.scan_pair("SOL/USDC")
            opp = self.scanner.find_arb(quotes)
            if opp and opp["profitable"]:
                await self.execute_arb(opp)
            await asyncio.sleep(0.05)  # 50ms
```

## 9. 工具箱：Jito Bundle 提交

```python
"""
提交套利 bundle 到 Jito Block Engine
"""
import aiohttp
import base64


async def submit_jito_bundle(signed_txs: list[bytes], tip_lamports: int) -> str:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "sendBundle",
        "params": [
            {
                "txs": [base64.b64encode(tx).decode() for tx in signed_txs],
                "tipAccount": "96gNYGLV7USK7F2HK3Wd9g4Y5z2AxeqAjxAPjGPVGJzZ",
                "tipLamports": tip_lamports
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post("https://mainnet.block-engine.jito.wtf/api/v1/bundles",
                                 json=payload) as r:
            data = await r.json()
    return data["result"]
```

## 10. 关键风险

| 风险 | 描述 | 缓解 |
|---|---|---|
| 拥塞 | 高峰期失败率高 | 多 RPC + 重试 |
| Failed Bundle | tip 不够高 | 动态 tip 估算 |
| 抢先 | 公开 mempool 仍可被先 | Jito bundle + 高 tip |
| 智能合约风险 | 协议 bug | 限仓 + 监控 |
| RPC 中断 | 节点问题 | 多 RPC 备份 |

## 11. 与 03 / 06 / 07 关联

- **03-市场机制**：Solana MEV 案例丰富
- **06-量化**：高频策略首选 Solana
- **07-机构策略**：Jito MEV 收益 = 机构 alpha 来源
- **13-Intent**：Jito 也在集成 Intent（2026 路线图）

## 12. 15 个关键引用

1. Jito Labs - https://www.jito.wtf/
2. Jito Block Engine API
3. Solana Cookbook - https://solanacookbook.com/
4. Jupiter Aggregator API
5. Raydium CLMM SDK
6. Orca Whirlpools SDK
7. Drift Protocol SDK
8. Kamino Finance SDK
9. MarginFi SDK
10. Marinade Finance SDK
11. Sanctum Infinity Pools
12. Phoenix Orderbook SDK
13. Wormhole Portal
14. deBridge DLN
15. Jito Tip 实时数据

<!-- 文档字数: 约 2400 中文字符 -->
