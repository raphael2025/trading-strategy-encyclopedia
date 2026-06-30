# Solana 主流 DeFi 协议与策略

> 文档版本: 2026-06
> 引用: 25 个
> 知识截止: 2026-05-31

## 1. 协议全景

```
┌──────────┬──────────┬──────────┬──────────┐
│   DEX    │  借贷    │  衍生品  │ 流动质押 │
├──────────┼──────────┼──────────┼──────────┤
│ Jupiter  │  Kamino  │  Drift   │ Marinade │
│ Raydium  │  MarginFi│  Zeta    │ Lido     │
│ Orca     │  Solend  │  Phoenix │ Sanctum  │
│ Phoenix  │  Drift   │  Mango   │ Jito     │
│ OpenBook │  Compound│  Flash   │  BinStaked│
└──────────┴──────────┴──────────┴──────────┘
```

## 2. Jupiter（DEX 聚合器 + Limit Order）

- **地位**：Solana 链最大聚合器，>$2B 日交易量
- **特性**：
  - 路由优化（Raydium / Orca / Phoenix / OpenBook）
  - Limit Order + DCA + TWAP
  - Perps（2024-Q4 上线）
  - 永续合约（Drift + Zeta 集成）
- **JUP 治理**：2024-01 推出，ve-tokenomics 模型
- **关键风险**：
  - 路由选择 bug 历史上导致 $5M 损失
  - 私有 mempool 不完整（仍可 MEV）

## 3. Raydium

- **机制**：AMM + on-chain orderbook（OpenBook 集成）
- **2024 演进**：LaunchLab 代币发行
- **TVL**：>$2B
- **优势**：流动性深度好，新代币 launchpad
- **风险**：CLMM 集中流动性管理复杂

## 4. Orca

- **机制**：CLMM 集中流动性
- **Whirlpools**：集中流动性池
- **定位**：零售友好 UI
- **TVL**：>$1B

## 5. Phoenix（on-chain orderbook）

- **机制**：完整 CLOB，所有订单链上
- **撮合**：链上匹配
- **清算**：on-chain
- **优势**：透明、无需信任、做市商友好
- **劣势**：Gas（但 Solana 便宜）
- **TVL**：>$300M

## 6. Drift Protocol

- **机制**：永续合约（perp）
- **特性**：
  - 现货 + 永续 + 借贷 + 保险
  - 隔离池（isolated markets）
  - 跨保证金
- **TVL**：>$1.5B
- **关键风险**：
  - 历史 2022 风险：$2.7M 漏洞
  - 永续爆仓系统需关注

## 7. Zeta Markets

- **机制**：永续 + 期权
- **DEX 链上期权**：BTC / SOL 美式期权
- **TVL**：>$200M
- **策略**：delta-neutral / covered call

## 8. Kamino（借贷 + 流动性）

- **机制**：集中流动性 + 借贷一体化
- **特色**：
  - 自动流动性管理
  - 杠杆借贷
  - 风险分级
- **TVL**：>$2B
- **KMNO 代币**：2024 推出

## 9. MarginFi

- **机制**：跨保证金借贷
- **特色**：
  - 集成 Drift / Jupiter
  - 风险参数动态调整
- **TVL**：>$500M

## 10. Mango Markets

- **机制**：综合 DeFi（perp + 现货 + 借贷）
- **历史**：2022-10 Avraham Eisenberg 操纵损失 $114M
- **现状**：v4 重启中
- **风险**：操纵攻击史

## 11. Marinade（流动质押）

- **机制**：质押 SOL → mSOL
- **特性**：
  - 100+ 验证人分散
  - 流动质押
- **mSOL**：DeFi 抵押品
- **TVL**：>$1.5B

## 12. Jito Staking

- **机制**：质押 SOL + MEV 收益
- **jitoSOL**：MEV 增强流动质押
- **Jito tip**：Solana MEV 拍卖市场
- **年化**：~7-10%（含 MEV）
- **TVL**：>$3B

## 13. Sanctum（Infinity Pools）

- **机制**：LST（Liquid Staking Token）统一流动性
- **特色**：
  - LST → SOL 0 滑点 swap
  - 跨 LST 互操作
  - LST 收益聚合
- **SANCTUM 代币**：2024 推出

## 14. 跨链桥

| 桥 | 类型 | 优势 |
|---|---|---|
| **Wormhole** | 通用 | 生态最广 |
| **deBridge DLN** | Intent | 见 13-Intent |
| **Mayan** | Auction | 跨链 swap |
| **Allbridge** | 多链 | EVM <-> Solana |
| **LayerZero** | OFT | 标准 OFT |

## 15. 协议策略 cheat sheet

| 协议 | 最佳策略 | 风险等级 |
|---|---|---|
| Jupiter | 聚合 swap | 低 |
| Raydium | Launchpad 抢新 | 中 |
| Orca Whirlpool | 集中流动性 | 中 |
| Phoenix | 做市 | 中 |
| Drift | perp funding 套利 | 中 |
| Zeta | 链上期权 | 中 |
| Kamino | 自动 LP | 低 |
| MarginFi | 跨保证金 | 中 |
| Jito | 质押 + MEV | 低 |
| Marinade | 流动质押 | 极低 |

## 16. Solana 策略

### 16.1 Jito MEV 套利
- 监听 Jito tip 拍卖
- 三角套利
- 清算

### 16.2 Drift funding 套利
- 现货 vs perp funding
- 8-15% 年化

### 16.3 Orca 集中流动性
- 选对范围 → 30%+ APR
- 错误范围 → IL 严重

### 16.4 Jito 质押 + 借贷
- jitoSOL 抵押
- 再借 SOL 循环
- 风险：清算阈值

## 17. 与 03 / 06 / 12 关联

- **03-市场机制**：Solana 微观结构 = 最快链
- **06-量化**：高频策略首选 Solana
- **12-2026**：SOL ETF + 质押收益 → 机构配置

## 18. 25 个关键引用

1. Jupiter Aggregator - https://jup.ag/
2. Raydium - https://raydium.io/
3. Orca - https://www.orca.so/
4. Phoenix DEX - https://phoenix.trade/
5. Drift Protocol - https://drift.trade/
6. Zeta Markets - https://zeta.markets/
7. Kamino Finance - https://kamino.finance/
8. MarginFi - https://marginfi.com/
9. Mango Markets v4
10. Marinade Finance
11. Jito Labs
12. Sanctum
13. Wormhole
14. deBridge
15. Mayan Finance
16. DefiLlama Solana TVL
17. Token Terminal Solana 收入
18. Jupiter DAO 治理
19. Pyth Network
20. Switchboard
21. Jito tip 数据
22. Solana 验证人集合
23. Drift 保险基金
24. Phoenix 做市商文档
25. Sanctum Infinity Pools 文档

<!-- 文档字数: 约 2400 中文字符 -->
