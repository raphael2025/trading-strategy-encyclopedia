# 加密货币合约交易全知识体系

> **完整版本** 2026-06
> 本知识库覆盖从基础 K 线分析到机构量化交易的完整体系

---

## 目录结构（17 大分类，2026-06）

```
research/
├── 01-技术分析/                # K线、指标、图表形态
├── 02-交易心理学/               # 认知偏差、情绪管理、恐惧贪婪
├── 03-市场机制/                # 流动性、机构操纵
├── 04-宏观政策/                # 监管、地缘、央行
├── 05-期权衍生品/               # 期权基础、Greeks、策略
├── 06-量化交易/                # 框架、策略、风险（含 DePrado DSR/CPCV 工具箱）
├── 07-机构策略/                # 统计套利、高频、多因子
├── 08-代码实现/                # Python库、回测、工具
├── 09-TradingView指标与策略/     # TV 公开脚本 + 实战指标
├── 10-订单簿策略/              # L2/L3 微观结构、OBI、OFI、做市、操纵检测
├── 11-Alpha挖掘/               # 链上/情绪/套利/量价/ML 因子
├── 12-2026机构方法/             # 做市/ETF/监管/托管/AI/风控/资产配置
├── 13-Intent交易/              # 【新】CoW/UniswapX/1inch Fusion/Across/Anoma
├── 14-稳定币风险/              # 【新】USDT/USDC/DAI/USDe 储备 + depeg 监控
├── 15-Solana生态/              # 【新】Jupiter/Drift/Marinade/Jito MEV
├── 16-链上期权/                # 【新】Lyra/Aevo/Hegic/Dopex 协议 + 定价
└── 17-AI Agent交易/            # 【新】ai16z/Eliza/Virtuals/Truth Terminal + 风险
```

> 📌 详细交叉索引见 [INDEX.md](INDEX.md)（5 个新分类 + wiki-link 全图）

---

## 学习路径

### 🟢 初学者路径（0-3 月）

1. **01-技术分析/01-K线基础/K线技术分析详解.md** —— 必读
2. **02-交易心理学/01-认知偏差/交易心理学详解.md** —— 必读
3. **03-市场机制/01-流动性/流动性猎杀机制.md** —— 必读
4. **06-量化交易/03-风险管理/量化策略的风险预算与组合配置.md** —— 了解

**目标**：理解市场基本结构，规避常见陷阱

### 🟡 进阶路径（3-12 月）

1. **01-技术分析/02-技术指标/技术指标深度解析.md**
2. **01-技术分析/03-图表形态/图表形态识别.md**
3. **02-交易心理学/03-情绪管理/情绪管理系统.md**
4. **04-宏观政策/01-监管/监管政策影响.md**
5. **05-期权衍生品/01-基础/期权交易基础.md**
6. **06-量化交易/02-策略开发/策略开发指南.md**

**目标**：建立完整的交易系统

### 🔴 专业交易员（12+ 月）

1. **05-期权衍生品/02-希腊字母/Greeks与波动率曲面.md**
2. **05-期权衍生品/03-策略组合/期权策略组合.md**
3. **06-量化交易/01-框架/量化交易框架.md**
4. **07-机构策略/01-统计套利/统计套利策略.md**
5. **07-机构策略/02-高频/高频交易策略.md**
6. **07-机构策略/03-多因子/多因子模型.md**
7. **08-代码实现/**（全模块）
8. **09-TradingView指标与策略/**（全模块）
9. **10-订单簿策略/订单簿策略与微观结构.md**
10. **11-Alpha挖掘/加密Alpha挖掘全谱.md**
11. **12-2026机构方法/2026加密机构方法论.md**

**目标**：机构级量化策略研究与执行

---

## 主题模块详解

### 1. 技术分析（3 个文档）

| 文档 | 字数 | 重点 |
|------|------|------|
| K线技术分析详解 | ~10K | 各种K线形态、组合形态、实战应用 |
| 技术指标深度解析 | ~12K | 趋势/震荡/成交量/波动率指标 |
| 图表形态识别 | ~12K | 17种形态 + Bulkowski 统计数据 |

**核心来源**：Bulkowski《Encyclopedia of Chart Patterns》、Wikipedia 形态分类

### 2. 交易心理学（3 个文档）

| 文档 | 字数 | 重点 |
|------|------|------|
| 交易心理学详解 | ~17K | 12种认知偏差 + 加密特色 |
| 恐惧贪婪指数分析 | ~10K | FGI 指标详解 + 实战应用 |
| 情绪管理系统 | ~12K | Steenbarger 协议 + HRV 监测 |

**核心来源**：Kahneman、Mark Douglas、Brett Steenbarger、Coates PNAS 研究

### 3. 市场机制（2 个文档）

| 文档 | 字数 | 重点 |
|------|------|------|
| 流动性猎杀机制 | ~9K | 6种猎杀手法 + 防御策略 |
| 机构操纵手法识别 | ~9K | 13类操纵 + 5大监管案例 |

**核心来源**：Wikipedia、CFTC、SEC、Chainalysis、NBER

### 4. 宏观政策（3 个文档）

| 文档 | 字数 | 重点 |
|------|------|------|
| 监管政策影响 | ~11K | 8大法域 + MiCA + 5大案例 |
| 地缘政治因素 | ~7K | 制裁与反制裁 + 稳定币地缘工具 |
| 央行政策传导 | ~7K | 4大传导渠道 + 央行政策详解 |

**核心来源**：Fed/ECB/BOJ 官方文件、BIS、Wikipedia

### 5. 期权衍生品（3 个文档）

| 文档 | 字数 | 重点 |
|------|------|------|
| 期权交易基础 | ~6K | Black-Scholes + 加密期权市场 |
| Greeks 与波动率曲面 | ~7K | 5大 Greeks + 波动率曲面 |
| 期权策略组合 | ~8K | 18种策略 + 加密特色 |

**核心来源**：Deribit、Greeks.live、Hull《Options, Futures, and Other Derivatives》

### 6. 量化交易（3 个文档）

| 文档 | 字数 | 重点 |
|------|------|------|
| 量化交易系统全栈架构 | ~11K | 7层架构 + 完整技术栈 |
| 策略开发全流程与回测陷阱 | ~10K | 8阶段流程 + 7大陷阱 |
| 风险预算与组合配置 | ~8K | 风险度量 + 加密特殊风险 |

**核心来源**：QuantConnect、Lean、Backtrader、VectorBT、Lopez de Prado 著作

### 7. 机构策略（3 个文档）

| 文档 | 字数 | 重点 |
|------|------|------|
| 统计套利与配对交易 | ~8K | Gatev 经典 + Avellaneda 框架 |
| 做市与高频策略 | ~10K | Avellaneda-Stoikov + MEV |
| 多因子模型与跨资产信号 | ~10K | 8大加密因子 + 跨资产信号 |

**核心来源**：Fama-French、AQR、Renaissance、Man AHL 公开材料

### 8. 代码实现（3 个文档）

| 文档 | 字数 | 重点 |
|------|------|------|
| CCXT 与加密数据接口 | ~15K | 100+交易所 + 完整代码 |
| Backtrader 与 VectorBT 回测 | ~16K | 7种框架对比 + 实战 |
| 链上数据与监控告警工具链 | ~21K | 5大服务商 + 监控告警 |

**核心来源**：CCXT 官方文档、Glassnode、Nansen、Dune Analytics

### 9. TradingView 指标与策略（4 个文档）

| 文档 | 字数 | 重点 |
|------|------|------|
| TradingView 公开脚本与信号源 | ~12K | TV 内置 100+ 指标、Pine Script 入门、付费脚本市场 |
| 自定义指标编写（Pine Script v5） | ~10K | 完整 Pine v5 语法 + 加密实战指标（Supertrend/CM_Williams/Vortex） |
| TradingView 策略回测与信号源 | ~8K | 信号回测 + 预警 API + 自动化接入 |
| 加密图表形态与机构常用指标 | ~8K | 17 种 TV 形态 + 机构级 TV 面板 |

**核心来源**：TradingView Wiki、Pine Script v5 Reference、TradingView Public Scripts

### 10. 订单簿策略（1 个文档）

| 文档 | 字数 | 重点 |
|------|------|------|
| 订单簿策略与微观结构 | ~8K | L2/L3 数据、OBI/Microprice/Cont-Kukanov-Stoikov、OFI/Kyle's Lambda/Amihud/Glosten-Harris、做市/激进策略、操纵检测、ML 与工程实现 |

**核心来源**：Cont, Kukanov, Stoikov (2011 排队模型)、Kyle (1985)、Glosten-Harris (1988)、Stoikov (2018)、Cartea-Jaimungal-Penalva (2015)、Glassnode Kaiko Amberdata 文档

### 11. Alpha 挖掘（1 个文档）

| 文档 | 字数 | 重点 |
|------|------|------|
| 加密 Alpha 挖掘全谱 | ~7.5K | 链上/情绪/套利/量价/另类数据/ML 七大类 + decay 管理 + 机构实战 + 2026-2027 趋势 |

**核心来源**：López de Prado (2018) *AFML*、Bailey & López de Prado (2014) DSR、Kakushadze (2015) 101 Alphas、Glassnode/CoinMetrics/Nansen/CryptoQuant

### 12. 2026 机构方法（1 个文档）

| 文档 | 字数 | 重点 |
|------|------|------|
| 2026 加密机构方法论 | ~8K | 机构生态、做市、ETF 矩阵、监管合规、托管、RL/AI、风控、执行、资产配置、失败案例 |

**核心来源**：Galaxy Research、CoinShares、a16z State of Crypto、MiCA (EUR-Lex)、BIS WP 1086、TRM Labs/Chainalysis/Elliptic、JPM Deep Hedging、BNP RL Market Making

---

## 数据来源说明

### 完全网络深度搜索的文档（6 个）
- 交易心理学详解
- 情绪管理系统
- 图表形态识别
- 流动性猎杀机制
- 机构操纵手法识别
- 期权基础与定价直觉

### 基于公开权威数据 + AI 整理的文档（17 个）
所有其他文档基于以下权威来源整理：
- 学术论文（PNAS, Sci Rep, JSTOR）
- 监管文件（SEC, CFTC, Wikipedia 法律记录）
- 行业研究（Glassnode, Nansen, CryptoQuant）
- 公开数据（Kaiko, Deribit, Bit.com）
- 经典著作（Hull, Chan, Lopez de Prado, Bulkowski, Douglas, Steenbarger）

---

## 关键统计

- **总文档数**：29+（12 大模块，2024-2026 持续扩展）
- **总字数**：约 30-35 万字
- **覆盖主题**：12 大模块（基础 8 类 + TV 指标 + 订单簿 + Alpha + 机构方法）
- **引用源**：300+ 学术与权威来源（arXiv/SSRN/BIS/Galaxy/CoinShares/MiCA/JPM/BNP）
- **代码示例**：50+ 可执行代码片段
- **关键数据点**：300+ 数据表格
- **2026 新增**：4 个新分类（09 TradingView、10 订单簿、11 Alpha、12 机构方法）共约 8 个新文档，~32K 字，~120 引用

---

## 重要免责声明

⚠️ **本知识库仅供学习研究使用，不构成任何投资建议**

- 加密货币交易风险极高，可能损失全部本金
- 过往表现不代表未来收益
- 监管政策处于快速演变期
- 统计数据来自多个公开来源，可能存在统计差异
- AI 整理内容可能存在错误，请交叉验证关键信息

---

## 致谢

本知识库基于以下来源整理：
- 学术界：Kahneman, Fama, French, Markowitz, Sharpe 等
- 行业实践：Glassnode, Nansen, CCXT, Deribit, BitMEX, Binance Research
- 监管机构：SEC, CFTC, MiCA, FATF, BIS
- 加密社区：Wikipedia, 各类学术期刊, 行业研究报告
- AI 辅助：OpenHands AI 整理和补充

---

**最后更新**：2026 年 6 月
**维护者**：OpenHands AI 代理
**许可证**：本知识库遵循 MIT 协议
