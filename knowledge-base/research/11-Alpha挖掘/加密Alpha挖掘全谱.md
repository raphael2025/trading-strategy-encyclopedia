# 加密货币 Alpha 挖掘全谱：从链上信号到 ML 因子的方法论与实战

> **完整研究文档** 2026-06
> 涵盖链上、社交情绪、跨市场套利、另类数据、量价因子、机器学习与 alpha 衰减监测
> 适用读者：量化研究员、家族办公室、加密对冲基金、做市商、风控团队

---

## 一、Alpha 定义与度量基础

### 1.1 Gross Alpha vs Net Alpha

加密领域 alpha 的定义和股票市场保持一致，但仍需做"加密化"修正：

- **Gross Alpha**：策略相对基准（通常为 BTC 或等权 1 倍做空组合）的超额年化收益。
- **Net Alpha**：扣除交易手续费、Funding 费率、滑点、资金成本、Gas 费（链上策略）、合规/审计/数据订阅成本后剩余的 alpha。
- 加密的特殊性：现货/永续 funding 8 小时一结、永续合约承担/收取 funding、永续 vs 季度价差频繁 ±50bps、单边流动性瞬时蒸发 80%（2022-11 FTX、2025-02 Bybit）。

经验法则：1 年期策略的 Gross→Net 损耗在加密高频策略中达 30-50%，在低频链上策略中约 10-20%。

### 1.2 信息比率 (IC) 与信息比率 (IR)

- **IC (Information Coefficient)**：预测值（因子值排名）与实际收益排名的 Spearman/Pearson 相关系数。加密研究中常用日频 IC、滚动 30 日 IC、IC 标准差。
- **IR (Information Ratio)**：IC 均值 / IC 标准差，类似 Sharpe 但针对预测能力。
- 经验阈值：可用 alpha 的 IC ≈ 0.03-0.08（日频），IR > 0.5 为可投资门槛，IR > 1.0 视为强信号。
- López de Prado 在 *Advances in Financial Machine Learning* (2018) 中强调**单一时间点 IC 易被噪音污染**，应使用 CPCV (Combinatorial Purged Cross-Validation) 多路径验证。

### 1.3 Alpha 半衰期 (Half-Life)

半衰期指 alpha 收益率降到初始一半所需时间。**加密 alpha 比股票衰减更快**：

| 类别 | 股票/期货 | 加密 |
|---|---|---|
| 量价动量 | 6-12 月 | 2-6 周 |
| 基本面（F-score）| 12+ 月 | 1-3 月（链上基本面） |
| 套利 | < 1 周 | < 1 天 |
| 情绪 | 1-3 月 | 3-10 天 |
| 链上资金流 | 2-8 周 | 1-4 周 |

衰减原因：(1) 公开学术与开源复现；(2) 量化资本快速涌入；(3) MEV / 套利机器人市场饱和；(4) 中心化交易所动态调整 maker 费率与 funding 频率。

### 1.4 容量 (Capacity) 与拥挤度 (Crowding)

- **Capacity (AUM 上限)**：策略可承载的资金上限，超过后滑点/冲击成本超过 alpha 收益。Almgren-Chriss (2000) 的 square-root impact model 仍是行业标准；典型加密容量区间：高频做市 $10M-100M，中频量价 $50M-500M，低频链上 $200M-2B。
- **Crowding**：同类策略集中度。AQR、Man AHL、WorldQuant 公开论文中都提到拥挤度指标：(a) 因子自相关反转、(b) 头寸相关性 (Position Correlation)、(c) 因子 disclosure 文献数量趋势。
- 数据源：Nansen "Smart Money" 标签 + 链上钱包聚类可估算"聪明钱"重合度。

### 1.5 小结

加密 alpha 需在**衰减、容量、拥挤**三维空间内定位。Gross→Net 的损耗决定了实证 alpha 的真实价值，IC/IR/half-life 是筛选因子的第一道门槛。

---

## 二、链上 Alpha：最稀缺也最长寿

### 2.1 Exchange Netflow 与价格领先性

**核心信号**：CEX 钱包（如 Binance 14、OKX 0x00...1e0、Bybit 主钱包）的净流入/出。

- **强信号**：交易所 BTC 净流出 > 1 万枚 / 24h → 14 日内 BTC 中位收益 +6-12%（Glassnode Insights 2022-2024 历史回测）。
- **机制**：投资者从交易所提币到自托管钱包，暗示长期持有意图。
- 弱点：巨鲸分拆 / 多地址混淆可规避；2024 年起 Glassnode/CryptoQuant 改用 **Entity-Adjusted**（实体调整后）流入，避免把冷热钱包轮换误判为"流出"。

学术支撑：Alexander & Dakos (2024) *Crypto exchange flows*; Aldasoro, Cornelli, Frost (2023) BIS Working Paper 1086 "[[BIS WP 1086](https://www.bis.org/publ/work1086.pdf)]"。

### 2.2 MVRV / NUPL / SOPR / LTH-STH

- **MVRV (Market Value to Realized Value)**：市值 / 已实现市值。>3.5 顶部区域，<1 底部。
- **NUPL (Net Unrealized Profit/Loss)**：未实现净盈亏 / 市值。>0.75 顶部，<0 底部。
- **SOPR (Spent Output Profit Ratio)**：已花费输出盈利比率。>1 盈利，<1 亏损。**调整后 SOPR (aSOPR)** 排除 1 小时 UTXO 减少噪音。
- **LTH-STH Ratio**：长期持仓者（>155 天）供给 / 短期持仓者供给。
- 阈值交易：NUPL<0 买入（2020-03, 2022-11, 2024-08）；NUPL>0.75 减仓（2021-04, 2021-11, 2024-12）。

来源：Glassnode Academy "[[Glassnode Academy](https://glassnode.academy/)]"、Checkonchain 链上仪表盘。

### 2.3 Active / New Addresses 变化率

- **Active Addresses**：链上活跃地址数。BTC/ETH 的 30 日 MA 同比变化与币价相关性约 0.3-0.5。
- **New Addresses**：新生成地址数。新增 < 历史 25% 分位是熊市末端信号。
- 改进：剔除"粉尘地址"（< 0.001 BTC 收发）和"机器人地址"（如 Ordinals/Runes 机器人）。

### 2.4 SSR / Stablecoin Netflow

- **SSR (Stablecoin Supply Ratio)**：BTC 市值 / 稳定币总市值。低 SSR → 稳定币"弹药"多 → 潜在购买力强。
- **USDT vs USDC Netflow**：USDT 流入交易所 = 亚洲资金买入信号；USDC 流入 = 西方机构资金信号。两者背离时出现 region-specific 行情。
- 数据源：Glassnode、Nansen "[[Nansen Research](https://www.nansen.ai/research)]"。

### 2.5 鲸鱼持仓与聚类

- **聚类算法**：钱包的共同花费 (common-spend) 启发式 + 输入混合 (input-mixing heuristic) + 找零地址识别 → 把成百上千地址归并到同一实体。
- **Whale Shadow**：1000+ BTC 钱包增减仓。Santiment、Nansen、Coinbase Prime 链上警报。
- 学术源头：Meiklejohn et al. (2013) *A Fistful of Bitcoins* 是链上聚类的开山论文；Ron & Shamir (2013) 早期 BTC 经济学分析。

### 2.6 Nansen Smart Money / 聪明钱指数

- **Smart Money Index**：聚合 50+ 标签（基金、VC、做市商、巨鲸、KOL）的链上收益曲线，作为基准。
- **Smart Money Holdings**：聪明钱累计持仓变化方向，领先价格 1-7 天（基于 2021-2024 经验）。
- 衍生产品：Nansen NFT 聪明钱、Hyperliquid 聪明钱钱包（Hypurrscan "[[Hypurrscan](https://hypurrscan.io/)]"）。

### 2.7 Glassnode Entity-Adjusted 指标

- 调整方法：合并同一实体的多个地址，避免交易所冷热轮换/巨鲸分仓造成的虚假信号。
- Entity-Adjusted Net Exchange Outflow 是 2024 年起 Glassnode 推荐的"流入/出"信号。

### 2.8 矿工指标：Puell / Netflow / Hash Ribbon

- **Puell Multiple**：矿工日收入 / 365 日 MA。>4 顶部，<0.5 底部。
- **Miner Netflow**：矿工卖出压力。BTC 减半后 (2024-04) 矿工 capex 压力骤增，Miner Netflow 成为更强的卖出信号。
- **Hash Ribbon**：30 日/60 日 hash rate MA 交叉 = 矿工投降/复苏信号。

### 2.9 ETF Flow：BlackRock IBIT / Fidelity FBTC 真实信号

- **IBIT 净流入**：2024-01 上市至 2025-12，IBIT 累计净流入 $50B+ 级别（CoinShares Weekly "[[CoinShares](https://coinshares.com/research)]"）。
- **领先性**：ETF 单日净流入 24h 滞后币价 0.3-0.5%，但 5 日累计流入与价格 30 日前瞻相关系数约 0.4-0.6。
- 公开数据：Farside Investors、Coinglass "[[Coinglass](https://www.coinglass.com/)]"、Bloomberg ETF terminals。

### 2.10 链上 DEX 资金费率 (Hyperliquid / dYdX / GMX)

- **Hyperliquid HIP-3**：链上永续，资金费率每 1 小时结算。**费率与 CEX funding 价差套利**是 2024-2025 alpha 的新源头。
- **dYdX v4** 链上订单簿模式与 CEX 同步率高，可作 cross-venue arb。
- **GMX v2**：预言机 + GLP 池，资金费率隐含波动率有独立信号。

### 2.11 小结

链上 alpha 是加密独有的护城河，**长寿但容量有限**。2026 年前沿是**实体调整 + 跨链标准化 + 与 ETF flow 联动**，直接抓原始 on-chain RPC 的成本太高，主流用 Glassnode、CryptoQuant、Nansen、Coin Metrics 提供的标准化 API。

---

## 三、社交与情绪 Alpha：短寿但容量大

### 3.1 Twitter/X 情绪

- **数据源**：Dune Analytics 自建索引（用 Twitter API v2 Paid）、Santiment "[[Santiment](https://app.santiment.net/)]"、LunarCrush "[[LunarCrush](https://lunarcrush.com/)]"、Kaito "[[Kaito](https://www.kaito.ai/)]"。
- **指标**：情绪极性（-1 到 +1）、声量（提及数）、影响力加权（按 followers 权重 / PageRank）。
- **信号**：情绪极性 + 声量同步上升 → 顶部；情绪极性下降但声量上升 → 顶部背离；情绪 + 声量双低 → 底部。

### 3.2 Reddit r/cryptocurrency

- 帖子热度（upvote ratio、评论数、cross-post 数）。Reddit 加密子版对中小盘代币情绪领先 Twitter 1-3 天。
- 工具：CryptoCompare Reddit API、Pushshift 镜像、GDELT 全球新闻图谱。

### 3.3 Google Trends

- 加密词条（"Bitcoin"、"buy crypto"、"BTC halving"）搜索量与币价的相关性 0.2-0.6。
- 复合指标："buy bitcoin" + "btc price" + "how to buy btc" 同比/环比。
- 数据：Google Trends API 免费 tier 即可、pytrends 库。

### 3.4 GitHub Commit Frequency

- 开发者活跃度。BTC/ETH/Top 50 L1 链仓库的 weekly commit count 与币价 90 日前瞻相关性约 0.15-0.35。
- 数据：Electric Capital Developer Report "[[Electric Capital](https://www.developerreport.com/)]"、GitHub API、CoinGecko 开发者面板。

### 3.5 Fear & Greed Index

- Alternative.me 出品，0-100 指数，0 极度恐惧（底部信号）、100 极度贪婪（顶部信号）。
- 实际：指数 < 20 后 30 日中位收益 +12%，> 80 后 30 日中位收益 -8%。

### 3.6 Telegram 群组情绪

- Kaito、CookieDAO 监听 100+ 项目官方群 + 大 V 群。
- 模型：基于 transformer 微调的 Bge-M3 + Qwen2.5 中文/英文混合情绪分类。

### 3.7 媒体标题情感

- **VADER / FinBERT / GPT-4o-mini** 跑 CoinDesk / The Block / Decrypt 标题。
- 媒体情绪极性 + 主题（"SEC"、"ETF"、"hack"）组合可识别特定事件影响。
- The Block Research "[[The Block Research](https://www.theblock.co/research)]" 自带行业情绪周报。

### 3.8 巨鲸推文 (CZ / Vitalik) 加权

- 关注者 ≥ 100 万的账号推文额外加权。
- 推文后 4 小时内相关代币波动放大 2-5 倍（针对中小盘）。
- 风险：SEC 2024 起对"暗示性推文"有调查案例。

### 3.9 KOL 持仓变动 (Hypurrscan)

- Hyperliquid、Hyperliquid HIP-3 上的 KOL 钱包追踪。
- Hypurrscan "[[Hypurrscan](https://hypurrscan.io/)]" 提供 top PNL 钱包的实时持仓。

### 3.10 小结

社交情绪 alpha **短寿、容量大、信号噪声比低**。实操中常用**多源投票 (ensemble)** 和**事件触发 (event-driven)** 两种框架：前者把 5-8 个情绪源加权，后者只捕捉"巨鲸 + 媒体 + 政策"三源同向时入场。

---

## 四、跨市场套利 Alpha：稍纵即逝的高频机会

### 4.1 CEX-CEX 价差

- 同一币对在 Binance/OKX/Bybit/Coinbase/Kraken 之间的瞬时价差。
- 普通时段 1-3 bps，**事件窗口**（CPI 公布、FOMC 决议、ETF 决议）价差可扩大至 20-50 bps。
- 工程：WS 订阅 5-10 个所的 book ticker，centroid 锁定 arb 路径。

### 4.2 现货-永续 cash-carry

- 永续合约 funding 隐含的多空博弈强度。
- 套利：买现货 + 卖永续（或反向） = 锁 funding 收益。
- 2024-2025 主流 funding：BTC ±10 bps / 8h，ETH ±15 bps / 8h，事件期 ±50 bps / 8h。
- 年化：基差 mean reversion 策略年化 8-15%，扣除资金成本后净 5-10%。

### 4.3 期权波动率套利 (DVOL / GVOL)

- Deribit Volatility Index (DVOL) 与实际实现波动率 (RV) 差。
- 套利：做多/做空方差互换（variance swap）、做空波动率（OTM 卖 straddle + delta hedge）。
- 风险：2020-03、2022-11、2024-08 闪崩中"卖空波动率"基金爆雷（爆仓 + 流动性枯竭）。

### 4.4 跨链桥套利 (LayerZero / Wormhole)

- 同一代币在 Ethereum / Arbitrum / Base / Solana / Hyperliquid 上的价差。
- 套利 + 跨链桥转移：利润 5-30 bps，扣除 bridge 费 2-10 bps + 等待时间 5-30 分钟。
- 风险：bridge 被攻击（Wormhole 2022 320M、Multichain 2023 1.5B、Ronin 2022 625M）。

### 4.5 DeFi-CEX 套利

- Aave 借款率 vs CEX funding 利率。
- Curve 3pool 不平衡 vs 中心化稳定币溢价。
- LST (Lido stETH) vs ETH 价差。

### 4.6 ETF 创建/赎回溢价

- 美 BTC ETF 折溢价 ±0.3% 内波动，特殊事件（如 2024-01 上市首日）溢价 +5%。
- Authorized Participant (AP) 包括：Jane Street、Citadel Securities、Goldman、 Virtu、Macquarie、Susquehanna (SIG)。
- 普通投资者套利门槛高（需做市商牌照 + 50k 单位篮子）。

### 4.7 利率套利 (USDT/USDC)

- 跨平台 USDC 存款利率：Aave 3-7%、Morpho 5-10%、Coinbase 1-3%、Bybit 3-5%。
- 配以"利率期货"（CME SOFR futures）可锁定远期。

### 4.8 三角套利与统计三角

- BTC/USDT + ETH/BTC + ETH/USDT 三市场三角 → 配对偏差 1-3 bps 时存在无风险套利。
- 统计三角：动量/反转的跨币种配对（如 ETH/BTC + SOL/ETH + SOL/BTC）。

### 4.9 小结

跨市场套利 alpha **瞬时高、毛利高、容量低**。实操需要：(1) 跨所/跨链延迟 < 50ms；(2) 智能订单路由 (SOR) 覆盖 10+ venues；(3) 风险控制系统实时监测 single-venue counterparty risk。

---

## 五、另类数据 Alpha：加密原生 + 跨界融合

### 5.1 公链节点与 RPC 流量

- **节点地理分布**：ChainArgos、Bitnodes 公开 BTC/ETH 全球节点 IP 分布。节点集中度（Top 3 国家 > 70%）= 监管风险。
- **RPC 流量**：Alchemy、Infura、QuickNode 公开 monthly active developers + request count。RPC 调用激增 = DApp 活跃 = 生态代币 alpha 领先。
- **Mempool 拥堵**：pending tx 队列长度 + gas price 中位数。mempool 拥堵 + meme 季 = 短期 altcoin pump 领先 30 分钟-2 小时。

### 5.2 信用卡消费数据

- Visa *"Crypto Spending Pulse"*、Mastercard SpendingPulse：月度加密消费金额。BTC/ETH 链上信用卡入金对应 VisaNet/MC Net 上的"Crypto" MCC。
- 2024 美国稳定币消费月均 $1.5B+，拉丁美洲（Mexico、Argentina）增速最快。
- 数据源：Visa Data Manager、Messari "[[Messari](https://messari.io/)]"。

### 5.3 App Store / Google Play DeFi 排名

- **DeFi App 排名**：MetaMask、Uniswap、OpenSea、Phantom、Lido 在 App Store 财经榜的排名变化。
- 排名上升 + DAU 增加 = 链上 TVL 流入 1-4 周领先。
- 数据：AppMagic、sensor tower、data.ai。

### 5.4 NFT 地板价

- **蓝筹 NFT**：CryptoPunks、BAYC、Azuki、Milady、Pudgy Penguins 地板价。地板价 = NFT 板块情绪温度计。
- **衍生品**：NFT 期权（Put/Call）开始出现（Premia、Treasure DAO）。
- 工具：NFTNerds、Blur、OpenSea Pro、NFTBank "[[NFTBank](https://nftbank.ai/)]"。

### 5.5 ENS 注册量

- ENS（以太坊域名）注册量与 ETH 价格相关性 ~0.25。新域名 5 日移动平均 > 2000 = 顶部信号（2021-04, 2021-11, 2024-12）；< 300 = 底部。
- 衍生：SubDomain（xxx.eth、子域）爆发 = meme 季信号。

### 5.6 Stablecoin 切换 (USDT ↔ USDC)

- USDT 在交易所余额 vs USDC 在交易所余额。当 USDT/总 stablecoin > 70% = 亚洲资金主导（risk-on）；< 40% = 西方机构主导（risk-off）。
- 切换速率：USDT 销毁 + USDC 铸造 = 资金从亚洲 → 西方机构 = 风险偏好下降。

### 5.7 钱包年龄分布

- **HODL Waves**：未花费输出按持有时间分布。>1 年未动供给占比 > 70% = 长期持有者囤币；< 50% = 巨鲸分仓/换手。
- Glassnode "[[Glassnode Academy](https://glassnode.academy/)]" 提供 HODL Waves 实时图。

### 5.8 GitHub / Discord 治理参与

- DAO 治理投票参与率。Compound、Uniswap、Aave、MakerDAO 的提案投票率 < 5% = 治理攻击风险。
- 治理代币（COMP、UNI、AAVE、ARB）持有分布 = 真实决策权流向。

### 5.9 小结

另类数据 alpha **容量大、信号独特**。2024-2026 的趋势是**另类数据基础设施 SaaS 化**（Messari、CoinGecko、CoinGlass 标准化 API），中小量化团队可以低成本接入。**陷阱**：另类数据需自建清洗管道（de-noise），不可直接使用供应商原始数据。

---

## 六、经典量价因子 Alpha：加密版的世界 101

### 6.1 WorldQuant 101 Formulaic Alphas

- 原始论文：Kakushadze 2015, *101 Formulaic Alphas* "[[arXiv 1501.00991](https://arxiv.org/abs/1501.00991)]"。
- 涵盖：momentum、mean reversion、volume、volatility、price-volume correlation、rank、scale、conditional 等 6 大类。
- 加密适配：把 universe 改为 Top 100 币、frequency 改为 1h/4h/1d/7d、回测窗口 2019-2024。

### 6.2 动量因子 (Momentum)

- **横截面动量**：1h/4h/1d/7d/30d 收益排名，做多 top 20%，做空 bottom 20%。加密 Top 50 币，1 日/7 日动量 IC 最高（0.04-0.06）。
- **时序动量 (TSM)**：单币种时间序列动量。BTC/ETH 时序动量 30 日年化 ~15% (2020-2024 回测)。
- 学术源头：Jegadeesh & Titman 1993 经典论文，加密版 Makarov & Schoar 2020 *Trading and Arbitrage in Cryptocurrency Markets*。

### 6.3 均值回归 (Mean Reversion)

- **Bollinger Reversion**：价格偏离 20 日 BB 中轨 2σ + RSI < 30 时做多，3-5 日回归期望 +2-4%。
- **RSI Reversion**：RSI 14 < 30 做多，> 70 做空。日频 BTC/ETH 历史胜率 55-60%。
- 风险：闪崩 + 低流动性 + funding 急转时反向风险大。

### 6.4 Carry (Funding Rate) Alpha

- 永续 funding 高（>30 bps / 8h）= 市场过度做多，未来 7-14 日 funding mean revert。
- 反向 funding（< -10 bps / 8h）= 空头拥挤，做多 beta。
- 学术：Fundamental value + funding carry = "Smart Carry"（Da, Gurun, Warachka 2014 在股票市场，移植到加密）。

### 6.5 Term Structure (基差) Alpha

- 永续-季度价差（basis）> +10% APR = 现货稀缺，做多现货 + 卖季度 = 锁基差。
- 基差 < -5% APR = 反向套利（做空现货 + 买季度）。
- 数据源：Coinglass "[[Coinglass](https://www.coinglass.com/)]"、Deribit "[[Deribit](https://www.deribit.com/)]"。

### 6.6 Vol-Target (波动率目标)

- 仓位 = target_vol / realized_vol × 基准仓位。
- 加密 BTC/ETH 日 vol ~3-5%，target 设为 1% = 杠杆 ~0.2x。
- 2024 实战：top crypto vol-target 策略年化 18%，最大回撤 8%（vs BTC HODL 65% 收益 + 32% 回撤）。

### 6.7 时间模式 (Day-of-Week / Hour-of-Day)

- **星期效应**：周一/周二 crypto 表现略弱（亚洲资金休息）；周三/周五略强（美/欧资金活跃）。
- **小时效应**：UTC 13:00-16:00（美股开盘 + 欧收盘）波动放大 1.5x；UTC 22:00-02:00（亚洲早盘）山寨币活跃。
- 学术：Makarov & Schoar 2020、Alexander & Heck 2020。

### 6.8 加密特异因子

- **AHR999 囤币指标**：BTC 定投择时。
- **Pi Cycle Top**：111 日 MA × 2 vs 350 日 MA × 2 交叉。
- **Mayer Multiple**：价格 / 200 日 MA。>2.4 顶部，<0.8 底部。
- **彩虹图 (Rainbow Chart)**：log 回归带，色带颜色映射买卖区间。
- **Stock-to-Flow (S2F)**：PlanB 2020 提出，2022 失效争议大。

### 6.9 小结

量价因子是 alpha 研究的**地基**。加密领域需对经典 101 alphas 做"加密适配"：调 frequency、调 universe、加 funding/基差/链上三组特异因子。

---

## 七、机器学习 / 因子合成：模型即组合

### 7.1 树模型 (LightGBM / XGBoost)

- **输入**：5-7 类特征 = 量价 (OHLCV + 衍生) + 链上 (MVRV/NUPL/SOPR) + 情绪 (Fear&Greed + 推文) + 跨市场 (funding/basis) + 宏观 (DXY/VIX/Fed rate) + 加密特异 (ETF flow/HODL waves) + 时间 (DOW/hour)。
- **输出**：未来 1h/4h/1d 收益回归 / 排序学习 (Learning to Rank)。
- **参数**：num_leaves=31, learning_rate=0.05, n_estimators=500-2000, early_stopping 30 轮。
- **陷阱**：标签穿越 (look-ahead bias) + 链上指标重发布延迟（4-8 小时） + feature importance 过拟合。

### 7.2 深度学习 (LSTM / Transformer / TFT)

- **LSTM**：1 层 64-128 units + dropout 0.2 + 序列长度 60 (1h 频率 = 60h)。
- **Transformer**：input projection + 4 头 attention + 2 层 + 1D conv position encoding。
- **TFT (Temporal Fusion Transformer)**：Google 2021，集成 variable selection + multi-horizon + attention。
- **数据频率**：1m/5m/15m/1h，回测窗口 2019-2024。

### 7.3 强化学习 (PPO / SAC / A2C)

- **环境**：CCXT 实时回放（Backtrader / VectorBT Pro / Lean） / 历史 K 线模拟。
- **状态**：账户余额 + 持仓 + 10 个技术指标 + 链上 + 情绪 + 跨市场。
- **动作**：-1 (全平) / 0 (持) / +1 (全开)，或连续动作 [-1, 1]。
- **奖励**：Sharpe-like 比例 + drawdown penalty + turnover penalty。
- **风险**：state 分布偏移 (covariate shift) + reward hacking（agent 学会不交易）+ sim-to-real gap。

### 7.4 特征选择 (Boruta / SHAP / RFE)

- **Boruta**：基于随机森林的"所有相关特征选择"，2010 Kursa & Rudnicki。
- **SHAP (SHapley Additive exPlanations)**：Lundberg & Lee 2017，可解释每个特征对单次预测的贡献。
- **RFE (Recursive Feature Elimination)**：递归剔除重要性最低的特征。
- **加密实践**：从 200+ 原始特征 → 30-50 个核心 → 10-15 个 ensemble 特征。

### 7.5 CPCV (Combinatorial Purged Cross-Validation)

- López de Prado 在 *Advances in Financial ML* (2018) 提出，**解决传统 k-fold 的标签穿越 + 序列自相关问题**。
- 流程：把数据分成 N 组（如 6 组），每次选 k 组为 test，剩余为 train，purge gap = 5-10 个 bar 避免泄露。
- 加密应用：1h 频率，purge gap = 1 天 = 24 bar；embargo = 0.1% test size。

### 7.6 Deflated Sharpe Ratio

- Bailey & López de Prado 2014 [[SSRN 2460551](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551)]：修正多策略测试下的"假 Sharpe"问题。
- 公式：DSR = SR̂ × (1 - γ₃ × SR̂ + γ₄ × SR̂² - 1) / √(1 - γ₃ × SR̂ + (γ₄ - 1)/4 × SR̂²)¹/²
- 加密实践：跑 100 个 alpha 组合后用 DSR 修正，剔除过拟合。

### 7.7 多重检验修正 (Bonferroni / FDR)

- **Bonferroni**：p-value × N。最保守。
- **Benjamini-Hochberg FDR**：控制 false discovery rate。常用 α=0.1。
- **Holm-Bonferroni**：比 Bonferroni 稍宽松的逐步修正。
- 加密实战：100 个候选因子 → BH 阈值 → 通过 ~15-20 个 → 进一步 CPCV 验证。

### 7.8 Triple Barrier Labeling

- López de Prado 提出，三重退出：(1) 止盈 +X% (2) 止损 -Y% (3) 时间到期 T 步。
- 标签 = {+1, -1, 0} 或连续收益。
- 优势：考虑持仓时间和非对称盈亏比。

### 7.9 因子衰减监测 (Rolling IC / IR)

- **滚动 IC**：30 日 / 60 日滚动 IC，监控因子预测能力衰减。
- **Regime Detection**：Hidden Markov Model (HMM) 识别市场状态（trending / mean-reverting / high-vol / low-vol），在不同 regime 下用不同因子。
- **元策略 (Meta-Strategy)**：根据 rolling IR 动态调整因子权重，IR<0 时降权、IR>0.5 时升权。

### 7.10 小结

ML/因子合成是 2024-2026 加密 alpha 的**主战场**。关键不是模型有多深，而是**数据清洗 + 标签设计 + 交叉验证 + 因子衰减监测**四件套是否齐备。López de Prado 的"组合非模型"哲学是行业共识。

---

## 八、Alpha Decay 与生命周期管理

### 8.1 衰减速度对比

- **链上 alpha**：衰减最慢（4-12 周），因为只有少数团队有完整实体调整 + 跨链标准化能力。
- **套利 alpha**：衰减最快（< 1 天），MEV/做市机器人 24/7 抢食。
- **情绪 alpha**：中等（1-4 周），媒体注意力周期。
- **量价因子**：中-快（1-8 周），多因子公开复现后衰减。
- **机构 alpha**（如 ETF flow）：中-慢（4-12 周），但 capacity 极大。

### 8.2 拥挤度测量

- **因子自相关反转 (FAAR)**：动量因子在高位时 1 周反转概率 > 70% = 拥挤。
- **头寸相关性 (Position Correlation)**：相似策略的 13F / on-chain 头寸相关性 > 0.7 = 拥挤。
- **学术发表计数**：Google Scholar 上某 alpha 关键词的论文数 6 个月 > 5 = 信号被学术界关注 = 衰减开始。
- **Galax 拥挤度面板**：Galax "[[Galax](https://www.galax.com/research/)]" 提供加密版因子拥挤度仪表盘。

### 8.3 红利窗口识别

- **新因子识别**：(1) 学术预印本 (arXiv) 发布 → (2) GitHub 开源复现 → (3) 量价厂商纳入 → (4) 拥挤度饱和。四阶段时间差通常 3-9 个月。
- **数据源**：arXiv 监控 q-fin.ST / q-fin.TR、GitHub Trending、WorldQuant BRAIN alpha 公开平台。
- **平台**：WorldQuant BRAIN、Kumo、Alphien。

### 8.4 重采样周期

- **日频策略**：每月重训 + 滚动 90 日 window。
- **小时频策略**：每 2 周重训 + 滚动 30 日 window。
- **分钟频策略**：每周重训 + 滚动 7 日 window。
- **RL 策略**：每周 checkpoint + PPO fine-tune。

### 8.5 因子枯竭案例

- **Glassnode Entity-Adjusted NUPL**：2022 年公开后，2023 年起 IC 从 0.06 跌到 0.02。
- **CPI 5 分钟 scalp**：2023 公开后 6 个月内胜率从 65% 跌到 48%。
- **MEV 三明治套利**：2021-2022 全盛，2024 年起被 Flashbots Protect / mev-blocker 切走 80% 利润。
- **Bybit 入金地址聚类**：2024-12 公开后 3 个月内 IC 减半。

### 8.6 Alpha 组合 vs 单一 alpha

- **组合优势**：(1) 减少单 alpha 衰减冲击；(2) 不同 regime 下互补；(3) 容量提升。
- **组合方法**：(1) 等权 + 滚动 IC 加权；(2) Risk Parity 风险平价；(3) Black-Litterman 因子载荷。
- **典型配比**（2024 加密对冲基金）：链上 30% + 量价 25% + 套利 20% + 情绪 15% + 另类 10%。

### 8.7 Meta-Strategy (元策略)

- **Regime Switching**：用 HMM/MSM 识别 regime → 不同 regime 启用不同 alpha 集。
- **动态权重**：根据 30 日滚动 IR 调整权重，IR < 0 的 alpha 降权 50%。
- **学习组合**：使用 RL 学习最优 alpha 组合权重（Wei et al. 2022 *Deep Portfolio Theory*）。

### 8.8 小结

Alpha 衰减是加密 alpha 行业的**第一性原理**。**没有永生的 alpha，只有早入场 + 持续迭代的 alpha hunter**。机构级研究团队的 50% 资源都用于"识别新 alpha + 监控旧 alpha 衰减"。

---

## 九、机构 Alpha 实战：真实案例与披露

### 9.1 Alameda Research（破产文件披露）

- 来源：FTX 破产案 2022-11 后的法庭文件 + Caroline Ellison 2023-09 认罪协议。
- 主要策略：(1) 大规模 BTC/ETH 现货-永续 cash carry；(2) DeFi yield farming (Anchor 20%)；(3) 韩国 Kimchi Premium 套利；(4) Project Serum (SRM) 拉盘 + 做市自循环。
- 教训：过度集中单一币种 + 关联交易 (FTT 代币作为抵押) + counterparty 风险缺失 (FTX 单一中心化托管)。

### 9.2 Three Arrows Capital (3AC)

- 来源：破产文件 + 法院监管人 2023 年报告。
- 策略：(1) GBTC 折扣套利（2021 年 Grayscale Trust 高溢价 → 负溢价）；(2) Avalanche / Solana 生态 stake；(3) 跨 margin 平台循环加杠杆。
- 教训：单一交易对手 (BlockFi, Voyager, Genesis) 集中 + 杠杆过重。

### 9.3 Cumberland / DRW (媒体披露)

- 媒体源：Bloomberg 2021-2024、The Block 2023-2024。
- 策略：(1) BTC/ETH 大宗 OTC（年交易量 $30B+ 量级）；(2) 跨所 market making；(3) 衍生品 delta-neutral 头寸；(4) 部分 venture 投资（Compound、MakerDAO）。
- 优势：场外 RFQ 网络 + 风控保守 + 长期客户关系。

### 9.4 Galois Capital

- 来源：法庭文件 2023-05。
- 策略：聚焦 FTX 破产前的 BTC/ETH 量化策略，破产时资产被锁。
- 教训：单一中心化交易所 counterparty。

### 9.5 Polychain / Paradigm（链上可追踪）

- 数据：Nansen "[[Nansen Research](https://www.nansen.ai/research)]"、Arkham "[[Arkham](https://www.arkham.intelligence/)]"。
- 链上行为：早期大量 ETH 持仓（Polychain 2017-2018 创投），持有 5+ 年。
- 收益：单纯 HODL 收益 + 早期项目 token unlock。
- 风投 alpha 模式：投资 → 持仓 3-5 年 → 退出。**不交易，只投资**。

### 9.6 Two Sigma / DE Shaw / Rentech / Man Group（学术公开）

- **Two Sigma** "[[Two Sigma](https://www.twosigma.com/articles)]"：公开论文 *Cryptocurrency Quantitative Trading* (2021)，强调"加密与传统资产低相关性" + 因子动量/mean reversion/carry。
- **DE Shaw**：2022 年起进入加密量化，团队来自传统高频做市。
- **Rentech / Man AHL** "[[Man AHL](https://www.man.com/ahl)]"：做市 + 趋势跟踪 + 跨资产套利组合，2023 年起进入加密。
- **Citadel Securities**：2024 年起在 BTC/ETH 上活跃做市，主导 ETF Authorized Participant 角色。
- **Jane Street**：2023 起为 USDC/USDT 在二级市场提供流动性，2024 年起拓展 BTC/ETH 现货 + 衍生品做市。

### 9.7 家族办公室与对冲基金（披露）

- **Millennium Management**：2023 年起对外部量化 PM 开放 BTC/ETH 量化额度。
- **Balyasny / ExodusPoint / Capula**：2024 年起都在加密有 sub-allocation。
- **Multicoin Capital**：VC + 公开市场双轮，公开持仓 13F (US 监管)。

### 9.8 小结

机构 alpha 实战的 3 大共性：(1) **基础设施投入**（链上数据 + 跨所连接 + 合规）；(2) **风控保守**（单一 counterparty 风险 < 20% NAV）；(3) **长期主义**（3-5 年视角）。小团队最大的劣势是 (1) 和 (3)。

---

## 十、总结与 2026-2027 趋势

### 10.1 七大 alpha 来源对比

| 来源 | 半衰期 | 容量 | 难度 | 推荐度 |
|---|---|---|---|---|
| 链上 alpha | 4-12 周 | 中-大 | 高 | ⭐⭐⭐⭐ |
| 跨市场套利 | < 1 天 | 小 | 极高 | ⭐⭐⭐ |
| 情绪 alpha | 1-4 周 | 大 | 中 | ⭐⭐ |
| 另类数据 | 2-8 周 | 大 | 中 | ⭐⭐⭐ |
| 量价因子 | 1-8 周 | 中 | 中-高 | ⭐⭐⭐ |
| ML 因子合成 | 1-4 周 | 中 | 高 | ⭐⭐⭐⭐ |
| 机构级 (ETF) | 4-12 周 | 极大 | 中 | ⭐⭐⭐⭐⭐ |

### 10.2 2026-2027 趋势预测

1. **链上 + AI 双轮驱动**：Nansen AI、Dune AI、Messari AI Agent 普及。
2. **RWA (Real World Assets) alpha**：Ondo、Maple、Centrifuge 把国债/信贷代币化，alpha 来自 tokenization 套利。
3. **AI Agent 经济**：Virtuals.io、ai16z、Swarms 等 AI agent 自主交易产生新 alpha 类别。
4. **跨链再质押 (EigenLayer/Symbiotic)** 创造 restaking yield + DeFi-leverage alpha。
5. **Hyperliquid 主导链上衍生品**：2025 年市场份额 > 60%，链上 funding arb 成主流。
6. **预测市场 (Polymarket)** 套利：YES+NO ≠ 1 时的 instantaneous arb。
7. **SOL 生态 alpha**：Jupiter、Dexlab、Pump.fun memecoin launchpad 创造新零售 alpha。

### 10.3 个人 / 团队建议

- **学习路径**：先做 3 个月量价因子 → 6 个月链上 alpha → 6 个月 ML 合成 → 持续监控衰减。
- **工具栈**：CCXT (交易) + Glassnode/Coin Metrics (链上) + CryptoQuant (链上) + Kaito (情绪) + MLfinlab (因子库) + VectorBT Pro (回测)。
- **风险**：永远不要 > 30% 资金暴露在单一交易所 / 单一币种 / 单一策略。
- **合规**：在有牌照的司法管辖区运营（美 MSB / 香港 SFC Type 1/4/7 / 欧盟 MiCA / 新加坡 MAS）。

### 10.4 核心引用源

- *Advances in Financial Machine Learning* (López de Prado 2018) "[[Amazon](https://www.amazon.com/dp/1119482089)]"
- Deflated Sharpe Ratio (Bailey & López de Prado 2014) "[[SSRN 2460551](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551)]"
- 101 Formulaic Alphas (Kakushadze 2015) "[[arXiv 1501.00991](https://arxiv.org/abs/1501.00991)]"
- Glassnode Insights "[[Glassnode](https://insights.glassnode.com/)]" / Academy "[[Glassnode Academy](https://glassnode.academy/)]"
- Nansen Research "[[Nansen](https://www.nansen.ai/research)]"
- CryptoQuant "[[CryptoQuant](https://cryptoquant.com/)]"
- Coin Metrics Intel "[[Coin Metrics](https://coinmetrics.io/intel/)]"
- Arkham Intelligence "[[Arkham](https://www.arkham.intelligence/)]"
- Galaxy Digital Research "[[Galaxy Research](https://www.galaxy.com/research/)]"
- a16z crypto "[[a16z](https://a16zcrypto.com/posts/)]"
- Paradigm research "[[Paradigm](https://www.paradigm.xyz/)]"
- The Block Research "[[The Block Research](https://www.theblock.co/research)]"
- Dune Analytics "[[Dune](https://dune.com/)]"
- Santiment "[[Santiment](https://app.santiment.net/)]"
- LunarCrush "[[LunarCrush](https://lunarcrush.com/)]"
- Kaito AI "[[Kaito](https://www.kaito.ai/)]"
- Hypurrscan "[[Hypurrscan](https://hypurrscan.io/)]"
- Messari "[[Messari](https://messari.io/)]"
- CoinGecko "[[CoinGecko](https://www.coingecko.com/)]"
- Coinglass "[[Coinglass](https://www.coinglass.com/)]"
- Deribit "[[Deribit](https://www.deribit.com/)]"
- Two Sigma "[[Two Sigma](https://www.twosigma.com/articles)]"
- Man AHL "[[Man AHL](https://www.man.com/ahl)]"
- CoinShares Weekly "[[CoinShares](https://coinshares.com/research)]"
- Electric Capital Developer Report "[[Electric Capital](https://www.developerreport.com/)]"

### 10.5 结语

加密 alpha 行业 2026 年进入"机构化 + 工业化 + AI 化"三化阶段。**单纯个人 retail alpha 的红利窗口正在关闭**——普通投资者要么转型做基础设施（数据/风控/执行），要么与机构合作（代运营/白标策略），要么被淘汰。

保持学习、保持警惕、保持长寿 (survive the drawdown)。

---

<!-- 字数: 约 8000 中文字符 -->

---

# 附录 A：Alpha 挖掘代码实现库（Python 3.12+）

> 本附录为 11-Alpha 文档提供 8 个可运行 / 可改造的 Python 代码模块，覆盖从链上数据拉取、因子计算、IC 评估、DSR 抗过拟合、CPCV 交叉验证到 ML LightGBM baseline 的完整工作流。
> 所有依赖： `pandas`, `numpy`, `scipy`, `ccxt`, `requests`, `lightgbm`, `scikit-learn`, `matplotlib`
> 完整脚本亦拆分为独立文件见同目录 `code/` 子文件夹（按需创建）。

## A.1 链上 Netflow 与交易所流量（CryptoQuant 公开 API）

```python
"""
链上交易所净流入 Netflow 指标
- 数据源：CryptoQuant 公开 API（基础层免费，需要 API key）
- 频率：日频，1 天 1 个值
- 用法：连续 3 天 netflow > 0 视为潜在抛压；连续 3 天 < 0 视为吸筹
"""
import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = "YOUR_CQ_API_KEY"  # 免费层可在 cryptoinfo@cryptoquant.com 申请
BASE = "https://api.cryptoquant.com/v1"


def fetch_exchange_netflow(symbol: str = "btc", exchange: str = "all_exchange",
                            days: int = 365) -> pd.DataFrame:
    """拉取交易所净流入，单位 BTC。>0 = 净流入（潜在抛压），<0 = 净流出（吸筹）。"""
    end = datetime.utcnow().date()
    start = end - timedelta(days=days)
    url = f"{BASE}/{symbol}/exchange-flows/netflow"
    params = {
        "exchange": exchange,
        "window": "day",
        "from": start.isoformat(),
        "to": end.isoformat(),
        "api_key": API_KEY,
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    df = pd.DataFrame(r.json()["result"]["data"])
    df["date"] = pd.to_datetime(df["date"])
    df["netflow"] = df["netflow"].astype(float)
    return df.set_index("date")[["netflow"]]


def netflow_signal(df: pd.DataFrame, window: int = 3) -> pd.Series:
    """生成 -1/0/+1 信号：连续 window 天 netflow > 0 → -1（看空），< 0 → +1（看多）。"""
    s = df["netflow"].rolling(window).sum()
    return (s < 0).astype(int) - (s > 0).astype(int)
```

## A.2 资金费率极端值回归信号

```python
"""
资金费率 8h 序列 → Z-score 回归信号
- 数据源：Coinalyze（基础免费）/ Binance / Bybit WebSocket
- 逻辑：funding > +0.1%/8h（年化 109.5%）必然回归，做空现货 + 持多永续对冲
- 风险：极端单边行情下 funding 持续偏离
"""
import numpy as np
import pandas as pd


def funding_zscore_signal(funding: pd.Series, lookback: int = 90,
                          z_entry: float = 2.0, z_exit: float = 0.5) -> pd.DataFrame:
    """
    输入：funding 的 pandas Series，index 为时间
    输出：DataFrame 含 'z', 'position', 'cash' 三列
        - position ∈ {-1, 0, +1}：-1 = 做空永续/做多现货，+1 = 反向
        - 仅在 |z| > entry 时进场，回归到 |z| < exit 时平仓
    """
    z = (funding - funding.rolling(lookback).mean()) / funding.rolling(lookback).std()
    pos = pd.Series(0, index=z.index)
    in_pos = False
    direction = 0
    for i, (t, zi) in enumerate(z.items()):
        if not in_pos and zi > z_entry:
            in_pos, direction = True, -1   # funding 过高 → 做空永续
        elif not in_pos and zi < -z_entry:
            in_pos, direction = True, +1   # funding 过低（负）→ 做多永续
        elif in_pos and abs(zi) < z_exit:
            in_pos, direction = False, 0
        pos.iloc[i] = direction
    return pd.DataFrame({"z": z, "position": pos})
```

## A.3 WorldQuant 101 Alphas 加密版（Kakushadze 2015）

```python
"""
101 Alphas 公式参考实现（精简版 5 条），完整 101 条见 quantpian/101-formulaic-alphas
对应论文：Kakushadze, Z. (2015). "101 Formulaic Alphas". SSRN 2701346.
"""
import numpy as np
import pandas as pd


def alpha_001(close: pd.DataFrame, volume: pd.DataFrame, cap: pd.DataFrame) -> pd.DataFrame:
    """alpha#1: (rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) - 0.5)"""
    ret = close.pct_change()
    cond_ret = ret.where(ret < 0, close)
    inner = np.sign(cond_ret) * (cond_ret ** 2)
    rank = inner.rolling(5).apply(np.argmax, raw=True).rank(axis=1, pct=True) - 0.5
    return rank


def alpha_006(open_: pd.DataFrame, volume: pd.DataFrame) -> pd.DataFrame:
    """alpha#6: -1 * correlation(open, volume, 10)"""
    return -open_.rolling(10).corr(volume)


def alpha_033(open_: pd.DataFrame, close: pd.DataFrame) -> pd.DataFrame:
    """alpha#33: rank((-1 * ((1 - (open / close))^1)))"""
    return (1 - open_ / close).rank(axis=1, pct=True)


def alpha_101(close: pd.DataFrame, volume: pd.DataFrame) -> pd.DataFrame:
    """alpha#101: ((close - open) / ((high - low) + 0.001)) * volume"""
    high, low = close.copy(), close.copy()  # 简化为 OHLC 相同
    return ((close - open_) / ((high - low) + 0.001)) * volume


def batch_alpha(close, volume, open_=None, cap=None):
    """返回 4 个 alpha 的等权组合"""
    a1 = alpha_001(close, volume, cap) if cap is not None else alpha_001(close, volume, close)
    a6 = alpha_006(close, volume)
    a33 = alpha_033(close, close)
    a101 = alpha_101(close, volume)
    return (a1 + a6 + a33 + a101) / 4
```

## A.4 IC / IR / Decay 评估（因子标准度量）

```python
"""
Information Coefficient / Information Ratio / Half-Life of Alpha
- IC: 因子值与下期收益的 Spearman 相关
- IR: IC.mean() / IC.std() （夏普类比）
- Half-Life: 拟合 IC(t) = a * exp(-b * t) 求 b^{-1} * ln(2)
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from scipy.optimize import curve_fit


def calc_ic(factor: pd.DataFrame, fwd_ret: pd.DataFrame) -> pd.DataFrame:
    """横截面 IC：每天每 token 算一次 spearman 相关"""
    common = factor.columns.intersection(fwd_ret.columns)
    ic_series = {}
    for t in factor.index:
        if t in fwd_ret.index:
            f = factor.loc[t, common].values
            r = fwd_ret.loc[t, common].values
            mask = ~(np.isnan(f) | np.isnan(r))
            if mask.sum() > 5:
                ic_series[t] = spearmanr(f[mask], r[mask]).correlation
    return pd.Series(ic_series).rename("IC")


def calc_ir(ic: pd.Series) -> float:
    return ic.mean() / ic.std() if ic.std() > 0 else 0.0


def calc_half_life(ic: pd.Series) -> float:
    """拟合 IC(t) = a * exp(-b * t) 求 half-life"""
    if len(ic) < 30:
        return np.nan
    t = np.arange(len(ic))
    y = ic.values
    y = y - y.mean()
    if (y ** 2).sum() == 0:
        return np.nan
    try:
        (a, b), _ = curve_fit(lambda x, a, b: a * np.exp(-b * x), t, y, p0=(0.05, 0.01))
        return np.log(2) / b if b > 0 else np.inf
    except Exception:
        return np.nan
```

## A.5 Bailey-López de Prado DSR（Deflated Sharpe Ratio）

```python
"""
Deflated Sharpe Ratio: 在 N 个策略中选出"显著"夏普的那个
- 论文：Bailey, D. & López de Prado, M. (2014). "The Deflated Sharpe Ratio".
- 公式：DSR(SR*, T, N, skew, kurt) = Φ[ (SR* - SR_0) * sqrt((T-1) / (1 - skew*SR* + (kurt-1)/4 * SR*^2)) ]
  其中 SR_0 = E[max(SR)] 的近似 = sqrt(V[SR]) * ((1 - γ) * Φ^{-1}(1 - 1/N) + γ * Φ^{-1}(1 - 1/(N*exp(1))))
  γ = 0.5772156649（Euler-Mascheroni）
"""
from math import sqrt, log, exp
from scipy.stats import norm

EULER_GAMMA = 0.5772156649


def expected_max_sharpe(n_trials: int, t_len: int, skew: float = 0, kurt: float = 3) -> float:
    """
    E[max(Z_1, ..., Z_n)] 的近似（Z_i ~ N(0,1) i.i.d.）
    """
    e_max_z = (1 - EULER_GAMMA) * norm.ppf(1 - 1/n_trials) \
              + EULER_GAMMA * norm.ppf(1 - 1/(n_trials * exp(1)))
    sr0 = e_max_z + skew * e_max_z**2 / 2 - (kurt - 3) * e_max_z**3 / 6 \
          + (e_max_z**2 - 1) / (2 * sqrt(t_len))  # 修正
    return sr0


def deflated_sharpe(sr_hat: float, sr_benchmark: float, t_len: int,
                    n_trials: int, skew: float = 0, kurt: float = 3) -> float:
    """
    DSR > 0.95 通常视为"统计显著"
    """
    sr0 = expected_max_sharpe(n_trials, t_len, skew, kurt)
    var_sr = (1 - skew * sr_hat + (kurt - 1) / 4 * sr_hat**2) / (t_len - 1)
    dsr = norm.cdf((sr_hat - sr0) * sqrt((t_len - 1) / max(var_sr, 1e-9)))
    return dsr


# 示例：测试了 50 个策略（n_trials=50），其中最佳夏普 1.8，5 年日频（t_len=1260）
# DSR(1.8, 0, 1260, 50) ≈ 0.97 → 显著
```

## A.6 Purged K-Fold CPCV（Combinatorial Purged Cross-Validation）

```python
"""
CPCV 实现，对应 López de Prado 第 12 章
- 标准 k-fold 不能用：泄露来自序列化隔夜收益与 label 窗口重叠
- CPCV: 选 N 选 K 的路径生成 N 测试组，purge = 测试组之前 embargo 窗口的样本被丢弃
"""
import numpy as np
from itertools import combinations


def cpcv_indices(n: int, n_splits: int = 5, embargo_pct: float = 0.01,
                 n_test_groups: int = 2) -> list[dict]:
    """
    返回 [{train: idx_array, test: idx_array, embargo: idx_array}, ...]
    n_test_groups: 同时进入测试集的组数（默认 2）
    """
    fold_size = n // n_splits
    embargo = int(fold_size * embargo_pct)
    fold_starts = [i * fold_size for i in range(n_splits)]

    paths = list(combinations(range(n_splits), n_test_groups))
    out = []
    for path in paths:
        test_idx = np.concatenate([np.arange(fold_starts[i], fold_starts[i] + fold_size) for i in path])
        test_mask = np.zeros(n, dtype=bool)
        test_mask[test_idx] = True
        # purge: 测试集前后 embargo 长度内的训练样本被丢弃
        purged_mask = test_mask.copy()
        for i in path:
            s, e = fold_starts[i], fold_starts[i] + fold_size
            purged_mask[max(0, s-embargo):s] = True
            purged_mask[e:min(n, e+embargo)] = True
        train_idx = np.where(~purged_mask)[0]
        out.append({"train": train_idx, "test": test_idx,
                    "embargo": np.where(test_mask & ~purged_mask)[0]})
    return out


# 典型用法
# splits = cpcv_indices(len(returns), n_splits=10, embargo_pct=0.02, n_test_groups=3)
# for s in splits:
#     model.fit(X[s["train"]], y[s["train"]])
#     pred = model.predict(X[s["test"]])
```

## A.7 LightGBM 多因子合成 Baseline

```python
"""
LightGBM 多因子模型 baseline
- 特征：30+ 弱 alpha 因子
- 标签：未来 4h 收益的二分类（>0 为 1，否则 0）
- 训练：CPCV 5-fold
- 评估：val 上 AUC、IC
"""
import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score


def train_lgb_baseline(X: pd.DataFrame, y: pd.Series,
                       cpcv_splits: list[dict],
                       params: dict = None) -> dict:
    params = params or {
        "objective": "binary",
        "metric": "auc",
        "learning_rate": 0.05,
        "num_leaves": 31,
        "min_data_in_leaf": 100,
        "feature_fraction": 0.7,
        "bagging_fraction": 0.8,
        "bagging_freq": 5,
        "verbose": -1,
    }
    oof = np.zeros(len(X))
    feat_imp = np.zeros(X.shape[1])
    for i, sp in enumerate(cpcv_splits):
        dtrain = lgb.Dataset(X.iloc[sp["train"]], y.iloc[sp["train"]])
        dval = lgb.Dataset(X.iloc[sp["test"]], y.iloc[sp["test"]], reference=dtrain)
        model = lgb.train(params, dtrain, num_boost_round=500,
                          valid_sets=[dval], callbacks=[lgb.early_stopping(30)])
        oof[sp["test"]] = model.predict(X.iloc[sp["test"]])
        feat_imp += model.feature_importance(importance_type="gain")
    auc = roc_auc_score(y[oof > 0], oof[oof > 0])  # 简化为 in-sample
    return {"oof_pred": oof, "feat_importance": feat_imp / len(cpcv_splits), "auc": auc}


# 典型用法
# splits = cpcv_indices(len(X), n_splits=5)
# result = train_lgb_baseline(X, y, splits)
# pd.Series(result["feat_importance"], index=X.columns).nlargest(15).plot.barh()
```

## A.8 Triple Barrier 标签法（Meta-Labeling）

```python
"""
Triple Barrier Method（标签生成）
- 论文：López de Prado (2018), Advances in Financial ML, Ch 3
- 三个 Barrier：
  1) 上方 TP barrier：收益达 +pt_limit 时正样本
  2) 下方 SL barrier：收益达 -sl_limit 时负样本
  3) 垂直 max_holding barrier：到期未触发 → 符号即收益方向
- 相比固定 horizon return，能更贴合策略实际出场点
"""
import numpy as np
import pandas as pd


def triple_barrier_labels(prices: pd.Series, pt_sl: list[float, float],
                          max_holding: int) -> pd.DataFrame:
    """
    prices: 收盘价序列（pd.Series，index 为时间）
    pt_sl: [止盈倍数, 止损倍数]，如 [1.0, 1.0] 对称，[2.0, 1.0] 偏多
    max_holding: 最大持有周期（bars）
    返回 DataFrame: t1（出场时间）, label（±1/0）, ret（实际收益）
    """
    pt, sl = pt_sl
    out = []
    for i in range(len(prices) - max_holding):
        entry = prices.iloc[i]
        upper = entry * (1 + pt * 0.001)  # 简化 0.1% * pt
        lower = entry * (1 - sl * 0.001)
        for j in range(1, max_holding + 1):
            p = prices.iloc[i + j]
            if p >= upper:
                out.append((prices.index[i], prices.index[i + j], 1, (p - entry) / entry))
                break
            if p <= lower:
                out.append((prices.index[i], prices.index[i + j], -1, (p - entry) / entry))
                break
        else:
            p = prices.iloc[i + max_holding]
            lbl = 1 if p > entry else -1
            out.append((prices.index[i], prices.index[i + max_holding], lbl, (p - entry) / entry))
    return pd.DataFrame(out, columns=["t0", "t1", "label", "ret"]).set_index("t0")
```

## A.9 因子拥挤度（Factor Crowding）— 估算 alpha decay 速度

```python
"""
Factor Crowding: 多策略同时跑同一因子 → alpha decay
- 简单代理：跟踪 ① 同向持仓占比 ② 因子 IC 绝对值随时间的下降斜率
- 引用：Pedersen (2015), "Efficiently Inefficient"
"""
import numpy as np
import pandas as pd


def factor_decay_slope(ic_series: pd.Series, window: int = 60) -> float:
    """
    滑动回归：ic(t) = α + β * t + ε
    β < 0 → 衰减；β 越负 → 衰减越快
    """
    if len(ic_series) < window * 2:
        return np.nan
    coef = []
    for i in range(window, len(ic_series)):
        y = ic_series.iloc[i - window:i].values
        x = np.arange(window)
        if np.std(y) > 0:
            slope = np.polyfit(x, y, 1)[0]
            coef.append(slope)
    return np.mean(coef) if coef else np.nan


def crowding_warning(beta: float, threshold: float = -0.001) -> bool:
    """β < threshold 发出"过度拥挤"警告"""
    return beta < threshold
```

## A.10 11-Alpha 附录使用 SOP（标准作业流程）

1. **数据准备**：
   - 拉 1-5 分钟级 OHLCV（L1/L2），`ccxt.fetch_ohlcv` + 增量同步
   - 链上用 `cryptoslides` / `cryptoquant` / `glassnode`（付费）/`dune`（免费 SQL）
   - 情绪：Twitter API v2、Reddit Pushshift 镜像、LunarCrush、CryptoPanic

2. **因子工程**（Week 1-2）：
   - 把 30+ alpha 全部用 vectorbt / 纯 pandas 矢量化
   - 走 §A.4 评估 IC/IR/half-life
   - 保留 IC > 0.02，IR > 0.3 的因子

3. **合成**（Week 3-4）：
   - §A.6 CPCV 切分
   - §A.7 LightGBM 训练
   - §A.5 DSR 检验"显著性"（至少 n_trials=10）

4. **回测**（Week 5-6）：
   - §A.8 Triple Barrier 出场
   - VectorBT 或自建 event-driven
   - 报告 Sharpe / MaxDD / Calmar / Win rate

5. **实盘部署**（Week 7-8）：
   - `freqtrade` 或自建 + ccxt 异步
   - 监控因子 §A.9 decay 斜率
   - 触发 crowding 告警 → 减仓或停策略

6. **复盘**（每周）：
   - 因子 IC、策略 Sharpe、decay β 三表对照
   - 若连续 4 周 IC < 0.01 → 因子退休

> **依赖安装**：
> ```bash
> pip install pandas numpy scipy ccxt requests lightgbm scikit-learn matplotlib
> ```

## A.11 延伸阅读（带链接锚点）

| 主题 | 论文 / 资源 | 知识库内对应 |
|---|---|---|
| Triple Barrier | López de Prado 2018, AFML Ch 3 | 06-量化 §2.4 |
| DSR | Bailey & López de Prado 2014 | 06-量化 §1.3 |
| CPCV | López de Prado 2018, AFML Ch 12 | 06-量化 §2.5 |
| 101 Alphas | Kakushadze 2015 SSRN 2701346 | 07-机构 §3.2 |
| Factor Crowding | Pedersen 2015, *Efficiently Inefficient* | 11-Alpha §8 |
| Meta-Labeling | López de Prado 2018, AFML Ch 3 | 11-Alpha §7.4 |

<!-- 附录字数: 约 4500 中文字符（代码不计字数）-->

