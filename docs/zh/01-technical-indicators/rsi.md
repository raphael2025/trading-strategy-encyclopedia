# RSI(相对强弱指数,Relative Strength Index)

> 一句话:一个 0–100 的动量振荡指标,据称用来标记"超买"(>70)和"超卖"(<30)状态。**判决:❌ 已证伪**(作为独立的买/卖信号)。

## 它是什么

RSI 由 J. Welles Wilder 于 1978 年提出,度量近期价格变动的速度与幅度。在一个回看窗口(经典为 14 个周期)上,它计算平均上涨幅度与平均下跌幅度之比,并映射到 0–100 的刻度:

```
RS  = (N 周期内的平均涨幅) / (N 周期内的平均跌幅)
RSI = 100 − 100 / (1 + RS)
```

民间读法:RSI > 70 = "超买,卖出";RSI < 30 = "超卖,买入"。变体还加入背离(价格创新高,RSI 没有)、中轴线(50)交叉和调过的阈值。

## 它的主张

一个极端的 RSI 读数标记着市场被拉伸、即将回复,所以淡化极端(超卖买入 / 超买卖出)能赚到一份均值回复溢价。它是散户交易中被传授得最广的"入场信号"之一。

## 检验

我们把 RSI 当作一条**独立的、机械式的入场规则**,在加密永续合约(BTC/ETH/SOL)和股票上做了评估,信号在 bar 收盘时打时间戳(无未来函数),并将**吃单/taker 费用 + 滑点 + 资金费内化**进收益。阈值对(30/70 水平)和回看 N 被当作一个搜索网格处理,以便我们诚实地度量选择偏差。

结论,与索引一致:

- **扣成本后无样本外优势。** 样本内"最优"的阈值/回看无法延续到样本外切分。这正是在[判决索引](../00-verdict-index.md)里**五种独立证伪方法**下统统失败的那类独立指标。
- **对选择有意识便死。** 调阈值会抬高样本内 Sharpe,但 **Deflated Sharpe/DSR**(为试过多少组阈值/回看组合而惩罚)向零崩溃。PBO 很高——样本内最优配置不过是样本外的噪声。
- **成本主导一切。** 在 RSI 触发最频繁的较低时间框架上,光是换手成本就极其残酷——正是中频方向预测在任何"信号"被讨论之前就已经损失 ≈ **每年 −86% 进了费用**的同一种状态。
- **打不过安慰剂检验(placebo test)。** RSI 入场与按时段和当下动量匹配过的随机入场无从区分。

## 判决:❌ 已证伪

作为一个独立的买/卖信号,RSI 过不了诚实检验。致命之处是**多重检验**(著名的 30/70 水平是一个无法泛化的调过的选择)与**成本**(它交易得太频繁,过不了费用关)的组合。它是对近期收益的一种*描述性*变换——用来谈论一张图表很有用——但其本身并不携带任何可被利用、能扛住成本的方向性信息。注意这个不对称:在强趋势里,"超买"能维持超买好几周,而去淡化它正是拖垮[均值回复](../03-strategies/mean-reversion.md)的那种接飞刀行为。

这是一个针对 RSI *单独作为信号*的判决——并不是说动量信息毫无价值。幸存者([趋势跟随](../03-strategies/trend-following.md)、[横截面动量](../03-strategies/cross-sectional-momentum.md))在一个对成本有意识、对选择有意识的框架内,以相反的方式使用动量(骑跨它,而不是淡化它)。

## 自己动手试

在 bar 收盘上计算 RSI(14),生成超卖做多 / 超买做空的入场信号,每次换手扣掉现实的吃单/taker 成本,然后把收益序列跑过 [`deflate`](https://github.com/raphael2025/deflate):检查 `placebo`(对比匹配过的随机入场)、`deflated_sharpe`(惩罚你搜索过的阈值网格)和 `pbo`(样本内最优阈值能在样本外幸存吗?)。失败的正是 DSR/PBO 这一步。

## 参考来源

- Wilder, J. Welles (1978), *New Concepts in Technical Trading Systems* —— RSI 的原始定义。
- Bailey & López de Prado (2014), "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality," *Journal of Portfolio Management*.
- Bailey, Borwein, López de Prado & Zhu (2017), "The Probability of Backtest Overfitting," *Journal of Computational Finance* (PBO/CSCV)。
