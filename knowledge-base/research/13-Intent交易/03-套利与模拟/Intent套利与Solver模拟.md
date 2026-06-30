# Intent 套利与 Solver 模拟（Python 3.12+）

> 文档版本: 2026-06
> 引用: 15 个
> 知识截止: 2026-05-31

## 1. Solver 经济模型

**收入侧**：
1. 落单利润（solver px − chain mid）
2. MEV 内部化（无外部抢跑）
3. 用户返佣（极少数协议给 Solver rebate）

**成本侧**：
1. RPC / 节点
2. 模拟失败成本
3. 押注损失（Across）
4. MEV 再分配（CoW）

**盈亏平衡点**：
```
Solver 月利润 > 节点成本 + 团队工资 + 押注资金机会成本
```

## 2. 套利场景

### 2.1 CEX-DEX 套利 + Intent
```
信号：CEX 价 < DEX 价 0.1%
操作：
  1. CEX 买入（限价单）
  2. 提交 Intent：CEX 卖出数量 → 链上目标 token
  3. Solver 落单 → 内部吃价差
```

### 2.2 跨链套利
```
信号：ETH 主网 ETH = $2010，Arbitrum ETH = $2015
操作：
  1. 主网买入 Intent（Across+ 桥至 Arbitrum）
  2. Arbitrum 卖出 Intent
  3. 1 个签名链下 2 笔 tx
```

### 2.3 CoW 内部套利
```
信号：同 batch 内 2 个用户想 1 ETH → USDC 与 USDC → ETH
Solver 撮合：直接 P2P 内部对敲
Solver 利润：0（CoW 把 surplus 全给用户）
Protocol 奖励：Solver 拿 COW token
```

## 3. Python 工具箱

### 3.1 EIP-712 Intent 签名生成

```python
"""
EIP-712 离线签名 Intent
- 钱包：Geth/ethers.js
- 验证：链上 verify(Intent, signature)
"""
import time
from eth_account import Account
from eth_account.messages import encode_typed_data


def sign_intent(wallet: Account, chain_id: int, verifier: str,
                intent: dict) -> dict:
    typed = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"}
            ],
            "Intent": [
                {"name": "trader", "type": "address"},
                {"name": "inputToken", "type": "address"},
                {"name": "inputAmount", "type": "uint256"},
                {"name": "minOutput", "type": "uint256"},
                {"name": "expiry", "type": "uint256"},
                {"name": "nonce", "type": "uint256"}
            ]
        },
        "primaryType": "Intent",
        "domain": {"name": "IntentProtocol", "version": "1",
                    "chainId": chain_id, "verifyingContract": verifier},
        "message": {
            "trader": wallet.address,
            "inputToken": intent["inputToken"],
            "inputAmount": intent["inputAmount"],
            "minOutput": intent["minOutput"],
            "expiry": int(time.time()) + 600,
            "nonce": intent["nonce"]
        }
    }
    sig = wallet.sign_message(encode_typed_data(full_message=typed))
    return {"intent": typed["message"], "signature": sig.signature.hex()}
```

### 3.2 Solver 利润模拟

```python
"""
模拟 100 个 Intent 流入 5 个 Solver 的竞争
- 每个 Solver 报价不同
- 利润 = 报价 - 实际链上成本
"""
import numpy as np
import pandas as pd


def simulate_solver_competition(n_intents: int = 100, n_solvers: int = 5,
                                 fee_bps: float = 5) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []
    for i in range(n_intents):
        size = rng.lognormal(8, 1.5)
        true_cost = size * (1 - rng.uniform(0, 0.003))
        quotes = []
        for _ in range(n_solvers):
            spread = rng.uniform(0.0001, 0.002)
            quotes.append(true_cost * (1 - spread))
        winner = rng.integers(n_solvers)
        profit = (quotes[winner] - true_cost) * size
        rows.append({"intent_id": i, "size": size, "winner": winner,
                     "profit": profit})
    return pd.DataFrame(rows)


def solver_pnl_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("winner").agg(
        wins=("intent_id", "count"),
        total_profit=("profit", "sum"),
        avg_profit=("profit", "mean"),
        fill_rate=("intent_id", lambda x: len(x) / df['intent_id'].nunique())
    )
```

### 3.3 Dutch Auction 价格衰减

```python
"""
UniswapX 风格 Dutch Auction
- 起价 = 用户最优
- 终价 = Solver 最优
- 线性衰减
"""
import numpy as np


def dutch_auction_px(start_px: float, end_px: float,
                      duration_sec: int, t: float) -> float:
    """t: 自拍卖开始时间"""
    progress = min(t / duration_sec, 1.0)
    return start_px * (1 - progress) + end_px * progress
```

### 3.4 CoW Batch 撮合（简化版）

```python
"""
简化版 CoW：单 batch 内最大化 P2P 匹配
"""
from collections import defaultdict


def cow_match(intents: list, max_batch_size: int = 50) -> dict:
    """
    intents: [{side, token_in, token_out, amount}]
    """
    inventory = defaultdict(lambda: defaultdict(float))
    filled = []
    for intent in intents:
        pair = (intent['token_in'], intent['token_out'])
        opp_pair = (intent['token_out'], intent['token_in'])
        if inventory[opp_pair].get(intent['amount'], 0) > 0:
            inventory[opp_pair][intent['amount']] -= intent['amount']
            filled.append({**intent, 'fill_type': 'cow'})
        else:
            inventory[pair][intent['amount']] += intent['amount']
            filled.append({**intent, 'fill_type': 'amm'})
    return {'matches': filled,
            'cow_fill_rate': sum(1 for f in filled if f['fill_type'] == 'cow') / len(intents)}
```

### 3.5 跨链套利信号

```python
"""
监控 CEX + 链上价格，输出 Intent 套利信号
"""
import ccxt
import pandas as pd


def arb_signal(symbol: str = "ETH/USDT", min_spread_bps: float = 30) -> dict:
    binance = ccxt.binance()
    binance_px = binance.fetch_ticker(symbol)['last']
    web3_px = 2010.0  # 模拟链上预言机
    spread_bps = (web3_px - binance_px) / binance_px * 10000
    return {
        "symbol": symbol,
        "cex_px": binance_px,
        "chain_px": web3_px,
        "spread_bps": spread_bps,
        "action": "buy_cex_sell_intent" if spread_bps > min_spread_bps
                    else "none"
    }
```

## 4. Solver 基础设施 checklist

| 模块 | 必需 / 可选 | 选型 |
|---|---|---|
| RPC | 必需 | Alchemy / Infura / 自建 Erigon |
| 模拟 | 必需 | Tenderly / eth_call / revm |
| 路径搜索 | 必需 | 自研 + 1inch Aggregator API |
| 监控 | 必需 | Prometheus + Grafana |
| MEV-Block | 推荐 | Flashbots Protect / mev-blocker |
| 抢跑保护 | 推荐 | MEV-Share / CoW protocol |
| 链支持 | 必需 | Ethereum / Arbitrum / Base / OP / Polygon |
| Solver 资金 | 必需 | 100+ ETH (跨链 swap) |

## 5. 利润预估（2026 年 5 月）

| 场景 | 落单量 | 利润率 | 月利润 ($) |
|---|---|---|---|
| UniswapX Filler | $50M | 2-5 bps | $10K-25K |
| CoW Solver | $30M | 1-3 bps | $3K-9K |
| Across+ Relayer | $20M 跨链 | 5-15 bps | $10K-30K |
| 自营跨链套利 | $5M | 10-30 bps | $5K-15K |

## 6. 监管与合规

- **OFAC 制裁名单**：必须集成 Chainalysis / TRM
- **KYT (Know Your Transaction)**：所有跨链 Intent 必经
- **Travel Rule**：>$3K 跨链需双方 VASP 标识
- **MiCA VASP 注册**：EU 用户需在 EU 注册实体

## 7. 与 03-市场机制关联

- Intent 是 **微观结构** 的最新演进（参见 `../../03-市场机制/02-机构操纵/机构操纵手法识别.md`）
- Solver 串谋 = 隐性 market maker
- Batch auction = 微观时间内的中央限价簿

## 8. 与 12-2026 机构方法关联

- 机构大单 → 必然走 Intent (CoW/1inch Fusion+)
- best execution 法规 → Intent 提供 auditable trail
- 跨境合规 → Across+ + Travel Rule 集成

## 9. 15 个关键引用

1. CoW Protocol - https://docs.cow.fi/
2. UniswapX Docs - https://docs.uniswap.org/
3. 1inch Fusion Mode
4. Across Protocol v3
5. deBridge DLN
6. Anoma Whitepaper
7. ERC-7521 EIP 草案
8. EIP-7702 智能账户
9. EIP-712 typed data
10. Flashbots SUAVE
11. MEV-Share
12. LayerZero V2
13. CCXT 库
14. Tenderly 模拟服务
15. eth-account 库

## 10. 附录：完整项目结构

```
intent-bot/
├── solver/
│   ├── monitor.py          # Intent 流监听
│   ├── router.py           # 路径搜索
│   ├── executor.py         # 落单
│   └── risk.py             # 押注 + 失败保护
├── config/
├── tests/
└── README.md
```

<!-- 文档字数: 约 2200 中文字符 -->
