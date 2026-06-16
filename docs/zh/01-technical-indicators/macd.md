# MACD(移动平均收敛发散,Moving Average Convergence Divergence)

> 一句话:由两条指数移动平均线之差构建的动量指标,据称在其两条线交叉时标记趋势转折。**判决:❌ 已证伪**(作为独立的买/卖信号)。

## 它是什么

MACD 由 Gerald Appel 在 1970 年代末提出,是一种经过平滑的动量变换。它跟踪三条序列:

```
MACD line   = EMA(12) − EMA(26)        (价格的快 EMA 减慢 EMA)
signal line = EMA(9) of the MACD line
histogram   = MACD line − signal line
```

民间读法:**看涨交叉**(MACD 线上穿信号线)是买入;**看跌交叉**(下穿)是卖出。变体还加入**零轴交叉**(MACD 在 0 上方/下方)和**背离**(价格创新高,MACD 没有)。

## 它的主张

一条快均线和一条慢均线之差度量了动量的变化,所以当快分量从慢分量拉开的那一刻,你就早早抓住了一波新趋势——买在看涨交叉,卖在看跌交叉,再让 histogram 确认强度。

## 检验

我们把 MACD 当作一条**独立的、机械式的交叉入场规则**,在加密永续合约(BTC/ETH/SOL)和股票上做了评估,信号在 bar 收盘时打时间戳(无未来函数),并将**吃单/taker 费用 + 滑点 + 资金费内化**。(12, 26, 9) 参数和一系列变体被当作一个搜索网格,以便选择偏差被度量出来,而不是被藏起来。

结论,与索引一致:

- **扣成本后无样本外优势。** 样本内"最优"的参数三元组无法延续到样本外切分——正是在[判决索引](../00-verdict-index.md)里**五种独立证伪方法**下统统失败的那类独立指标。
- **对选择有意识便死。** 调这三个窗口会抬高样本内 Sharpe,但 **Deflated Sharpe/DSR**(为试过多少组参数而惩罚)向零崩溃,且 PBO 很高——样本内最优配置不过是样本外的噪声。
- **成本主导一切。** MACD 在震荡中无休止地反复打脸,产生大量来回交易;光是换手成本就是拖垮中频方向预测的同一种残酷拖累(≈ **每年 −86% 进了费用**)。
- **打不过安慰剂检验(placebo test)。** 交叉入场与按时段和当下动量匹配过的随机入场无从区分。

## 判决:❌ 已证伪

作为一个独立的交叉信号,MACD 过不了诚实检验。致命之处是**多重检验**(著名的 12/26/9 是一个调出来的历史遗留产物——那些长度并无特别之处,而且无法泛化)外加**成本**(交叉在横盘市场里不停触发并流血般地耗费费用)。MACD 是两条移动平均线之差的滞后、平滑版本——结构上和[移动平均线交叉](./moving-averages.md)属于同一类,死法也一样。

注意这个重要的不对称:一个**缓慢的、对成本有意识、对选择有意识的[趋势跟随](../03-strategies/trend-following.md)系统**,即便恰好用到移动平均线,也可以是 ✅(Sharpe ~1.1)。那和"MACD 看涨交叉就是买入"*不是*一回事。主动地去交易交叉、用调出来的默认参数、快到足以反复打脸——这是对选择视而不见的民间传说,而这里失败的正是它。

## 自己动手试

在 bar 收盘上生成看涨交叉做多 / 看跌交叉做空的入场信号,每次换手扣掉现实的吃单/taker 成本,然后把收益序列跑过 [`deflate`](https://github.com/raphael2025/deflate):检查 `placebo`(对比匹配过的随机入场)、`deflated_sharpe`(惩罚你搜索过的 (fast, slow, signal) 网格)和 `pbo`(样本内最优三元组能在样本外幸存吗?)。失败的正是 DSR/PBO 这一步。

## 参考来源

- Appel, Gerald —— MACD 的原创者;他本人的论述见 *Technical Analysis: Power Tools for Active Investors* (2005)。
- Bailey & López de Prado (2014), "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality," *Journal of Portfolio Management*.
