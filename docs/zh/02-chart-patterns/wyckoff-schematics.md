# 威科夫示意图(图表形态视角)

> 一句话:威科夫(Wyckoff)方法中的弹簧、上冲、交易区间示意图,画在价格图上的样子。**判决:作为择时形态 ❌(含未来函数 + 主观性)。**

## 它是什么

本条目讲的是威科夫的*图表形态*那一面:教科书式的**吸筹(accumulation)**与**派发(distribution)**示意图及其命名事件——*卖出/买入高潮、自动反弹/回落、二次测试、弹簧(spring,假跌破)、上冲/UTAD(假突破)、强势/弱势信号、最后支撑点*。交易者把这些画在图上,试图在弹簧处入场(做多)或在上冲处入场(做空)。完整的方法、定律以及"综合人(Composite Man)"的框架,见市场机制部分的[威科夫吸筹与派发](../07-market-mechanics/wyckoff-accumulation-distribution.md)。

## 主张

主张是:示意图能在*区间仍在形成之际*告诉你,聪明钱是在吸筹还是在派发——于是弹簧是一个高胜率的做多入场点,上冲是一个高胜率的做空入场点,止损就紧贴在假突破之外。

## 检验

作为一种图表形态,它继承了标准的形态杀手:

- **未来函数。**只有当价格回到区间内时,一个"弹簧"才算弹簧;如果它继续下跌,那就是一次跌破。在刺破的那一刻你无从判断是哪一种——给它贴标签需要未来信息。这与[头肩形态](head-and-shoulders.md)、[三角形](triangles-flags-wedges.md)和[艾略特波浪(Elliott Wave)](elliott-wave.md)是同样的结构性缺陷。
- **主观性。**哪个区间、哪个低点才是"那个"弹簧、刺破多深才算数——全凭自由裁量,因此示意图能拟合过去,却在样本外过拟合。
- **拥挤的价位 + 成本。**区间边缘恰恰是止损聚集之处,使它们成为绝佳的[流动性猎杀](../07-market-mechanics/liquidity-hunts.md)目标;日内逆势挂单去吃这些价位会败给手续费和滑点,正如本书检验过的其他每一种[假突破逆势交易](../00-verdict-index.md)一样。

## 判决:❌

威科夫示意图是一幅有用的*图景*,描绘了区间有时如何收尾,但作为机械化入场它失败了:弹簧/上冲的标签是事后的,画法是主观的,而那些价位是拥挤的流动性。它所暗示的那种持续性(拉升/打压)被缓慢的[趋势跟随](../03-strategies/trend-following.md)和[突破](../03-strategies/breakout.md)以诚实的方式捕捉。更宽广的框架以及同样的判决,见[市场机制条目](../07-market-mechanics/wyckoff-accumulation-distribution.md)。

## 自己试试

把"弹簧 = 在刺破区间低点后的 K 根 K 线内收盘价重回区间内"编码出来,做因果时间戳,加上成本,然后跑 [`deflate`](https://github.com/raphael2025/deflate) 的 `placebo` + `deflated_sharpe`。这个因果定义去掉了那个让它看起来很美的事后视角。

## 来源

- 维基百科 —— *Technical analysis*、*Chart pattern*。
- Wyckoff, R. D. —— 原始的吸筹/派发示意图(20 世纪早期;二手综述)。
- Bailey, Borwein, López de Prado & Zhu(2017),"The Probability of Backtest Overfitting."
