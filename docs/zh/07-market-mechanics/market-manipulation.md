# 市场操纵(机构操作手册)

> 一句话:大资金扭曲价格的各种手法的总目录——幌骗(spoofing)、分层挂单(layering)、对敲刷量(wash trading)、拉高出货(pump-and-dump)、做盘(painting the tape)、囤积逼仓(cornering)、尾盘做价(marking the close)。**判决:⚠️ 真实且有充分记录——但"识别它并交易它"不是散户的优势。**

## 它是什么

市场操纵是指刻意制造虚假的价格或成交量信号。这些有名有姓的手法都很古老(大多数早于加密货币出现,并且在受监管市场中明确属于非法),但一个 24/7 运转、碎片化、监管薄弱、链上公开的市场把它们全部放大了:

- **幌骗(Spoofing)** — 下达大额限价单,意图在成交前撤销,以伪造供需。被多德-弗兰克法案 §747 列为违法;2010 年的"闪崩"就与 Navinder Sarao 在 E-mini 上的幌骗有关。
- **分层挂单(Layering)** — 在一侧的不同价位上挂出多笔虚假订单。英国 FSA 曾因此对 Swift Trade 处以 800 万英镑罚款(2011 年)。
- **对敲刷量(Wash trading)** — 同一实体既买又卖,人为制造成交量。NBER(Cong et al. 2022)估计某些 NFT 的成交量中 >70% 是对敲交易;CFTC 因虚假/对敲相关的报告问题对 Coinbase 处以 650 万美元罚款(2021 年)。
- **拉高出货(Pump-and-dump)** — 吸筹一个低流通量代币,炒作它(Telegram/Discord/X),然后向散户买盘抛售。
- **做盘(Painting the tape)** — 在关联账户之间协同交易,制造出一张"活跃"、稳步上升的图表(DEX 的"市值管理"团队)。
- **囤积逼仓(Cornering)** — 控制足够多的供给以左右价格(亨特兄弟的白银,1979–80 年)。
- **尾盘做价 / 预言机操纵(Marking the close / oracle manipulation)** — 在关键时刻推动一个参考价/标记价。2025 年 Hyperliquid 的"JELLY"事件(在稀薄市场中约 1.6 亿美元的头寸,扭曲了标记价格)就是链上版本。
- **隐藏关联方 / 虚假储备(Hidden affiliated parties / fake reserves)** — 例如,CFTC 发现 Tether 在 2016–2018 年间只有约 27.6% 的天数持有完整的法币背书(4100 万美元罚款,2021 年);FTX/Alameda 挪用客户资金导致约 80 亿美元的资金缺口,SBF 被判 25 年监禁。

## 它的主张

对散户颇具诱惑的主张是:*"学会实时识别操纵(幌骗墙、对敲量激增、巨鲸钱包动向)并反向交易它。"*链上透明度(Nansen、Arkham、Whale Alert、CoinGlass)据称让这成为可能。

## 检验

*事后为起诉而检测*操纵是真实而有效的——Chainalysis 式的取证从丝绸之路追回了 >10 亿美元,并支撑了 BitMEX/Tether/FTX 等案件。但*快到足以据此盈利地交易*则是另一个问题,它落入与 [order-flow imbalance / spoofing detection](../04-microstructure/order-flow-imbalance.md) 相同的范畴:🔶 **对 HFT 有信息价值,但散户无法执行。**

- **延迟。** 幌骗/撤单的循环活在亚秒级/毫秒级的尺度上。等散户看到那堵墙并作出反应时,它早已消失。这种优势(如果存在的话)属于共置(co-located)的挂单/maker。
- **你通常是被宰的对象,而非读盘者。** 跟随一笔可见的巨鲸入场,往往意味着成为他们的[退出流动性](../03-strategies/copy-trading.md)——存在幸存者偏差的巨鲸钱包,在去偏后对未来几乎没有任何预测力。
- **未来函数与成本。** "那是拉高出货的顶部"是事后标注;在因果上交易时,拉高出货的反向操作打不赢安慰剂,而换手会在手续费上失血。

## 判决:⚠️ 真实 / ❌ 作为散户信号不成立

这里的每一种手法都是真实的,都让散户真金白银地亏过钱,都值得了解——主要是为了让你能*避开那些专为收割你而存在的产品和模式*(流动性差的被炒作山寨币、像 Anchor 那 19.45% 那样的"保证收益"、清算簇附近的杠杆)。但"识别操纵并交易它"不是散户优势:真正可操作的检测要么是 HFT 级延迟,要么是事后取证,而散户时间尺度的版本会因未来函数、拥挤和成本而失败——与[止损猎杀](stop-hunting.md)和[流动性猎杀](liquidity-hunts.md)一样。其防御价值才是全部意义所在。

## 自己试试

你可以*复现这套取证*(Whale Alert 阈值、跨交易所价差异常、通过自成交检测对敲)以加深理解——但要检验其中任何一项是否*可交易*,就拿最干净的版本(例如,在 +30%/24h、5σ 成交量激增后反向做一笔被检测到的拉高),用 [`deflate`](https://github.com/raphael2025/deflate) 跑一遍:`placebo`、`deflated_sharpe`、`pbo`。扣除成本后的优势无法存活。

## 来源

- 维基百科 — *Market manipulation*、*Spoofing (finance)*、*Layering (finance)*、*Pump and dump*、*Wash trade*、*Front running*、*Painting the tape* — 定义与法律地位。
- CFTC 新闻稿 8369-21(Coinbase)和 8450-21(Tether)— 执法细节及 27.6% 储备的认定。
- Cong et al. (2022),*Crypto Wash Trading*,NBER WP 30783 — https://www.nber.org/papers/w30783
- 维基百科 — *Bankruptcy of FTX*、*Terra (blockchain)*、*BitMEX* — 上文引用的案例史。
- Chainalysis — 链上取证背景(事后检测,而非交易信号)。
