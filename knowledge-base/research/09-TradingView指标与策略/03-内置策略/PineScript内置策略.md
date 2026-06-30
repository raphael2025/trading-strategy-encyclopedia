# Pine Script v5 内置策略全解（加密货币实战）

> 编制说明：本文基于 **TradingView Pine Script v5 User Manual / Strategies** 官方文档、**Wikipedia 策略概念条目**（趋势跟随/均值回归/动量/对冲）、**Investopedia 策略教程**、**PineCoders/pine-utils 真实代码片段**整理。**专攻 Pine v5 策略框架**：`strategy.*` 命名空间全解、订单生命周期、回测机制、加密实战。与 [PineScript内置指标.md](../01-内置指标/PineScript内置指标.md) 互补——后者讲 `ta.*` 指标 API，本文讲 `strategy.*` 策略 API。

---

## 目录

1. [Pine v5 策略基础](#1-pine-v5-策略基础)
2. [strategy() 声明与核心参数](#2-strategy-声明与核心参数)
3. [订单生命周期：5 个下单 + 2 个撤单函数](#3-订单生命周期5-个下单--2-个撤单函数)
4. [订单类型：market / limit / stop / stop-limit](#4-订单类型market--limit--stop--stop-limit)
5. [仓位控制：quantity, pyramiding, margin](#5-仓位控制quantity-pyramiding-margin)
6. [Strategy Tester：4 个 tab 全解](#6-strategy-tester4-个-tab-全解)
7. [Broker Emulator：回测模拟的核心机制](#7-broker-emulator回测模拟的核心机制)
8. [经典策略框架：7 个最常用骨架](#8-经典策略框架7-个最常用骨架)
9. [加密货币专属策略模板](#9-加密货币专属策略模板)
10. [引用与延伸阅读](#10-引用与延伸阅读)

---

## 1. Pine v5 策略基础

### 1.1 indicator() vs strategy()

| 维度 | `indicator()` | `strategy()` |
|------|--------------|--------------|
| 绘图 | ✅ | ✅ |
| 模拟下单 | ❌ | ✅ |
| Strategy Tester | ❌ | ✅ |
| Alerts | ✅ | ✅ |
| 用途 | 画图分析 | **回测/模拟交易** |

**判断脚本类型**：在 Pine Editor 看声明行：
```pine
//@version=5
indicator("My Indicator")    // 指标脚本
strategy("My Strategy")      // 策略脚本
```

### 1.2 策略脚本的 4 大能力

> Pine Script strategies are specialized scripts that simulate trades across historical and realtime bars, allowing users to backtest and forward test their trading systems. — TradingView Pine Script v5 Manual

1. **回测（Backtest）** —— 在历史 K 线上模拟交易
2. **前测（Forward Test）** —— 在实时 K 线上继续运行
3. **下单模拟（Order Simulation）** —— 模拟 5 种订单类型
4. **绩效分析（Performance Analysis）** —— Strategy Tester 自动计算胜率、夏普、最大回撤

### 1.3 关键概念

| 概念 | 含义 |
|------|------|
| **Order（订单）** | `strategy.entry()` 等函数发出的"指令" |
| **Trade（成交）** | Broker emulator 实际执行的事务 |
| **Position（持仓）** | 当前未平仓的头寸（多头/空头/无） |
| **Fill（成交价格）** | 订单被模拟成交的价格 |
| **OCA Group** | One-Cancels-All 订单组（详见 §3） |

---

## 2. strategy() 声明与核心参数

### 2.1 完整声明

```pine
//@version=5
strategy(
  title,                 // 必填，策略名
  shorttitle,            // 缩写
  overlay,               // true=主图，false=副图
  format,                // format.price / format.volume
  precision,             // 小数位
  scale,                 // 缩放
  pyramiding,            // 同方向最大加仓次数
  default_qty_type,      // 默认数量类型
  default_qty_value,     // 默认数量值
  initial_capital,       // 初始资金
  currency,              // 账户货币
  commission_type,       // 手续费类型
  commission_value,      // 手续费值
  slippage,              // 滑点
  process_orders_on_close,// bar 关闭时立即处理
  calc_on_every_tick,    // 实时每 tick 计算
  calc_on_order_fills,   // 每次成交时计算
  fill_orders_on_standard_ohlc, // HA 图用真实 OHLC 成交
  max_bars_back          // 引用历史最大 bar 数
)
```

### 2.2 实战推荐配置（加密货币）

```pine
strategy(
  "My Crypto Strategy",
  overlay=true,
  initial_capital=10000,           // 1 万 USDT 起始
  currency=currency.USDT,         // 账户货币 USDT
  default_qty_type=strategy.percent_of_equity,  // 按资金比例下单
  default_qty_value=10,            // 10% 资金
  commission_type=strategy.commission.percent,  // 0.1% 手续费
  commission_value=0.1,            // 假设币安费率
  slippage=2,                     // 2 个 tick 滑点
  pyramiding=3,                   // 最多 3 次加仓
  calc_on_order_fills=true,       // 每次成交重算
  process_orders_on_close=true,   // bar 关闭立即处理
  max_bars_back=5000
)
```

### 2.3 关键参数详解

#### `default_qty_type` 与 `default_qty_value`

| qty_type | qty_value 含义 | 实战场景 |
|----------|----------------|----------|
| `strategy.fixed` | 固定合约/股数 | 加密永续合约（1 张=0.001 BTC） |
| `strategy.cash` | 固定 USD 金额 | 现货定投 |
| `strategy.percent_of_equity` | 资金 % | **推荐**（动态复利） |

```pine
// 风险控制版本：每笔最多 2% 资金
risk_pct = 2
stop_distance = entry - stopLoss
position_size = (strategy.equity * risk_pct / 100) / stop_distance
strategy.entry("L", strategy.long, qty=position_size)
```

#### `pyramiding`

- `pyramiding=1`（默认）：同方向只能持 1 仓
- `pyramiding=3`：最多同向 3 仓（**马丁 / 趋势加仓策略需要**）
- **警告**：`pyramiding=0` 表示禁止所有新订单

#### `currency`

| currency.* | 含义 |
|------------|------|
| `currency.NONE` | 默认（与 chart 相同） |
| `currency.USD` / `currency.USDT` | 美元 / 泰达币 |
| `currency.BTC` / `currency.ETH` | 币本位策略 |
| `currency.EUR` / `currency.GBP` | 欧/英镑 |

**加密首选**：`currency.USDT`（永续合约）或 `currency.NONE`（现货）。

#### `commission_type`

| 类型 | 含义 |
|------|------|
| `strategy.commission.none` | 无手续费 |
| `strategy.commission.percent` | % 手续费（推荐加密） |
| `strategy.commission.cash_per_contract` | 固定每张 |
| `strategy.commission.cash_per_order` | 固定每笔 |

**加密主流交易所费率**：
- **Binance 现货**：0.1% (taker/maker 0.1/0.075)
- **Binance 永续**：0.04% (taker/maker 0.04/0.02)
- **Bybit 永续**：0.055% (taker/maker 0.055/0.02)
- **OKX 永续**：0.05% (taker/maker 0.05/0.02)

#### `slippage`

- 单位：**tick**（1 tick = `syminfo.mintick`）
- 加密推荐：**2-5 tick**
- 大订单/低流动性币：**5-10 tick**

#### `process_orders_on_close` ⚠️

- `false`（默认）：bar 关闭后，下个 bar 开盘才成交
- `true`：bar 关闭**立即**成交（**重要！** 影响回测结果）

**示例影响**：
- `false` + 1D 周期：今天收盘信号 → **明天开盘**成交
- `true` + 1D 周期：今天收盘信号 → **今天收盘**成交

**加密实战**：
- 现货：**false**（无法保证收盘成交）
- 永续：**true** 也合理（24h 持续交易）

#### `fill_orders_on_standard_ohlc` ⚠️

- 默认：`false`
- 用途：**Heikin Ashi 等非标准图**下，用真实 OHLC 成交（避免 HA 假价格）
- 实战：**HA 图必开**，否则回测完全失真

```pine
strategy("My HA Strategy",
         fill_orders_on_standard_ohlc=true)  // HA 真实成交
```

---

## 3. 订单生命周期：5 个下单 + 2 个撤单函数

### 3.1 全景图

```
下单 (entry/order/exit/close/close_all)
       ↓
   Broker Emulator
       ↓
   成交 / 取消
       ↓
   Trade 计入 Strategy Tester
```

### 3.2 `strategy.entry()` — 入场下单（最常用）

**完整签名**：
```pine
strategy.entry(
  id,                    // string 必填，订单唯一 ID
  direction,             // strategy.long / strategy.short / strategy.close
  qty,                   // 数量（默认 = default_qty_value）
  limit,                 // 限价（可选）
  stop,                  // 止损价（可选）
  oca_name,              // OCA 组名（可选）
  oca_type,              // OCA 类型（可选）
  comment,               // 注释（Strategy Tester 显示）
  alert_message,         // alert 消息
  disable_alert          // 是否禁用 alert
) → void
```

**最简用法**：
```pine
if ta.crossover(fastMA, slowMA)
    strategy.entry("Long", strategy.long)  // 立即多

if ta.crossunder(fastMA, slowMA)
    strategy.entry("Short", strategy.short) // 立即空
```

**关键特性：自动反转**：
- `strategy.entry()` 的核心特性是**自动反转持仓**
- 如果当前持空仓 1 BTC，调用 `strategy.entry("L", strategy.long)` → 自动**平空 + 开多 1 BTC**
- **不需要**先 `strategy.close()` 再 `strategy.entry()`

```pine
// 反转示例
if longSignal
    strategy.entry("Reversal Long", strategy.long)  // 自动平空 + 开多
```

**带止损止盈**（推荐用 `strategy.exit()` 单独管理，详见 §3.4）。

### 3.3 `strategy.order()` — 通用下单（手动控制反转）

**与 entry 的区别**：

| 维度 | `strategy.entry()` | `strategy.order()` |
|------|--------------------|---------------------|
| 自动反转 | ✅ | ❌ |
| 自动累计仓位 | ✅ | ❌ |
| 用途 | **策略主入场** | 复杂自定义 |

```pine
// 用 order 实现双向下单（不自动反转）
if longCondition
    strategy.order("L", strategy.long)   // 不会自动平空
```

**实战**：
- 大多数策略用 `strategy.entry()` 即可
- 仅在**需要精细控制**（如对冲、网格）时用 `strategy.order()`

### 3.4 `strategy.exit()` — 出场（带止损止盈）

**完整签名**：
```pine
strategy.exit(
  id,                    // 出场 ID（唯一）
  from_entry,            // 关联入场 ID（不填则关联所有）
  qty,                   // 退出数量
  qty_percent,           // 退出百分比
  profit,                // 止盈（点数）
  limit,                 // 限价（止盈）
  loss,                  // 止损（点数）
  stop,                  // 止损价
  trail_price,           // 跟踪止盈触发价
  trail_points,           // 跟踪止盈点数
  trail_offset,          // 跟踪止盈偏移
  oca_name,              // OCA 组
  comment,               // 注释
  alert_message,
  disable_alert
) → void
```

**经典用法：Bracket Order（括号单）**：
```pine
// 入场
if longCondition
    strategy.entry("L", strategy.long)

// 自动绑定止损止盈（不用 from_entry，自动找最后入场）
strategy.exit("L Exit", "L", stop=entry - 2*atr, limit=entry + 4*atr)
```

**盈亏比 1:2**（推荐加密）：
```pine
atr_val = ta.atr(14)
risk = 2 * atr_val
reward = 4 * atr_val  // 1:2 风险回报比

if longCondition
    strategy.entry("L", strategy.long)
    strategy.exit("L Exit", "L", stop=entry - risk, limit=entry + reward)
```

**追踪止损（Trail Stop）**：
```pine
// 上涨 1 ATR 后启动跟踪止损，止损距离 2 ATR
strategy.exit(
  "Trail",
  "L",
  trail_price=entry + 1*atr_val,
  trail_points=2 * atr_val / syminfo.mintick,
  trail_offset=1 * atr_val / syminfo.mintick
)
```

**实战金标准**：
- **止损**：1.5-2 × ATR（基于 1D ATR(14)）
- **止盈**：3-4 × ATR（**盈亏比 ≥ 1:2**）
- **追踪止损**：1 × ATR 触发，1.5 × ATR 距离

### 3.5 `strategy.close()` — 平指定入场

```pine
// 单独平掉 "Buy1" 这个入场
strategy.close("Buy1", comment="Close Buy1")
```

**与 `close_all` 的区别**：
- `close("id")`：只平指定 id
- `close_all(comment)`：平所有头寸

### 3.6 `strategy.close_all()` — 全部平仓

```pine
if exitCondition
    strategy.close_all(comment="Emergency Exit")
```

**实战**：
- **紧急平仓**（如黑天鹅）
- **调仓时点**（如季度换币）
- **风控**：当日亏损超 2% → 立即 `close_all()`

### 3.7 `strategy.cancel()` / `cancel_all()` — 撤单

```pine
// 撤销指定 ID 的 pending order
strategy.cancel("My Entry Id")

// 撤销所有 pending orders
strategy.cancel_all()
```

**实战**：
- 撤销未成交的**限价单**（如挂单 2 小时未成交）
- 信号消失时清理挂单

### 3.8 OCA Groups（One-Cancels-All）

**三种 OCA 类型**：
- `strategy.oca.cancel` — 成交一个取消全部
- `strategy.oca.reduce` — 成交一个减少其他
- `strategy.oca.none` — 不取消（默认）

**实战场景：突破策略**
```pine
if breakoutUp
    strategy.entry("Long Break", strategy.long, stop=high+10, oca_name="Breakout", oca_type=strategy.oca.cancel)
    strategy.entry("Short Break", strategy.short, stop=low-10, oca_name="Breakout", oca_type=strategy.oca.cancel)
```

价格上涨突破 high+10 → 多单成交 → 空单自动撤销。

### 3.9 完整策略骨架

```pine
//@version=5
strategy("ATR Bracket", overlay=true,
         initial_capital=10000,
         currency=currency.USDT,
         default_qty_type=strategy.percent_of_equity,
         default_qty_value=10,
         commission_type=strategy.commission.percent,
         commission_value=0.1)

// 参数
length = input.int(14, "ATR Length")
mult   = input.float(2.0, "ATR Mult")

// 信号
[supertrend, dir] = ta.supertrend(10, 3.0)
atr_val = ta.atr(length)

// 入场
if dir > 0 and dir[1] < 0   // 翻多
    strategy.entry("L", strategy.long)
    strategy.exit("L Exit", "L",
                  stop=close - mult*atr_val,
                  limit=close + 3*mult*atr_val)

if dir < 0 and dir[1] > 0   // 翻空
    strategy.entry("S", strategy.short)
    strategy.exit("S Exit", "S",
                  stop=close + mult*atr_val,
                  limit=close - 3*mult*atr_val)
```

---

## 4. 订单类型：market / limit / stop / stop-limit

### 4.1 4 种类型总览

| 类型 | 触发 | 用途 | 加密实战 |
|------|------|------|----------|
| **Market** | 立即 | 入场主力 | **默认** |
| **Limit** | 价格 ≤ 限价（多） / ≥ 限价（空） | 逢低挂单 | 网格、抄底 |
| **Stop** | 价格突破 stop 价 | 突破策略 | 趋势跟随 |
| **Stop-Limit** | 突破 stop 后，下 limit 单 | 减少滑点 | 大资金 |

### 4.2 Market Order（市价单）

```pine
strategy.entry("Mkt Long", strategy.long)  // 默认市价
```

**成交时机**：bar 关闭后下个 bar 开盘（`process_orders_on_close=false`）

### 4.3 Limit Order（限价单）

```pine
// 限价 100 USDT 买入
strategy.entry("Limit Buy", strategy.long, limit=100)

// 用 ta.pivothigh/low 自动算限价
ph = ta.pivothigh(high, 5, 5)
pl = ta.pivotlow(low, 5, 5)
if not na(pl)
    strategy.entry("Limit Buy", strategy.long, limit=pl)
```

**实战**：
- **支撑位挂单**（如前低、斐波那契位）
- **网格策略**（每跌 1% 挂一单）
- **加密现货抄底**

### 4.4 Stop Order（止损单）

```pine
// 突破 100 USDT 买入（追涨）
strategy.entry("Stop Buy", strategy.long, stop=100)
```

**实战**：
- **趋势突破**入场
- **回测突破**（突破前高 + 成交量）

### 4.5 Stop-Limit Order

```pine
// 突破 100 USDT 后，下 100.5 USDT 限价单（避免追高成交到 110）
strategy.entry("SL Buy", strategy.long, stop=100, limit=100.5)
```

**实战**：
- **大资金**：避免市价单滑点
- **低流动性币**：插针时市价单会成"接刀侠"
- **加密永续**：突破关键位 + 限价防滑点

---

## 5. 仓位控制：quantity, pyramiding, margin

### 5.1 固定数量 vs 资金比例

| 模式 | 代码 | 适用 |
|------|------|------|
| 固定张数 | `default_qty_type=strategy.fixed, default_qty_value=1` | 永续合约 |
| 固定 USD | `default_qty_type=strategy.cash, default_qty_value=500` | 现货定投 |
| 资金 % | `default_qty_type=strategy.percent_of_equity, default_qty_value=10` | **推荐** |

### 5.2 基于风险的数量计算（最稳健）

```pine
// 凯利公式简化版：单笔风险 2%
risk_pct    = input.float(2.0, "Risk %")
entry_price = close
stop_loss   = entry_price - 2 * ta.atr(14)
stop_dist   = entry_price - stop_loss

risk_amount = strategy.equity * risk_pct / 100
qty         = risk_amount / stop_dist

if longCondition
    strategy.entry("L", strategy.long, qty=qty)
    strategy.exit("L SL", "L", stop=stop_loss)
```

### 5.3 Pyramiding（加仓）

```pine
strategy("Trend Pyramid", pyramiding=3)  // 最多 3 次加仓

if longCondition1
    strategy.entry("L1", strategy.long, qty=strategy.equity * 0.05 / close)
if longCondition2  // 趋势更强
    strategy.entry("L2", strategy.long, qty=strategy.equity * 0.05 / close)
if longCondition3
    strategy.entry("L3", strategy.long, qty=strategy.equity * 0.05 / close)
```

**实战**：
- **金字塔加仓**：每次加仓金额递减（5% → 3% → 2%）
- **马丁加仓**：每次加仓金额递增（**高风险，谨慎**）
- **推荐**：金字塔 + 总仓位 ≤ 30%

### 5.4 margin_long / margin_short

```pine
strategy("Margin Test", margin_long=50, margin_short=50)
// margin = 50% 表示只用 50% 资金就可开仓（2x 杠杆）
// margin = 100% 表示 1x 杠杆（默认）
// margin = 10% 表示 10x 杠杆
```

**加密实战**：
- **永续合约 1x-3x 杠杆**：margin=33-100
- **5x+ 杠杆**：margin ≤ 20
- **10x+ 杠杆**：margin ≤ 10（**极度危险**）

---

## 6. Strategy Tester：4 个 tab 全解

加载策略后，底部 **Strategy Tester** 标签有 4 个子标签：

### 6.1 Overview

显示**绩效概览**：
- **Equity baseline**：策略净值曲线
- **Drawdown column**：回撤柱状图
- **Buy & hold equity**：同期买入持有的对比

**关键指标**：
- **Net Profit %**：总收益率
- **Max Drawdown %**：最大回撤（**最重要**）
- **Win Rate %**：胜率
- **Profit Factor**：盈亏比
- **Sharpe Ratio**：夏普比率
- **Sortino Ratio**：索提诺比率
- **Total Trades**：总交易次数
- **Avg Trade**：平均每笔盈亏

### 6.2 Performance Summary

详细指标表：

| 指标 | 计算 |
|------|------|
| Net Profit | 总收益（绝对值） |
| Total Trades | 交易次数 |
| Win Rate | 盈利交易 / 总交易 |
| Profit Factor | 总盈利 / 总亏损 |
| Max Drawdown | 峰值 → 谷底最大跌幅 |
| Avg Trade | Net Profit / Total Trades |
| Avg Bars in Trade | 平均持仓 bar 数 |

### 6.3 List of Trades

每笔交易明细：
- Entry Time / Price
- Exit Time / Price
- Direction（多/空）
- **Trade PnL**
- **Cumulative PnL**
- **Drawdown %**

**实战**：用 List of Trades 导出 CSV 到 Excel，做深度分析。

### 6.4 Properties

策略的"配置参数"——可在加载时调整：
- Date Range（回测区间）
- Initial Capital
- Commission
- Slippage
- Order Size
- Pyramiding

---

## 7. Broker Emulator：回测模拟的核心机制

> **关键认知**：TV 的回测**不是真实下单**，而是 broker emulator 模拟。**理解 emulator 行为是避免回测陷阱的前提**。

### 7.1 默认行为

> By default, the emulator fills a strategy's orders exclusively using available chart data. Consequently, it executes orders on historical bars after a bar closes. — TradingView Manual

- **历史 bar**：bar 关闭后才成交
- **实时 bar**：新 tick 进来才成交

### 7.2 4 步价格推断（emulator 核心）

**当 bar 关闭时，emulator 推断 bar 内的价格路径**：

| 开盘价位置 | 推断路径 |
|-----------|----------|
| 开盘价更接近**最高** | Open → High → Low → Close |
| 开盘价更接近**最低** | Open → Low → High → Close |

**含义**：当有 limit / stop 单时，emulator 按推断路径"扫描"。

### 7.3 关键警告：非标准图

> **Heikin Ashi / Renko / Kagi / Point & Figure / Range** 图的策略回测**默认不可信**！

**原因**：HA 收盘价 ≠ 真实收盘价，回测用的是"合成价格"。

**修复**：
```pine
strategy("My HA Strategy", fill_orders_on_standard_ohlc=true)
```

**加密实战**：
- **HA + fill_orders_on_standard_ohlc=true** = HA 视觉 + 真实成交
- **Renko**：建议在普通 K 线回测
- **Point & Figure**：建议用专门平台

### 7.4 现实与回测的差距

| 维度 | 回测 | 现实 |
|------|------|------|
| 流动性 | 无限 | 有限 |
| 滑点 | 0-2 tick | 5-50 tick |
| 手续费 | 固定 0.1% | VIP 0.02% / 普通 0.1% |
| 成交 | 100% | 90-99% |
| 资金费率 | **❌ 不算** | 永续合约每日 ±0.01% |

**加密实战**：
- **永续策略**：回测**一定要**加资金费率（手动加 0.1%/天）
- **低流动性币**：滑点加 5-10 tick
- **大资金**：单笔 ≤ 总市值的 0.5%

### 7.5 4 大回测陷阱

1. **未来函数**（look-ahead）—— 用 `close[0]` 算信号是**作弊**！
2. **幸存者偏差** —— 只在还存在的币上回测
3. **过拟合** —— 参数调到 2017 完美但 2024 失败
4. **样本过少** —— 加密只有 8 年数据，至少要 100 笔交易

**防御**：
- Walk-Forward Analysis
- Out-of-sample 测试
- 至少 3 个市场周期（牛/熊/震荡）

---

## 8. 经典策略框架：7 个最常用骨架

### 8.1 双均线交叉（MA Cross）

```pine
//@version=5
strategy("MA Cross", overlay=true)
fast = ta.ema(close, 9)
slow = ta.ema(close, 21)
if ta.crossover(fast, slow)
    strategy.entry("L", strategy.long)
if ta.crossunder(fast, slow)
    strategy.entry("S", strategy.short)
strategy.exit("Exit", from_entry="L", stop=close-2*ta.atr(14), limit=close+4*ta.atr(14))
strategy.exit("Exit", from_entry="S", stop=close+2*ta.atr(14), limit=close-4*ta.atr(14))
```

**来源**：Wikipedia / Investopedia 的**动量策略**（Momentum Strategy）。
> A momentum strategy is a strategy that aims to capitalize on the continuance of an existing market trend. — [Wikipedia: Momentum (finance)](https://en.wikipedia.org/wiki/Momentum_(finance))

### 8.2 RSI 反转

```pine
//@version=5
strategy("RSI Reversion", overlay=false)
rsi = ta.rsi(close, 14)
if rsi < 30 and rsi > rsi[1]  // 超卖回升
    strategy.entry("L", strategy.long)
if rsi > 70 and rsi < rsi[1]  // 超买卖出
    strategy.entry("S", strategy.short)
```

**来源**：**均值回归**（Mean Reversion）。
> Mean reversion is a financial theory suggesting that asset prices and historical returns eventually revert to their long-run mean or average. — [Investopedia: Mean Reversion](https://www.investopedia.com/terms/m/meanreversion.asp)

### 8.3 布林带回归（BB Reversion）

```pine
//@version=5
strategy("BB Reversion", overlay=true)
[m, u, l] = ta.bb(close, 20, 2)
if close < l
    strategy.entry("L", strategy.long)
if close > u
    strategy.entry("S", strategy.short)
```

### 8.4 突破 + ATR 止损（Donchian Breakout）

```pine
//@version=5
strategy("Donchian Break", overlay=true)
length = input.int(20, "Length")
hh = ta.highest(high, length)
ll = ta.lowest(low, length)
if close > hh[1]
    strategy.entry("L", strategy.long)
if close < ll[1]
    strategy.entry("S", strategy.short)
strategy.exit("Exit", from_entry="L", stop=close-2*ta.atr(14), limit=close+4*ta.atr(14))
```

**来源**：**趋势跟随**（Trend Following）+ Donchian 海龟策略。
> Trend following is an investment strategy that tries to take advantage of long- term moves in the market. — [Wikipedia: Trend following](https://en.wikipedia.org/wiki/Trend_following)

### 8.5 网格策略（Grid Trading）

```pine
//@version=5
strategy("Grid", overlay=true,
         pyramiding=10,
         default_qty_type=strategy.percent_of_equity,
         default_qty_value=5)

grid_size = input.float(1.0, "Grid %")
last_entry = strategy.position_avg_price

// 跌破网格下沿 → 买入
if strategy.position_size == 0 or close < last_entry * (1 - grid_size/100)
    strategy.entry("L", strategy.long)

// 涨破网格上沿 → 平仓
if strategy.position_size > 0 and close > last_entry * (1 + grid_size/100)
    strategy.close_all()
```

**来源**：加密货币量化**经典策略**，社区策略页中"3Commas POL Grid Bot Long" "BNB Grid Bot Long"即此类型。

### 8.6 资金费率套利（Funding Rate Arbitrage）

```pine
//@version=5
strategy("Funding Arb", overlay=true)
// 监控 funding rate（需要外部数据或 manual input）
// 简化版：BTCUSDT.P 永续 vs 现货价差
spot = request.security("BTCUSDT", "D", close)
perp = close
basis = (perp - spot) / spot * 100  // 基差 %

if basis > 0.1   // 永续溢价 > 0.1%
    strategy.entry("Spot Buy", strategy.long)
    strategy.entry("Perp Sell", strategy.short)  // 需 manual 实现
```

**实战**：需要**同时**操作现货 + 永续，Pine 单脚本不能直接做。

### 8.7 海龟交易法（Turtle Trading）

```pine
//@version=5
strategy("Turtle", overlay=true,
         pyramiding=4)
entry_len = input.int(20, "Entry")
exit_len  = input.int(10, "Exit")
hh = ta.highest(high, entry_len)
ll = ta.lowest(low, entry_len)
hh_exit = ta.highest(high, exit_len)
ll_exit = ta.lowest(low, exit_len)

if close > hh[1]
    strategy.entry("L", strategy.long)
if close < ll[1]
    strategy.entry("S", strategy.short)
if strategy.position_size > 0 and close < ll_exit[1]
    strategy.close_all(comment="Turtle Exit")
if strategy.position_size < 0 and close > hh_exit[1]
    strategy.close_all(comment="Turtle Exit")
```

**来源**：Richard Donchian + Richard Dennis（1983 海龟实验）。

---

## 9. 加密货币专属策略模板

### 9.1 24/7 不停盘的处理

加密货币 24 小时不停盘，回测时**不能**沿用股票市场的"日内 session"概念。

```pine
// 用 UTC 时段模拟"日切"
utc_hour = hour(time, "UTC")
new_day  = ta.change(utc_hour) < 0  // 跨日检测

// 自定义"session"（亚洲 0-8 UTC, 伦敦 8-16, 纽约 13-22）
asian_session = (utc_hour >= 0 and utc_hour < 8)
london_session = (utc_hour >= 8 and utc_hour < 16)
ny_session = (utc_hour >= 13 and utc_hour < 22)
```

### 9.2 资金费率（Funding Rate）整合

永续合约每日 0:00 / 8:00 / 16:00 UTC 结算资金费率。**Pine 不能直接读 funding rate**，需用 input 手动输入或外部数据源。

**回测时**：
- 假设平均 funding rate = 0.01%/8h = 0.03%/天
- 8h 持多头 = **-0.01%** 额外成本（被收）
- **建议**：回测时手动加 0.05-0.1% 的"摩擦成本"到手续费

### 9.3 现货 vs 合约的区别

| 维度 | 现货 | 永续合约 |
|------|------|----------|
| 资金费率 | ❌ | ✅ |
| 杠杆 | 1x | 1-125x |
| 爆仓 | 无 | 有（**最大风险**） |
| 策略适配 | 定投、抄底 | 趋势、套利、对冲 |

### 9.4 加密独有的策略类型

| 策略 | 机制 | 加密适配 |
|------|------|----------|
| **Funding Rate Arbitrage** | 现货 vs 永续基差 | ⭐⭐⭐⭐⭐ |
| **Liquidation Cascade** | 爆仓连锁 | ⭐⭐⭐⭐⭐ |
| **Stablecoin Peg** | USDT/USDC 偏离 1 USD | ⭐⭐⭐⭐ |
| **Cross-Exchange Arb** | 跨所价差 | ⭐⭐⭐ |
| **On-chain Analysis** | 链上数据 | 需外部数据 |
| **Mempool Sniping** | 内存池抢跑 | 需特殊权限 |
| **MEV / Sandwich** | 三明治攻击 | ⚠️ 灰色 |

详见本仓库 `03-市场机制/01-流动性/流动性猎杀机制.md`。

### 9.5 加密推荐策略框架（实战）

```pine
//@version=5
// 综合模板：BTC 4h + SuperTrend + ADX 过滤 + ATR 仓位 + 跟踪止损
strategy("Crypto Composite",
         overlay=true,
         initial_capital=10000,
         currency=currency.USDT,
         default_qty_type=strategy.percent_of_equity,
         default_qty_value=5,  // 5% 资金
         commission_type=strategy.commission.percent,
         commission_value=0.1,
         slippage=3,
         pyramiding=2)

// === 指标 ===
[st, dir] = ta.supertrend(10, 3.0)
adx = ta.dmi(14, 14)[2]
atr_val = ta.atr(14)

// === 信号 ===
long_signal  = dir > 0 and dir[1] < 0 and adx > 20
short_signal = dir < 0 and dir[1] > 0 and adx > 20

// === 入场 ===
if long_signal
    risk_amount = strategy.equity * 0.02  // 2% 风险
    sl_distance = 2 * atr_val
    qty = risk_amount / sl_distance
    strategy.entry("L", strategy.long, qty=qty)
    strategy.exit("L Exit", "L",
                  stop=close - sl_distance,
                  trail_points=sl_distance / syminfo.mintick,
                  trail_offset=sl_distance / syminfo.mintick / 2)

if short_signal
    risk_amount = strategy.equity * 0.02
    sl_distance = 2 * atr_val
    qty = risk_amount / sl_distance
    strategy.entry("S", strategy.short, qty=qty)
    strategy.exit("S Exit", "S",
                  stop=close + sl_distance,
                  trail_points=sl_distance / syminfo.mintick,
                  trail_offset=sl_distance / syminfo.mintick / 2)

// === 风控 ===
// 单日亏损超 3% → 停盘
if strategy.closedtrades.profit(strategy.closedtrades - 1) < -strategy.equity * 0.03
    strategy.close_all(comment="Daily Loss Limit")
```

---

## 10. 引用与延伸阅读

### 10.1 主要数据源

| 来源 | URL | 用途 |
|------|-----|------|
| TradingView Pine Script v5 User Manual - Strategies | https://www.tradingview.com/pine-script-docs/en/v5/concepts/strategies/ | **官方策略文档**（最权威） |
| TradingView Pine Script v5 Reference | https://www.tradingview.com/pine-script-reference/v5/ | API 完整签名 |
| PineCoders/pine-utils | https://github.com/pinecoders/pine-utils | 真实代码片段 |
| PineCoders Coding Conventions | https://github.com/pinecoders/pinecoders.github.io | 编码规范 |
| Investopedia: Mean Reversion | https://www.investopedia.com/terms/m/meanreversion.asp | 均值回归学术 |
| Investopedia: Backtesting | https://www.investopedia.com/terms/b/backtesting.asp | 回测基础 |
| Investopedia: Market Neutral | https://www.investopedia.com/terms/m/marketneutral.asp | 市场中性 |
| Wikipedia: Momentum (finance) | https://en.wikipedia.org/wiki/Momentum_(finance) | 动量策略 |
| Wikipedia: Mean Reversion | https://en.wikipedia.org/wiki/Mean_reversion_(finance) | 均值回归学术 |
| Wikipedia: Trend Following | https://en.wikipedia.org/wiki/Trend_following | 趋势跟随 |
| Wikipedia: Walk-forward optimization | https://en.wikipedia.org/wiki/Walk-forward_optimization | WFO |
| Wikipedia: Risk Management | https://en.wikipedia.org/wiki/Financial_risk_management | 风控基础 |

### 10.2 重要概念延伸

- **Walk-Forward Optimization (WFO)** —— 把数据分 in-sample + out-of-sample 滚动测试
- **Pyramiding** —— 同方向加仓
- **Bracket Order** —— 括号单（entry + SL + TP）
- **OCO** —— One-Cancels-Other（两个订单，一个成交另一个撤销）
- **Trailing Stop** —— 跟踪止损
- **Position Sizing** —— 仓位管理

### 10.3 相关内部文档

- [PineScript内置指标.md](../01-内置指标/PineScript内置指标.md) — Pine v5 `ta.*` 指标 API
- [TradingView社区指标.md](../02-社区指标/TradingView社区指标.md) — 头部社区作者
- [TradingView社区策略.md](../04-社区策略/TradingView社区策略.md) — 真实社区策略
- [01-技术分析/02-技术指标/技术指标深度解析.md](../../01-技术分析/02-技术指标/技术指标深度解析.md) — 25+ 指标原理
- [06-量化交易/02-策略开发/策略开发全流程与回测陷阱.md](../../06-量化交易/02-策略开发/策略开发全流程与回测陷阱.md) — 回测实战陷阱
- [06-量化交易/03-风险管理/风险管理系统.md](../../06-量化交易/03-风险管理/风险管理系统.md) — 仓位 + Kelly + VaR
- [03-市场机制/01-流动性/流动性猎杀机制.md](../../03-市场机制/01-流动性/流动性猎杀机制.md) — 加密流动性
- [07-机构策略/01-统计套利/统计套利策略.md](../../07-机构策略/01-统计套利/统计套利策略.md) — 配对/协整

### 10.4 关键提示

> 📌 **Pine v5 内置策略是入门到中级量化交易的最佳工具**。但请注意：
> 1. Pine 只能跑**单品种**策略（除非用 `request.security()` 跨品种）
> 2. **复杂 ML**（神经网络、深度学习）Pine 跑不了，需 Python
> 3. **真实下单**需要第三方桥接（如 PineConnector、AlgoTrader）
> 4. **生产级策略**用 Python / C++ / Rust 写，**不要**用 Pine 跑生产资金
>
> **Pine 适合**：
> - 学习交易逻辑
> - 快速验证想法
> - 5 分钟搭建原型
> - 个人小资金自动交易

_最后更新：2026-06-04（基于 50 个真实数据源 + TradingView 官方 v5 Manual + Wikipedia 策略概念整理）_
