# CCXT 与加密数据接口实战

> 文档版本: 2026-06（基于 OpenHands AI 知识库整理 + CCXT 官方文档交叉验证）
> 来源: CCXT 官方文档, Wikipedia "Cryptocurrency exchange", 各大交易所 API 文档

---

## 一、CCXT 基础

### 1. 什么是 CCXT

**CCXT**（CryptoCurrency eXchange Trading Library）：
- 一个统一的 JavaScript / Python / PHP 库
- 覆盖 **100+ 加密交易所**
- 统一的 API 接口
- MIT 开源许可

**支持交易所（部分）**：
- Binance, OKX, Bybit, Coinbase, Kraken, Bitfinex, Bitstamp
- Huobi, Gate.io, KuCoin, MEXC, Bitget
- DeFi：Uniswap, SushiSwap, dYdX, GMX（部分）

**GitHub 数据**（2024）：
- 30,000+ ⭐
- 累计 1,000,000+ 下载/月
- 持续活跃维护

### 2. 三大类接口

**1）公共接口（Public）**：
- 无需认证
- 行情数据：ticker, orderbook, OHLCV, trades

**2）私有接口（Private）**：
- 需要 API key/secret
- 账户操作：balance, orders, trades

**3）衍生品（Derivatives）**：
- 期货、期权、永续合约
- Funding Rate, mark price, OI

---

## 二、安装与初始化

### 1. 安装

```bash
pip install ccxt
# 或
uv add ccxt
```

### 2. 基础初始化

```python
import ccxt

# 1. 现货交易所
binance = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET',
    'enableRateLimit': True,
    'options': {'defaultType': 'spot'}
})

# 2. 永续合约
binance_swap = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET',
    'enableRateLimit': True,
    'options': {'defaultType': 'swap'}
})

# 3. 多个交易所
exchanges = {
    'binance': ccxt.binance({'enableRateLimit': True}),
    'okx': ccxt.okx({'enableRateLimit': True}),
    'bybit': ccxt.bybit({'enableRateLimit': True}),
}
```

---

## 三、公共 API 详解

### 1. 行情（Ticker）

```python
# 单个 ticker
ticker = binance.fetch_ticker('BTC/USDT')
print(f"BTC: ${ticker['last']}, 24h change: {ticker['percentage']}%")

# 多个 ticker
tickers = binance.fetch_tickers(['BTC/USDT', 'ETH/USDT', 'SOL/USDT'])
for symbol, ticker in tickers.items():
    print(f"{symbol}: ${ticker['last']}")
```

### 2. 订单簿（Order Book）

```python
# 完整订单簿
orderbook = binance.fetch_order_book('BTC/USDT', limit=20)

# 分析订单簿
bids = orderbook['bids']
asks = orderbook['asks']
spread = asks[0][0] - bids[0][0]
mid_price = (asks[0][0] + bids[0][0]) / 2
print(f"Spread: ${spread}, Mid: ${mid_price}")

# 深度分析
total_bid_volume = sum(b[1] for b in bids[:10])
total_ask_volume = sum(a[1] for a in asks[:10])
imbalance = (total_bid_volume - total_ask_volume) / (total_bid_volume + total_ask_volume)
print(f"Order Book Imbalance: {imbalance:.2%}")
```

### 3. K 线（OHLCV）

```python
import pandas as pd

# 获取 K 线
ohlcv = binance.fetch_ohlcv('BTC/USDT', '1d', limit=100)

# 转为 DataFrame
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
df = df.set_index('datetime')

# 各种时间框架
for tf in ['1m', '5m', '15m', '1h', '4h', '1d', '1w']:
    data = binance.fetch_ohlcv('BTC/USDT', tf, limit=100)
    print(f"{tf}: {len(data)} candles")
```

### 4. 成交（Trades）

```python
trades = binance.fetch_trades('BTC/USDT', limit=100)
buy_volume = sum(t['amount'] for t in trades if t['side'] == 'buy')
sell_volume = sum(t['amount'] for t in trades if t['side'] == 'sell')
buy_sell_ratio = buy_volume / sell_volume
print(f"Buy/Sell ratio: {buy_sell_ratio:.2f}")
```

### 5. 衍生品数据

```python
# Funding Rate
funding = binance.fetch_funding_rate('BTC/USDT:USDT')
print(f"Funding Rate: {funding['fundingRate']}")

# Open Interest
oi = binance.fetch_open_interest('BTC/USDT:USDT')
print(f"Open Interest: {oi['openInterestAmount']} BTC")

# 历史 Funding Rate
funding_history = binance.fetch_funding_rate_history('BTC/USDT:USDT', limit=100)
```

---

## 四、私有 API 详解

### 1. 账户余额

```python
balance = binance.fetch_balance()
print(f"Total USDT: {balance['USDT']['total']}")
print(f"Free USDT: {balance['USDT']['free']}")

# 多个币种
for currency in ['BTC', 'ETH', 'USDT']:
    if currency in balance:
        print(f"{currency}: {balance[currency]['total']}")
```

### 2. 下单

```python
# 1. 市价买单
order = binance.create_order(
    symbol='BTC/USDT',
    type='market',
    side='buy',
    amount=0.01
)

# 2. 限价卖单
order = binance.create_order(
    symbol='BTC/USDT',
    type='limit',
    side='sell',
    amount=0.01,
    price=70000
)

# 3. 止损单
order = binance.create_order(
    symbol='BTC/USDT',
    type='stop_market',
    side='sell',
    amount=0.01,
    params={'stopPrice': 65000}
)

# 4. 永续合约做空
order = binance_swap.create_order(
    symbol='BTC/USDT:USDT',
    type='market',
    side='sell',
    amount=0.01
)
```

### 3. 订单管理

```python
# 查询订单
order = binance.fetch_order('123456', 'BTC/USDT')

# 查询未完成订单
open_orders = binance.fetch_open_orders('BTC/USDT')

# 取消订单
binance.cancel_order('123456', 'BTC/USDT')

# 批量取消
binance.cancel_all_orders('BTC/USDT')
```

### 4. 持仓（合约）

```python
positions = binance_swap.fetch_positions()
for pos in positions:
    if float(pos['contracts']) > 0:
        print(f"{pos['symbol']}: {pos['side']} {pos['contracts']} @ {pos['entryPrice']}")
        print(f"  PnL: {pos['unrealizedPnl']}")
        print(f"  Liquidation: {pos['liquidationPrice']}")

# 设置杠杆
binance_swap.set_leverage(10, 'BTC/USDT:USDT')
```

---

## 五、错误处理与限速

### 1. 限速处理

**交易所限速**：
- Binance：1200 req/min
- OKX：20 req/sec
- Bybit：600 req/min
- Coinbase Pro：10 req/sec

**CCXT 内置限速**：
```python
binance = ccxt.binance({
    'enableRateLimit': True,
    'rateLimit': 100,  # ms between requests
})
```

### 2. 异常处理

```python
from ccxt.base.errors import (
    NetworkError, ExchangeError, AuthenticationError,
    RateLimitExceeded, InvalidOrder, InsufficientFunds, OrderNotFound
)

try:
    order = binance.create_order(
        symbol='BTC/USDT', type='limit', side='buy',
        amount=0.01, price=68000
    )
except RateLimitExceeded:
    print("Rate limit hit, waiting...")
    time.sleep(60)
except InsufficientFunds:
    print("Insufficient balance")
except InvalidOrder as e:
    print(f"Invalid order: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
except ExchangeError as e:
    print(f"Exchange error: {e}")
```

### 3. 重试机制

```python
import tenacity

@tenacity.retry(
    wait=tenacity.wait_exponential(min=1, max=60),
    stop=tenacity.stop_after_attempt(5),
    retry=tenacity.retry_if_exception_type(NetworkError)
)
def fetch_with_retry(exchange, symbol):
    return exchange.fetch_ticker(symbol)
```

---

## 六、异步与并发

### 1. 异步版本

```python
import ccxt.pro as ccxtpro
import asyncio

async def main():
    binance = ccxtpro.binance({'enableRateLimit': True})
    okx = ccxtpro.okx({'enableRateLimit': True})
    
    btc_binance, btc_okx = await asyncio.gather(
        binance.fetch_ticker('BTC/USDT'),
        okx.fetch_ticker('BTC/USDT')
    )
    
    print(f"Binance BTC: ${btc_binance['last']}")
    print(f"OKX BTC: ${btc_okx['last']}")
    
    await binance.close()
    await okx.close()

asyncio.run(main())
```

### 2. WebSocket 实时数据

```python
import ccxt.pro as ccxtpro
import asyncio

async def watch_orderbook():
    binance = ccxtpro.binance({'enableRateLimit': True})
    
    while True:
        orderbook = await binance.watch_order_book('BTC/USDT', limit=20)
        best_bid = orderbook['bids'][0]
        best_ask = orderbook['asks'][0]
        print(f"Bid: {best_bid[0]} x {best_bid[1]}, Ask: {best_ask[0]} x {best_ask[1]}")

asyncio.run(watch_orderbook())
```

### 3. 批量并发

```python
async def fetch_all_tickers(exchanges_config, symbols):
    """并发获取所有交易所的所有交易对"""
    exchanges = [getattr(ccxtpro, name)({'enableRateLimit': True}) 
                for name in exchanges_config]
    
    tasks = []
    for ex in exchanges:
        for sym in symbols:
            tasks.append(ex.fetch_ticker(sym))
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    await asyncio.gather(*[ex.close() for ex in exchanges])
    
    return results
```

---

## 七、链上数据获取

### 1. Etherscan API

```python
import requests

def get_eth_balance(address, api_key):
    url = "https://api.etherscan.io/api"
    params = {
        'module': 'account',
        'action': 'balance',
        'address': address,
        'tag': 'latest',
        'apikey': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    return int(data['result']) / 1e18  # wei to ETH

balance = get_eth_balance('0x...', 'YOUR_ETHERSCAN_API_KEY')
print(f"Balance: {balance} ETH")
```

### 2. 通过 The Graph

```python
import requests

def query_uniswap_v3():
    """查询 Uniswap V3 子图"""
    query = """
    {
      pools(first: 5, orderBy: totalValueLockedUSD, orderDirection: desc) {
        id
        token0 { symbol }
        token1 { symbol }
        totalValueLockedUSD
        volumeUSD
      }
    }
    """
    response = requests.post(
        'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3',
        json={'query': query}
    )
    return response.json()['data']['pools']

pools = query_uniswap_v3()
for pool in pools:
    print(f"{pool['token0']['symbol']}/{pool['token1']['symbol']}: TVL ${float(pool['totalValueLockedUSD']):,.0f}")
```

### 3. 链上数据服务

**Glassnode API**：
```python
import requests
import time

api_key = 'YOUR_GLASSNODE_API_KEY'

url = "https://api.glassnode.com/v1/metrics/market/mvrv"
params = {
    'a': 'BTC',
    'api_key': api_key,
    's': int(time.time()) - 86400 * 365,
    'u': int(time.time()),
    'i': '24h'
}
response = requests.get(url, params=params)
data = response.json()
latest_mvrv = data[-1]['v']
print(f"Current BTC MVRV: {latest_mvrv}")
```

---

## 八、数据库存储

### 1. 时序数据库

**TimescaleDB**：
```python
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:pass@localhost:5432/crypto')
df.to_sql('ohlcv_btc', engine, if_exists='append', index=True)

query = "SELECT * FROM ohlcv_btc WHERE time > NOW() - INTERVAL '30 days'"
df = pd.read_sql(query, engine)
```

### 2. 文件存储

**Parquet**：
```python
import pandas as pd

df.to_parquet('btc_ohlcv_2024.parquet', compression='snappy')
df = pd.read_parquet('btc_ohlcv_2024.parquet')
```

---

## 九、CCXT Pro 与 WebSocket

### 1. WebSocket 订阅

```python
import ccxt.pro as ccxtpro
import asyncio

async def watch_multiple():
    binance = ccxtpro.binance({'enableRateLimit': True})
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    
    while True:
        for symbol in symbols:
            try:
                ticker = await binance.watch_ticker(symbol)
                print(f"{symbol}: ${ticker['last']}")
            except Exception as e:
                print(f"Error: {e}")

asyncio.run(watch_multiple())
```

### 2. 实时订单簿变化

```python
async def detect_large_orders():
    binance = ccxtpro.binance({'enableRateLimit': True})
    
    while True:
        ob = await binance.watch_order_book('BTC/USDT', limit=100)
        large_bids = [b for b in ob['bids'] if b[1] > 10]
        large_asks = [a for a in ob['asks'] if a[1] > 10]
        if large_bids or large_asks:
            print(f"Large orders: {len(large_bids)} bids, {len(large_asks)} asks")
```

---

## 十、其他关键库

### 1. TA-Lib（技术指标）

```python
import talib
import numpy as np

close_prices = df['close'].values
rsi = talib.RSI(close_prices, timeperiod=14)

macd, signal, hist = talib.MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)

upper, middle, lower = talib.BBANDS(close_prices, timeperiod=20, nbdevup=2, nbdevdn=2)
```

### 2. pandas-ta

```python
import pandas_ta as ta

df['RSI_14'] = ta.rsi(df['close'], length=14)
df['EMA_20'] = ta.ema(df['close'], length=20)
df['MACD'] = ta.macd(df['close'])['MACD_12_26_9']
```

### 3. Freqtrade（完整交易框架）

```bash
pip install freqtrade
```

**策略示例**：
```python
from freqtrade.strategy import IStrategy
import talib.abstract as ta

class SimpleMaStrategy(IStrategy):
    INTERFACE_VERSION = 3
    
    def populate_indicators(self, dataframe, metadata):
        dataframe['ema_short'] = ta.EMA(dataframe, timeperiod=10)
        dataframe['ema_long'] = ta.EMA(dataframe, timeperiod=50)
        return dataframe
    
    def populate_entry_trend(self, dataframe, metadata):
        dataframe.loc[
            (dataframe['ema_short'] > dataframe['ema_long']) &
            (dataframe['volume'] > 0),
            'enter_long'] = 1
        return dataframe
    
    def populate_exit_trend(self, dataframe, metadata):
        dataframe.loc[
            (dataframe['ema_short'] < dataframe['ema_long']),
            'exit_long'] = 1
        return dataframe
```

### 4. Jesse（加密专用框架）

```bash
pip install jesse
```

---

## 十一、数据质量与陷阱

### 1. 常见数据问题

1. **缺失值**：交易所 API 故障
2. **异常值**：合约标记错误、极端行情
3. **时间戳**：UTC vs 本地时间
4. **重复值**：API 分页
5. **停牌/下架**：停止交易的币种

### 2. 数据验证

```python
def validate_ohlcv(df):
    """验证 OHLCV 数据"""
    # 价格关系
    assert (df['high'] >= df['low']).all()
    assert (df['high'] >= df['open']).all()
    assert (df['high'] >= df['close']).all()
    assert (df['low'] <= df['open']).all()
    assert (df['low'] <= df['close']).all()
    
    # 成交量
    assert (df['volume'] >= 0).all()
    
    # 时间连续
    time_diff = df.index.to_series().diff()
    expected_diff = pd.Timedelta(minutes=1)
    gaps = time_diff[time_diff > expected_diff * 1.5]
    if len(gaps) > 0:
        print(f"Warning: {len(gaps)} time gaps")
    
    return True
```

### 3. 数据清洗

```python
def clean_ohlcv(df):
    """清洗 OHLCV 数据"""
    df = df[~df.index.duplicated(keep='first')]
    df = df.sort_index()
    df = df.fillna(method='ffill')
    df = df[df['volume'] > 0]
    df.index = df.index.tz_localize('UTC')
    return df
```

---

## 十二、关键数据点

| # | 数据 | 来源 |
|---|------|------|
| 1 | 100+ | CCXT 支持的交易所数 |
| 2 | 30,000+ | CCXT GitHub Stars |
| 3 | 1,000,000+ | CCXT 月下载量 |
| 4 | 1200 req/min | Binance API 限速 |
| 5 | 20 req/sec | OKX API 限速 |
| 6 | 600 req/min | Bybit API 限速 |
| 7 | 10 req/sec | Coinbase Pro API 限速 |
| 8 | 100+ | CCXT 支持的衍生品类型 |
| 9 | 50+ | CCXT 支持的订单类型 |
| 10 | 100+ | TA-Lib 技术指标数 |
| 11 | 130+ | pandas-ta 指标数 |
| 12 | 10+ | CCXT Pro 异步订阅类型 |
| 13 | 1M+ | Freqtrade 用户数 |
| 14 | 5+ | 主流 Python 量化框架 |
| 15 | 100ms | 典型 API 响应时间 |

---

## 📚 引用来源

1. CCXT 官方文档: https://docs.ccxt.com/
2. CCXT GitHub: https://github.com/ccxt/ccxt
3. CCXT Pro: https://github.com/ccxt/ccxt/tree/master/pro
4. Wikipedia — Cryptocurrency exchange: https://en.wikipedia.org/wiki/Cryptocurrency_exchange
5. Binance API 文档: https://binance-docs.github.io/apidocs/
6. OKX API 文档: https://www.okx.com/docs-v5/
7. Bybit API 文档: https://bybit-exchange.github.io/docs/
8. TA-Lib: https://ta-lib.org/
9. pandas-ta: https://github.com/twopirllc/pandas-ta
10. Freqtrade: https://www.freqtrade.io/
11. Jesse: https://jesse.trade/
12. Etherscan API: https://docs.etherscan.io/
13. The Graph: https://thegraph.com/
14. Glassnode API: https://docs.glassnode.com/

---

**免责声明**：本文为研究性资料整理，不构成投资建议。交易涉及重大风险，请使用模拟盘充分测试后再实盘。
