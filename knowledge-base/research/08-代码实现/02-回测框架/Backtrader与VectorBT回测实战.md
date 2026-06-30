# Backtrader 与 VectorBT 回测实战

> 文档版本: 2026-06（基于 OpenHands AI 知识库整理 + 框架官方文档交叉验证）
> 来源: Backtrader, VectorBT, Zipline, QuantConnect Lean 官方文档, Wikipedia "Backtesting"

---

## 一、回测框架选择

### 1. 主流框架对比

| 框架 | 类型 | 性能 | 加密支持 | 学习曲线 |
|------|------|------|----------|----------|
| **Backtrader** | 事件驱动 | 中 | 通过 CCXT 适配 | 中 |
| **VectorBT** | 向量化 | 极快 | 自定义数据 | 中 |
| **Zipline** | 事件驱动 | 中 | 主要股票 | 中高 |
| **QuantConnect Lean** | 事件驱动 | 快 | 多资产 | 高 |
| **Jesse** | 事件驱动 | 快 | 加密原生 | 中 |
| **Freqtrade** | 事件驱动 | 中 | 加密原生 | 中 |
| **Backtesting.py** | 向量化 | 快 | 通用 | 低 |

### 2. 选择建议

**初学者**：
- Backtesting.py：API 简单
- Freqtrade：加密专精、文档好

**中级**：
- Backtrader：经典、文档多
- VectorBT：快速实验

**高级**：
- QuantConnect Lean：云端、丰富数据
- 自建：Python + 性能库

---

## 二、Backtrader 实战

### 1. 安装与基础

```bash
pip install backtrader
# 或
uv add backtrader
```

### 2. 第一个策略

```python
import backtrader as bt

# 1. 创建 Cerebro 引擎
cerebro = bt.Cerebro()

# 2. 添加数据
data = bt.feeds.GenericCSVData(
    dataname='btc_usdt_daily.csv',
    dtformat=('%Y-%m-%d'),
    datetime=0, open=1, high=2, low=3, close=4, volume=5, openinterest=-1
)
cerebro.adddata(data)

# 3. 添加策略
class SmaCross(bt.Strategy):
    params = (
        ('fast', 10),
        ('slow', 30),
    )
    
    def __init__(self):
        self.fast_ma = bt.indicators.SMA(period=self.p.fast)
        self.slow_ma = bt.indicators.SMA(period=self.p.slow)
        self.crossover = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)
    
    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        else:
            if self.crossover < 0:
                self.sell()

cerebro.addstrategy(SmaCross)

# 4. 设置初始资金和佣金
cerebro.broker.setcash(100000.0)
cerebro.broker.setcommission(commission=0.001)  # 0.1%

# 5. 运行回测
print(f"初始资金: {cerebro.broker.getvalue():.2f}")
cerebro.run()
print(f"最终资金: {cerebro.broker.getvalue():.2f}")

# 6. 绘制结果
cerebro.plot()
```

### 3. 完整加密回测

```python
import backtrader as bt
import pandas as pd
import ccxt

# 1. 从 CCXT 获取数据
def fetch_data(symbol='BTC/USDT', timeframe='1d', limit=1000):
    exchange = ccxt.binance({'enableRateLimit': True})
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df = df.set_index('datetime')
    df.to_csv(f'{symbol.replace("/", "_")}_{timeframe}.csv')
    return df

# 2. 加密策略
class CryptoStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),
        ('rsi_oversold', 30),
        ('rsi_overbought', 70),
        ('position_size', 0.95),  # 95% 仓位
    )
    
    def __init__(self):
        self.rsi = bt.indicators.RSI(period=self.p.rsi_period)
        self.order = None
    
    def next(self):
        if self.order:
            return
        
        if not self.position:
            # 买入信号：RSI 超卖
            if self.rsi < self.p.rsi_oversold:
                size = (self.broker.getcash() * self.p.position_size) // self.data.close[0]
                self.order = self.buy(size=size)
        else:
            # 卖出信号：RSI 超买
            if self.rsi > self.p.rsi_overbought:
                self.order = self.sell(size=self.position.size)
    
    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                print(f"买入: {order.executed.price} @ {bt.num2date(order.executed.dt)}")
            else:
                print(f"卖出: {order.executed.price} @ {bt.num2date(order.executed.dt)}")
        self.order = None

# 3. 运行
cerebro = bt.Cerebro()
data = bt.feeds.GenericCSVData(
    dataname='BTC_USDT_1d.csv',
    dtformat='%Y-%m-%d %H:%M:%S',
    datetime=0, open=1, high=2, low=3, close=4, volume=5, openinterest=-1
)
cerebro.adddata(data)
cerebro.addstrategy(CryptoStrategy)
cerebro.broker.setcash(100000.0)
cerebro.broker.setcommission(commission=0.001)
cerebro.run()
cerebro.plot()
```

### 4. 多个数据源

```python
# 多币种组合回测
cerebro = bt.Cerebro()

# 添加 BTC
data_btc = bt.feeds.GenericCSVData(dataname='btc.csv', ...)
cerebro.adddata(data_btc, name='BTC')

# 添加 ETH
data_eth = bt.feeds.GenericCSVData(dataname='eth.csv', ...)
cerebro.adddata(data_eth, name='ETH')

# 添加 SOL
data_sol = bt.feeds.GenericCSVData(dataname='sol.csv', ...)
cerebro.adddata(data_sol, name='SOL')

class MultiAssetStrategy(bt.Strategy):
    def next(self):
        for d in self.datas:
            pos = self.getposition(d)
            if not pos:
                # 简单动量信号
                if d.close[0] > d.close[-5]:
                    self.buy(data=d, size=10)
            else:
                if d.close[0] < d.close[-5]:
                    self.sell(data=d, size=10)

cerebro.addstrategy(MultiAssetStrategy)
cerebro.run()
```

### 5. 性能分析

```python
# 添加分析器
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')

results = cerebro.run()
strat = results[0]

print(f"Sharpe Ratio: {strat.analyzers.sharpe.get_analysis()['sharperatio']:.2f}")
print(f"Max Drawdown: {strat.analyzers.drawdown.get_analysis()['max']['drawdown']:.2f}%")
print(f"Total Return: {strat.analyzers.returns.get_analysis()['rtot']:.2f}%")

# 交易分析
trades = strat.analyzers.trades.get_analysis()
print(f"Total Trades: {trades.total.total}")
print(f"Win Rate: {trades.won.total / trades.total.total * 100:.1f}%")
```

### 6. 优化参数

```python
cerebro = bt.Cerebro()

# 参数优化
cerebro.optstrategy(
    SmaCross,
    fast=range(5, 30, 5),
    slow=range(20, 100, 10)
)

# 多进程加速
cerebro.optstrategy(SmaCross, fast=range(5, 30, 5), slow=range(20, 100, 10))

# 运行优化
results = cerebro.run(maxcpus=4)

# 找最佳
best_sharpe = -float('inf')
best_params = None
for run in results:
    sharpe = run[0].analyzers.sharpe.get_analysis()['sharperatio']
    if sharpe and sharpe > best_sharpe:
        best_sharpe = sharpe
        best_params = (run[0].params.fast, run[0].params.slow)

print(f"Best Params: fast={best_params[0]}, slow={best_params[1]}")
print(f"Best Sharpe: {best_sharpe:.2f}")
```

---

## 三、VectorBT 实战

### 1. 安装与基础

```bash
pip install vectorbt
```

### 2. 基础回测

```python
import vectorbt as vbt
import pandas as pd
import numpy as np

# 1. 获取数据
data = vbt.BinanceData.download('BTCUSDT', interval='1d', start='2020-01-01')
print(data.shape)
print(data.head())

# 2. 计算指标
close = data.get('Close')

# 3. 简单 SMA 策略
fast_ma = vbt.MA.run(close, 10)
slow_ma = vbt.MA.run(close, 30)

# 4. 生成信号
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

# 5. 回测
pf = vbt.Portfolio.from_signals(
    close, entries, exits,
    init_cash=10000,
    fees=0.001  # 0.1%
)

# 6. 结果
print(f"总收益: {pf.total_return():.2%}")
print(f"Sharpe: {pf.sharpe_ratio():.2f}")
print(f"Max DD: {pf.max_drawdown():.2%}")
```

### 3. 完整策略

```python
import vectorbt as vbt
import pandas as pd
import numpy as np

# 1. 数据
data = vbt.BinanceData.download('BTCUSDT', interval='4h', start='2021-01-01')
close = data.get('Close')

# 2. 多因子
# 因子 1: RSI
rsi = vbt.RSI.run(close, 14)

# 因子 2: 布林带
bb = vbt.BBANDS.run(close, 20, 2)

# 因子 3: ATR (波动率)
atr = vbt.ATR.run(data.get('High'), data.get('Low'), close, 14)

# 3. 信号合成
entries = (rsi.rsi < 30) & (close < bb.lower)
exits = (rsi.rsi > 70) | (close > bb.upper)

# 4. 回测
pf = vbt.Portfolio.from_signals(
    close, entries, exits,
    init_cash=10000,
    fees=0.001,
    sl_stop=0.05,  # 5% 止损
    tp_stop=0.15,  # 15% 止盈
)

# 5. 性能
stats = pf.stats()
print(stats)
```

### 4. 参数优化

```python
# 多参数优化
fast_ma = vbt.MA.run(close, [5, 10, 15, 20, 25, 30], short_name='fast')
slow_ma = vbt.MA.run(close, [20, 30, 40, 50, 60, 70], short_name='slow')

# 生成所有参数组合
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

# 回测所有参数组合
pf = vbt.Portfolio.from_signals(
    close, entries, exits,
    init_cash=10000,
    fees=0.001
)

# 找最佳参数
sharpe = pf.sharpe_ratio()
best_idx = sharpe.idxmax()
print(f"Best params: {best_idx}")
print(f"Best Sharpe: {sharpe[best_idx]:.2f}")

# 绘制热力图
sharpe.vbt.heatmap().show()
```

### 5. 投资组合回测

```python
# 多币种
symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT']
prices = pd.DataFrame()

for symbol in symbols:
    data = vbt.BinanceData.download(symbol, interval='1d', start='2022-01-01')
    prices[symbol] = data.get('Close')

# 计算动量
momentum = prices.pct_change(20)

# 选 Top 2
top_2 = momentum.rank(axis=1, ascending=False) <= 2

# 等权分配
weights = top_2.div(top_2.sum(axis=1), axis=0).fillna(0)

# 投资组合
pf = vbt.Portfolio.from_orders(
    prices, weights * 10000,  # 总资金 10000
    init_cash=10000,
    fees=0.001
)

print(pf.total_return())
print(pf.sharpe_ratio())
```

### 6. 加密专属数据源

```python
# VectorBT 内置加密数据
data = vbt.BinanceData.download(
    'BTCUSDT',
    interval='1d',
    start='2020-01-01',
    end='2024-01-01'
)

# 自定义数据源
def custom_loader(symbol, start, end):
    exchange = ccxt.binance({'enableRateLimit': True})
    ohlcv = exchange.fetch_ohlcv(symbol, '1d', since=...)
    df = pd.DataFrame(ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df = df.set_index('datetime')
    return df
```

---

## 四、其他回测框架

### 1. Zipline

```bash
pip install zipline-reloaded
```

```python
from zipline.api import order, symbol, record
from zipline import run_algorithm
import pandas as pd

def initialize(context):
    context.asset = symbol('BTC')

def handle_data(context, data):
    short_mavg = data.history(context.asset, 'price', bar_count=10, frequency='1d').mean()
    long_mavg = data.history(context.asset, 'price', bar_count=30, frequency='1d').mean()
    
    if short_mavg > long_mavg:
        order_target_percent(context.asset, 1.0)
    else:
        order_target_percent(context.asset, 0.0)

# 运行
start = pd.Timestamp('2020-01-01')
end = pd.Timestamp('2024-01-01')
result = run_algorithm(
    start=start, end=end,
    initialize=initialize,
    handle_data=handle_data,
    capital_base=10000,
)
```

### 2. Backtesting.py

```python
# pip install backtesting
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

class SmaCross(Strategy):
    n1 = 10
    n2 = 20
    
    def init(self):
        self.sma1 = self.I(lambda x: pd.Series(x).rolling(self.n1).mean(), self.data.Close)
        self.sma2 = self.I(lambda x: pd.Series(x).rolling(self.n2).mean(), self.data.Close)
    
    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()

# 加载数据
data = pd.read_csv('btc.csv', parse_dates=['datetime'], index_col='datetime')
data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

# 回测
bt = Backtest(data, SmaCross, cash=10000, commission=0.001)
stats = bt.run()
print(stats)
bt.plot()
```

### 3. Freqtrade

```python
# 完整策略框架
class MyStrategy(IStrategy):
    INTERFACE_VERSION = 3
    
    # 最小 ROI
    minimal_roi = {"0": 0.1}
    
    # 止损
    stoploss = -0.05
    
    # 时间框架
    timeframe = '5m'
    
    def populate_indicators(self, dataframe, metadata):
        dataframe['rsi'] = ta.RSI(dataframe)
        dataframe['ema'] = ta.EMA(dataframe, timeperiod=20)
        return dataframe
    
    def populate_entry_trend(self, dataframe, metadata):
        dataframe.loc[
            (dataframe['rsi'] < 30) & 
            (dataframe['close'] > dataframe['ema']),
            'enter_long'] = 1
        return dataframe
    
    def populate_exit_trend(self, dataframe, metadata):
        dataframe.loc[
            (dataframe['rsi'] > 70),
            'exit_long'] = 1
        return dataframe
```

---

## 五、回测陷阱与防御

### 1. 未来数据

**症状**：回测 Sharpe 异常高，实盘崩

**防御**：
```python
# 错误用法：用今日收盘价做今日决策
def wrong_strategy(data):
    if data.close > data.sma:
        return 1  # 错误：使用了未来数据
    
# 正确用法：T+1 执行
def correct_strategy(data):
    if data.close.shift(1) > data.sma.shift(1):  # 使用昨日数据
        return 1
```

### 2. 过拟合

**防御**：
- 样本量 > 参数数 × 100
- Walk-Forward 验证
- 简化参数

### 3. 生存者偏差

**防御**：
- 用历史全量数据
- 包含已下架币种

### 4. 交易摩擦

**防御**：
```python
# Backtrader 设置
cerebro.broker.setcommission(
    commission=0.001,  # 0.1% 手续费
    margin=0.1,  # 10% 保证金
    leverage=3  # 3x 杠杆
)
cerebro.broker.set_slippage_perc(0.0005)  # 0.05% 滑点
```

### 5. 冲击成本

**防御**：
- 限制仓位（不超过日交易量 1%）
- 用 TWAP/VWAP 模拟

### 6. 资金费率

**永续合约额外成本**：
```python
# 模拟 funding cost
def apply_funding(equity_curve, funding_rate=0.0001):
    # 假设每天 3 次 funding (8h 一次)
    n_periods = len(equity_curve) // 3
    for i in range(n_periods):
        equity_curve.iloc[i*3] -= funding_rate * equity_curve.iloc[i*3]
    return equity_curve
```

---

## 六、性能评估

### 1. 关键指标

**收益指标**：
- 总收益（Total Return）
- 年化收益（CAGR）
- 月度收益

**风险指标**：
- 年化波动率
- 最大回撤
- 下行波动率

**风险调整收益**：
- Sharpe Ratio
- Sortino Ratio
- Calmar Ratio

**交易指标**：
- 胜率（Win Rate）
- 盈亏比（Avg Win/Avg Loss）
- Profit Factor
- 持仓时间

### 2. 评估代码

```python
def evaluate_strategy(equity_curve, trades_df):
    """综合评估策略"""
    
    # 收益指标
    total_return = (equity_curve.iloc[-1] / equity_curve.iloc[0]) - 1
    n_years = (equity_curve.index[-1] - equity_curve.index[0]).days / 365
    cagr = (1 + total_return) ** (1 / n_years) - 1
    
    # 风险指标
    daily_returns = equity_curve.pct_change().dropna()
    volatility = daily_returns.std() * np.sqrt(252)
    cumulative_max = equity_curve.cummax()
    drawdown = (equity_curve - cumulative_max) / cumulative_max
    max_drawdown = drawdown.min()
    
    # 风险调整
    sharpe = cagr / volatility if volatility > 0 else 0
    downside_returns = daily_returns[daily_returns < 0]
    sortino = cagr / (downside_returns.std() * np.sqrt(252)) if len(downside_returns) > 0 else 0
    calmar = cagr / abs(max_drawdown) if max_drawdown != 0 else 0
    
    # 交易指标
    n_trades = len(trades_df)
    win_rate = (trades_df['pnl'] > 0).mean() if n_trades > 0 else 0
    avg_win = trades_df[trades_df['pnl'] > 0]['pnl'].mean() if n_trades > 0 else 0
    avg_loss = abs(trades_df[trades_df['pnl'] < 0]['pnl'].mean()) if n_trades > 0 else 0
    profit_factor = avg_win / avg_loss if avg_loss > 0 else 0
    
    return {
        'total_return': total_return,
        'cagr': cagr,
        'volatility': volatility,
        'max_drawdown': max_drawdown,
        'sharpe': sharpe,
        'sortino': sortino,
        'calmar': calmar,
        'n_trades': n_trades,
        'win_rate': win_rate,
        'profit_factor': profit_factor,
    }

# 使用
equity = pf.value()  # 投资组合价值曲线
trades = pf.trades.records_readable  # 交易记录
stats = evaluate_strategy(equity, trades)
for k, v in stats.items():
    print(f"{k}: {v:.4f}")
```

### 3. 基准对比

```python
# 买入持有 BTC 基准
btc_data = pd.read_csv('btc.csv', parse_dates=['datetime'], index_col='datetime')
btc_return = (btc_data['close'].iloc[-1] / btc_data['close'].iloc[0]) - 1

strategy_return = (pf.value().iloc[-1] / pf.value().iloc[0]) - 1
alpha = strategy_return - btc_return

print(f"Strategy: {strategy_return:.2%}")
print(f"BTC HODL: {btc_return:.2%}")
print(f"Alpha: {alpha:.2%}")
```

---

## 七、关键数据点

| # | 数据 | 来源 |
|---|------|------|
| 1 | 100x | VectorBT vs Backtrader 性能差异 |
| 2 | 0.001 | 默认加密手续费率 |
| 3 | 0.0005 | 默认滑点 |
| 4 | 1.5+ | 合格 Sharpe |
| 5 | 2.0+ | 优秀 Sharpe |
| 6 | < 20% | 良好 Max DD |
| 7 | 100x | 样本/参数最小比 |
| 8 | 0.1% | 永续 funding 阈值 |
| 9 | 0.01 | 最小下单量（BTC） |
| 10 | 30+ | Backtrader 内置指标 |
| 11 | 100+ | VectorBT 性能 vs Backtrader |
| 12 | 5+ | 主流回测框架 |
| 13 | 3x | 默认杠杆 |
| 14 | 0.0001 | 0.01% 滑点（深度好时） |
| 15 | 1% | 单资产日交易量占比上限 |

---

## 📚 引用来源

1. Backtrader 文档: https://www.backtrader.com/docu/
2. VectorBT 文档: https://vectorbt.dev/
3. Zipline-reloaded: https://zipline.ml4trading.io/
4. QuantConnect Lean: https://www.quantconnect.com/docs
5. Backtesting.py: https://kernc.github.io/backtesting.py/
6. Freqtrade: https://www.freqtrade.io/
7. Jesse: https://jesse.trade/
8. Wikipedia — Backtesting: https://en.wikipedia.org/wiki/Backtesting
9. CCXT: https://docs.ccxt.com/
10. Chan, E. (2017). *Quantitative Trading* (2nd ed.). Wiley.
11. Lopez de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley.

---

**免责声明**：本文为研究性资料整理，不构成投资建议。回测结果不代表未来实盘表现，请使用模拟盘充分测试后再实盘。
