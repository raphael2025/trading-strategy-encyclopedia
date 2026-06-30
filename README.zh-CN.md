<div align="center">

# 交易策略，实测过的

### 全网唯一一个告诉你**哪个策略真能用**的交易百科——附证据。

**[English](README.md) · [中文](README.zh-CN.md) · [Русский](README.ru.md)**

</div>

---

每一个交易策略、指标、图表形态——先讲清楚,再**严格实测**,然后给一个判决。

网上的交易"知识"大多只告诉你一个策略**怎么用**,几乎没人告诉你它**到底有没有用**。这个仓库告诉你。每一条都跑过**无未来函数回测** + 一整套**反过拟合检验**(安慰剂检验、Deflated Sharpe、PBO、样本外),并打上一个诚实的判决标签。

> **我们反复发现的难堪真相:一旦算上成本、未来函数泄露、以及"你其实试了200个"这件事,绝大多数流行策略都活不下来。** 不管结论如何,我们把证据摆给你看。


## 🔬 深入一层 —— 判决背后的证据

本仓库现已并入三块配套内容：

- **[`machine-validated/`](machine-validated/)** —— 每条判决都附**可复现**的完整反过拟合检验（Deflated Sharpe、PBO/CSCV、walk-forward、block bootstrap）：原始 [verdict 数据](machine-validated/results/)、逐策略[报告](machine-validated/reports/)、[实盘 PLAYBOOK](machine-validated/PLAYBOOK.md)、[验证代码](machine-validated/experiments/)。*诚实的结论：16 个机器验证策略里，只有 1 个通过了全部关卡。*
- **[`knowledge-base/`](knowledge-base/)** —— 加密永续合约交易全知识体系（技术分析 / 风控 / 市场机制 / 期权 / 链上 / 订单簿 / Alpha 挖掘），判决之下的参考层。

> 它们一起回答的不只是"策略 X 有没有用"，而是"什么能扛过诚实的验证，以及你怎么自己搭这套验证关卡"。

## 判决体系

| 标签 | 含义 |
|---|---|
| ✅ **已验证** | 扛过样本外 + Deflated Sharpe + 成本。一个真实的(通常很小的)边。 |
| ❌ **已证伪** | 朴素回测里好看;一过安慰剂/样本外/成本/多重检验就死。 |
| 🔶 **有条件** | 真,但只在特定条件下(如仅 maker、特定行情)——不适合普通散户吃单。 |
| ⚠️ **未测** | 为完整性收录;我们还没跑(欢迎 PR)。 |

我们怎么测、你怎么复现:**[方法论 METHODOLOGY](METHODOLOGY.md)**。验证工具已开源:**[`deflate`](https://github.com/raphael2025/deflate)**——把它对准你自己策略的收益,看看你是不是在自欺。

## 从这里开始

➡️ **[判决索引——所有策略一览](docs/zh/00-verdict-index.md)**——直接看答案。

## 目录

- **[01 · 技术指标](docs/zh/01-technical-indicators/)** —— RSI、MACD、布林带、均线,25+ 指标
- **[02 · 图表形态](docs/zh/02-chart-patterns/)** —— 头肩、三角、谐波、K线形态
- **[03 · 策略](docs/zh/03-strategies/)** —— 趋势跟随、均值回复、动量、突破、网格、跟单
- **[04 · 市场微观结构](docs/zh/04-microstructure/)** —— 订单流、OFI/VPIN、流动性、spoofing
- **[05 · 交易心理学](docs/zh/05-psychology/)** —— 认知偏差、恐惧贪婪、纪律体系
- **[06 · 风险管理](docs/zh/06-risk-management/)** —— 仓位、波动目标、杠杆、回撤控制
- **[07 · 市场机制](docs/zh/07-market-mechanics/)** —— 流动性猎杀、操纵、止损猎杀
- **[08 · 加密专属](docs/zh/08-crypto-specific/)** —— 资金费率、基差/carry、永续、清算

## 凭什么信它?

因为我们**公开自己的失败**。我们对加密策略做了一次大规模搜索,而我们测过的大部分——预测信号、跟单聪明钱、技术指标、散户订单流——**都没通过诚实的验证**。我们用数字说出来。一个只给你看赢家的来源,是在向你推销东西。([读读理念 →](METHODOLOGY.md#why-most-backtests-lie))

## 获取实时判决与告警

我们在社区里发布**客观市场数据**(资金费/carry 机会、趋势 regime 翻转、清算事件)——**是事实,不是涨跌预测**:

📲 **Telegram:[t.me/+E3UdPtwlISVhZDc1](https://t.me/+E3UdPtwlISVhZDc1)**  ·  🧪 **验证工具:[`deflate`](https://github.com/raphael2025/deflate)**

## 贡献

发现我们漏了的策略?发 PR。但本仓库的铁律:**结论必须有证据。** 一个策略在跑过整套检验之前,只能是 `⚠️ 未测`,不是 `✅`。见 [CONTRIBUTING](CONTRIBUTING.md)。

## 免责声明

仅为教育与研究内容,均非投资建议。"已验证"意思是*在历史数据上扛过了我们的检验*——**不是**对未来收益的承诺。盈亏自负。

## 许可

内容:[CC BY 4.0](LICENSE) · 代码示例:MIT。来源均注明并链接;我们做综述与归因,不转载他人受版权保护的原文。
