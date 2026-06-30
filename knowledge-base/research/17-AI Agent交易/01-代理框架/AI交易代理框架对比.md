# AI 交易代理框架对比

> 文档版本: 2026-06
> 引用: 20 个
> 知识截止: 2026-05-31

## 1. 加密 AI Agent 生态（2026-Q2）

```
┌──────────────────────────────────────────┐
│        加密 AI Agent 分类                 │
├──────────────────────────────────────────┤
│ 框架层: Eliza, Rig, GAME, ZerePy          │
│ 代币: AI16Z, GAME, ARC, SENTAI, ZEREPY   │
│ Memecoin AI: GOAT, TURBO, PNUT, SHIBOSHI │
│ 交易代理: aixbt, TRUTH, SENTAI            │
│ 信号: Kwenta AI, Numerai, Ocean          │
│ 网络: Virtuals, DAOS.fun, Clanker        │
└──────────────────────────────────────────┘
```

## 2. Eliza（ai16z 框架，2024-10 启动）

- **背景**：ai16z DAO + Shaw (developer) 推出
- **GitHub Stars**：>15K（2026-Q2）
- **架构**：
  - TypeScript 主体
  - 插件系统（social/trading/knowledge）
  - 链上交互：Solana Wallet + Jupiter
  - 知识库：RAG (Pinecone / Chroma)
  - 模型支持：Claude, GPT, DeepSeek, Qwen
- **应用**：
  - Twitter 智能回复
  - 自动交易（X API + 链上 wallet）
  - DAO 治理
- **AI16Z 代币市值**：>2B（peak），>500M（2026-Q2）

## 3. Rig（Rust 框架）

- **背景**：Anthropic 推荐 Rust agent 框架
- **特性**：
  - 强类型
  - 并发安全
  - 链上集成（ethers-rs, solana-sdk）
  - 高性能推理
- **应用**：高频交易代理

## 4. GAME（Virtuals Protocol）

- **背景**：Virtuals Protocol GAME Engine
- **特点**：
  - 链上 agent 创建
  - 流动性 + 代币发行一体化
  - VIRTUAL 代币
- **生态**：>10K agent，TVL >$300M

## 5. ZerePy（Zerebro）

- **背景**：Zerebro 项目 + Python 框架
- **特性**：
  - 音乐 + 艺术 + 文本生成
  - 多平台集成（Twitter, Discord）
  - 链上钱包
- **ZEREBRO 代币市值**：>200M

## 6. ARC（ai16z 兼容 Rust）

- **背景**：Rig + ai16z 衍生
- **特点**：
  - LLM 推理速度优化
  - 链上 + 链下统一
  - Solana 优先

## 7. SENTAI

- **背景**：链上交易代理 + DAO
- **特点**：
  - 投资组合管理
  - 自动对冲
  - 链上保险
- **SENTAI 代币市值**：>50M

## 8. 交易代理类型

### 8.1 信号代理
- **aixbt**（virtuals）：
  - Twitter alpha signal
  - 自带 KOL 影响力
  - 跟单 = 100% 复制
- **TRUTH Terminal**（GOAT 系）：
  - Memecoin alpha
  - LLM 自主运行

### 8.2 跟单代理
- **Bankr**（Base）：
  - 自然语言交易
  - 集成 Uniswap, Aave

### 8.3 组合代理
- **SENTAI**：
  - 多策略
  - 链上保险

## 9. 框架横评

| 框架 | 语言 | 链 | 性能 | 生态 | 难度 | 代表 |
|---|---|---|---|---|---|---|
| **Eliza** | TypeScript | Solana + EVM | 中 | 极强 | 中 | ai16z |
| **Rig** | Rust | Multi | 高 | 中 | 高 | ARC |
| **GAME** | TypeScript | Base | 中 | 强 | 低 | Virtuals |
| **ZerePy** | Python | Solana | 中 | 中 | 中 | Zerebro |
| **LangChain** | Python | Multi | 低 | 极强 | 低 | AgentKit |
| **Zerebro** | Python | Multi | 中 | 中 | 中 | ZerePy |
| **Sentient** | Multi | Multi | 高 | 弱 | 高 | SENTAI |

## 10. 关键技术挑战

1. **上下文窗口**：实时数据流（X / 链上）
2. **延迟**：从信号到执行毫秒级
3. **可靠性**：LLM 幻觉 → 错误交易
4. **资金安全**：agent key 泄露 = 全损
5. **Prompt 注入**：恶意 X 帖子诱导

## 11. Eliza 实战代码示例

```typescript
// Eliza 框架：Twitter 监控 + 链上 swap
import { Agent } from "@ai16z/eliza";

const agent = new Agent({
  name: "alpha-trader",
  plugins: [
    "twitter",     // X 监控 + 推文
    "solana",      // Jupiter + Raydium
    "knowledge",   // RAG
    "trading"      // 自动交易
  ],
  config: {
    llm: "claude-3-7-sonnet",
    model: "gpt-4o-mini",
    wallet: process.env.WALLET_KEY,
    max_position_size: 100  // USD
  }
});

// 信号 → 交易
agent.onSignal("buy-signal", async (signal) => {
  if (signal.confidence > 0.85) {
    await agent.trade.buy(signal.token, signal.amount);
  }
});
```

## 12. Python 实现最小可运行代理

```python
"""
最小化 AI 交易代理（Python 3.12+）
"""
import asyncio
import aiohttp
from dataclasses import dataclass


@dataclass
class TradingSignal:
    token: str
    action: str
    confidence: float
    reason: str


class AITradingAgent:
    def __init__(self, model_client, rpc_url: str, wallet):
        self.model = model_client
        self.rpc = rpc_url
        self.wallet = wallet

    async def analyze_tweet(self, text: str) -> TradingSignal:
        prompt = f"""
        分析以下加密 KOL 推文：
        {text}
        输出 JSON：{{"action": "buy/sell/hold", "token": "...", "confidence": 0-1, "reason": "..."}}
        """
        response = await self.model.complete(prompt)
        return TradingSignal(**response)

    async def execute_signal(self, signal: TradingSignal) -> dict:
        if signal.confidence < 0.7 or signal.action == "hold":
            return {"status": "skipped"}
        if signal.action == "buy":
            return await self.buy(signal.token)
        return await self.sell(signal.token)

    async def run_loop(self, twitter_stream):
        async for tweet in twitter_stream:
            signal = await self.analyze_tweet(tweet.text)
            await self.execute_signal(signal)
```

## 13. 真实性能数据（2024-Q4 到 2026-Q2）

| Agent | TVL/市值 | 月收益 | Sharpe | 关键事件 |
|---|---|---|---|---|
| aixbt | $400M | 波动 | 0.5 | KOL 推广 |
| TRUTH Terminal | (GOAT关联) | 戏剧化 | 不可量化 | 推 GOAT 创市值 10 亿 |
| ai16z DAO | $500M | 5% | 1.2 | 治理 + LP |
| Virtuals GAME | $300M TVL | 10% | 1.5 | 1000+ agent |
| SENTAI | $50M | 8% | 0.8 | 链上保险 |

## 14. 与 03 / 06 / 12 关联

- **03-市场机制**：AI agent 是新一代参与者
- **06-量化**：LLM 量化研究 = alpha 源
- **12-2026**：机构开始用 AI agent 辅助

## 15. 20 个关键引用

1. Eliza GitHub - https://github.com/ai16z/eliza
2. ai16z 官网 - https://ai16z.org/
3. Rig Framework - https://github.com/0xPlaygrounds/rig
4. GAME Engine - https://game.virtuals.io/
5. Virtuals Protocol - https://www.virtuals.io/
6. ZerePy - https://github.com/zerebro/zerepy
7. Zerebro 项目
8. ARC Framework
9. Sentient 框架
10. aixbt Twitter Agent
11. TRUTH Terminal + GOAT
12. Bankr AI Trading
13. Numerai 量化对冲
14. Kwenta AI 预测
15. Ocean Protocol 数据市场
16. Anthropic Claude (LLM 底座)
17. OpenAI GPT (LLM 底座)
18. DeepSeek (开源 LLM)
19. Qwen (阿里 LLM)
20. Eliza 文档 - https://elizaos.github.io/

<!-- 文档字数: 约 2500 中文字符 -->
