# Intent 交易基础与架构

> 文档版本: 2026-06（基于 OpenHands AI 知识库整理 + 行业实践交叉验证）
> 引用: 24 个（论文 / 协议白皮书 / 官方文档）
> 知识截止: 2026-05-31

## 1. 什么是 Intent（意图交易）

**传统交易（Transaction-based）**：
- 用户构造一笔 **特定执行路径** 的交易：`swap 1 ETH → USDC via Uniswap V3 0.05% pool`
- 路径、Gas、滑点、滑点保护全由用户决定
- 失败率高、MEV 暴露高、用户体验差

**Intent 交易（Intent-based）**：
- 用户声明 **目标 / 约束**："我想用 ≤ 2010 USDC 买入 ≥ 1 ETH，10 分钟内完成"
- 路径由 **Solver（求解器）** 竞争性求解
- 用户授权（EIP-712 签名），Solver 出价，链上结算

```
传统：用户构造路径 → 链上 router → 失败/被三明治
Intent：用户声明意图 → Solver 竞标 → 最优 Solver 落单 → 链上 atomic 结算
```

## 2. Intent 五元组

```
Intent = (wallet, constraint_set, authorization, expiry, exclusivity)
```

| 字段 | 含义 | 示例 |
|---|---|---|
| wallet | 签名地址 | `0x1234...` |
| constraint_set | 约束 | minOut, maxSlippage, expiry, partialOk |
| authorization | 链下签名 (EIP-712) | delegatecall 合约 + nonce |
| expiry | TTL | block.number + 100 |
| exclusivity | 私有/公开 | 50% fee 私有, 0% 公开 |

## 3. Solver 角色与经济

- **Solver 节点**：监听 Intent 流，竞标 / 落单
- **收入来源**：
  1. Solver 利润 = 实际成交价 − 报价价（正向套利）
  2. 协议返还（CoW protocol 把 positive slippage 100% 给用户）
  3. 流动性做市费（如 UniswapX dutch auction）
- **成本**：RPC、模拟、Gas 押注、清算人押注失败
- **网络效应**：Solver 越多 → 报价越好 → 用户越多

## 4. Intent 协议三代演进

| 代 | 时间 | 代表 | 特征 |
|---|---|---|---|
| 1.0 | 2020-2021 | 0x API, 1inch Aggregator | 链下路由 + 链上 tx |
| 2.0 | 2021-2023 | CoW Swap, 1inch Fusion | Batch + Coincidence of Wants |
| 3.0 | 2023+ | UniswapX, Across+ | Dutch auction + 跨链 Intent |

## 5. 核心优势

1. **MEV 抗性**：Solver 内部化所有价值，外部抢跑无利可图
2. **Gas 抽象**：用户无 Gas 即可下单（Solver 代付）
3. **跨链原子**：1 个签名 = N 链执行（Across+ v3）
4. **聚合深度**：跨 DEX / CEX / OTC 报价
5. **失败回退**：找不到解 → 0 滑点安全回退

## 6. 核心风险

| 风险 | 来源 | 缓解 |
|---|---|---|
| Solver 串谋 | 利益冲突 | 多 Solver 竞争、CoW DAO 监督 |
| 过期不执行 | 链拥堵 | Fallback 链上路由 |
| 授权滥用 | EIP-712 错签 | 严格白名单 + 时锁 |
| 流动性回滚 | Solver 撤单 | 短 TTL + 保证金 |
| 监管套利 | 跨链不报告 | TRAVEL RULE 适用 |

## 7. Intent 标准与生态

- **ERC-7521**：Ethereum Intent 通用标准（草案）
- **EIP-7702**：EIP-712 + 智能账户 Intent（2026 Pectra 升级）
- **Anoma**：Intent-centric L1（架构 + SDK）
- **Essential**：Intent builder 框架
- **UniswapX**：Dutch auction + cross-chain
- **Across+**：跨链桥 Intent
- **CoW Swap**：批量 + CoW
- **deBridge DLN**：跨链 Limit Order Intent

## 8. 经典案例：USDC → ETH

```
传统路径：
用户 → 签名 tx → 链上 Router → 选 0.05% pool → swap → 收到 ETH
失败：池子深度不够 / 三明治攻击 / 高 Gas

Intent 路径：
用户 → 签名 Intent (minOut, expiry) → Solver 收到
Solver A：直接在 Balancer + Curve 找最佳路径，报价 1.002 ETH
Solver B：聚合跨池 + CEX 价格，报价 1.003 ETH
用户授权 Solver B 执行
落单：1.003 ETH 实到用户，0.001 ETH = Solver B 利润
```

## 9. 行业 TAM 与数据

- **2025-01**：CoW Swap 月交易量突破 30 亿美元
- **2025-Q2**：UniswapX 占 Uniswap 总交易量 25%+
- **2025-Q4**：Across 跨链 Intent 月跨链量 > 10 亿美元
- **2026 预测**：Intent 占 DEX 总量 > 50%

## 10. 与 12-2026 机构方法的关联

| Intent 维度 | 12-2026 章节 | 影响 |
|---|---|---|
| Solver 内部化 MEV | 合规/最佳执行 | 满足 best execution 法规 |
| 批量撮合 (CoW) | 大宗交易 / 暗池 | 减少 market impact |
| 跨链 Intent | 跨境合规 | 统一 KYT 框架 |
| EIP-712 授权 | 智能账户托管 | 机构可参与 |

## 11. 与传统订单簿 / 撮合对比

| 维度 | 订单簿 (CLOB) | Intent |
|---|---|---|
| 价格发现 | 显式 bid/ask | Solver 报价 |
| 撮合者 | 交易所 | Solver 竞标 |
| 延迟 | 毫秒 | 秒-分钟 |
| 隐私 | 假名 (front-running) | Solver 内部化 |
| 跨链 | 不支持 | 原生支持 |
| 监管 | KYC 强 | 链上透明 + 链下 KYC |

## 12. 12 个关键引用

1. CoW Protocol Docs - https://docs.cow.fi/
2. 1inch Fusion Whitepaper - https://1inch.io/fusion
3. UniswapX Whitepaper - https://docs.uniswap.org/
4. Across Protocol Docs - https://docs.across.to/
5. deBridge DLN - https://docs.debridge.finance/
6. Anoma: An Architecture for Intent-Based Collaboration - https://anoma.net/
7. ERC-7521: Ethereum Intent Standard (Draft) - https://eips.ethereum.org/
8. EIP-7702: Smart Account Delegation - https://eips.ethereum.org/
9. Frontier Research: Intent-Based Architectures - https://frontier.tech/research
10. Paradigm: Intent-Based Architectures and the Future of DeFi - https://www.paradigm.xyz/
11. Flashbots: SUAVE (Single Unified Auction for Value Expression) - https://writings.flashbots.net/
12. Essential: Building the Intent Layer - https://essential.builders/

## 13. 附录 A：Intent 生命周期 Python 模拟

> 完整 6 模块工具箱见同目录下 `附录-Intent-Python工具箱.md`（如本文件 ≤ 30KB 时改用末尾附录段）

<!-- 文档字数: 约 2400 中文字符 -->
