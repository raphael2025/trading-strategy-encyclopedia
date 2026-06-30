# 币安合约交易核心逻辑

> 东京节点必须掌握的交易知识

---

## 📊 合约基础

### 保证金模式

```
全仓保证金 (Cross)：所有仓位共享保证金
逐仓保证金 (Isolated)：每个仓位独立保证金

默认：逐仓（更安全）
```

### 杠杆

```
币安合约：1x - 125x
我们使用：10x

风险计算：
- 10x 杠杆 = 价格反向波动 10% 爆仓
- 止损设置：-5%（亏损保证金的 50%）
```

---

## 🎯 关键 API 端点

### 1. 开仓（做多）

```bash
POST /fapi/v1/order

参数：
- symbol: "BTCUSDT"
- side: "BUY"        # 做多=BUY，做空=SELL
- positionSide: "BOTH"  # 双向持仓
- type: "LIMIT"       # LIMIT 或 MARKET
- quantity: "0.001"   # 交易数量（BTC 数量）
- price: "65000"      # 限价单价格（市价单不需要）
- timeInForce: "GTC"  # Good Till Cancel
- timestamp: 1234567890000
- signature: <HMAC-SHA256>
```

### 2. 开仓（做空）

```bash
POST /fapi/v1/order

参数：
- symbol: "BTCUSDT"
- side: "SELL"        # 做空=SELL
- positionSide: "BOTH"
- type: "MARKET"
- quantity: "0.001"
```

### 3. 平仓

```bash
# 多头平仓 = 卖出相同数量
POST /fapi/v1/order
{
  "symbol": "BTCUSDT",
  "side": "SELL",
  "positionSide": "BOTH",
  "type": "MARKET",
  "quantity": "0.001",
  "reduceOnly": "true"  # 只减仓，不开新仓
}

# 空头平仓 = 买入相同数量
POST /fapi/v1/order
{
  "symbol": "BTCUSDT",
  "side": "BUY",
  "positionSide": "BOTH",
  "type": "MARKET",
  "quantity": "0.001",
  "reduceOnly": "true"
}
```

### 4. 设置止损止盈

```bash
# 止损单（STOP_MARKET）
POST /fapi/v1/order
{
  "symbol": "BTCUSDT",
  "side": "SELL",      # 多头止损=SELL
  "positionSide": "BOTH",
  "type": "STOP_MARKET",
  "quantity": "0.001",
  "stopPrice": "64000",  # 触发价格
  "reduceOnly": "true"
}

# 止盈单（TAKE_PROFIT_MARKET）
POST /fapi/v1/order
{
  "symbol": "BTCUSDT",
  "side": "SELL",      # 多头止盈=SELL
  "positionSide": "BOTH",
  "type": "TAKE_PROFIT_MARKET",
  "quantity": "0.001",
  "stopPrice": "68000",  # 触发价格
  "reduceOnly": "true"
}
```

---

## 📐 仓位计算

### 开仓数量计算

```bash
# 已知条件
本金：10000 USDT
仓位：20% = 2000 USDT
杠杆：10x
实际仓位：20000 USDT
BTC 价格：65000

# 计算 BTC 数量
BTC 数量 = 实际仓位 / BTC 价格
BTC 数量 = 20000 / 65000 = 0.307 BTC

# 验证
0.307 BTC × 65000 = 20000 USDT ✓
```

### 强平价格计算

```bash
# 多头强平价格
强平价 = 入场价 × (1 - 1/杠杆 + 手续费率)
强平价 = 65000 × (1 - 1/10 + 0.0005)
强平价 = 65000 × 0.9005 = 58532

# 空头强平价格
强平价 = 入场价 × (1 + 1/杠杆 - 手续费率)
强平价 = 65000 × (1 + 1/10 - 0.0005)
强平价 = 65000 × 1.0995 = 71467
```

### 盈亏计算

```bash
# 多头盈亏
盈亏 USDT = (卖出价 - 买入价) × 数量
盈亏% = (卖出价 - 买入价) / 买入价 × 杠杆

示例：
买入：65000，卖出：66000，数量：0.307 BTC
盈亏 USDT = (66000 - 65000) × 0.307 = 307 USDT
盈亏% = (66000 - 65000) / 65000 × 10 = 15.4%

# 空头盈亏
盈亏 USDT = (卖出价 - 买入价) × 数量
（注意：空头是高价卖出，低价买回）

示例：
卖出：65000，买回：64000，数量：0.307 BTC
盈亏 USDT = (65000 - 64000) × 0.307 = 307 USDT
```

---

## ⚠️ 风险控制

### 止损设置原则

```bash
# 多头止损
止损价 = 支撑位下方 2-3%
或
止损价 = 形态失败点（如颈线突破）

# 空头止损
止损价 = 阻力位上方 2-3%
或
止损价 = 形态失败点

# 止损金额
止损亏损 = 仓位 × (入场价 - 止损价) / 入场价 × 杠杆

示例：
仓位：20000 USDT（2000 × 10x）
入场：65000，止损：64000（-1.5%）
止损亏损 = 20000 × (65000-64000)/65000 × 10
止损亏损 = 20000 × 0.0154 × 10 = 308 USDT
```

### 止盈设置原则

```bash
# 第一目标：阻力位
# 第二目标：形态目标（如头肩顶的颈线距离）
# 第三目标：延伸位（1.618 倍）

# 盈亏比计算
盈亏比 = 止盈金额 / 止损金额
要求：> 1.5:1 才交易
```

---

## 📋 完整交易流程

### 1. 分析市场

```bash
1. 识别形态（头肩顶、双底等）
2. 识别支撑位和阻力位
3. 确定交易方向（多/空）
```

### 2. 计算仓位

```bash
1. 确定入场价
2. 确定止损价（支撑下方 2-3%）
3. 确定止盈价（阻力位或形态目标）
4. 计算盈亏比
5. 如果盈亏比 > 1.5:1，继续
```

### 3. 开仓

```bash
1. 设置杠杆（10x）
2. 计算开仓数量
3. 下市价单或限价单
4. 记录开仓价格
```

### 4. 设置止损止盈

```bash
1. 立即设置止损单（STOP_MARKET）
2. 设置止盈单（TAKE_PROFIT_MARKET）
3. 验证止损止盈价格正确
```

### 5. 监控仓位

```bash
1. 每 30 分钟检查一次
2. 如果价格接近止损，准备手动干预
3. 如果形态变化，考虑提前平仓
```

### 6. 平仓

```bash
1. 触及止盈 → 自动平仓
2. 触及止损 → 自动平仓
3. 形态变化 → 手动平仓
4. 记录交易结果
```

---

## 🔑 签名计算

```bash
# HMAC-SHA256 签名
参数：timestamp=1234567890000
密钥：SECRET_KEY

签名 = HMAC-SHA256(参数，密钥)

bash 实现：
SIGNATURE=$(echo -n "timestamp=$TIMESTAMP" | openssl dgst -sha256 -hmac "$SECRET_KEY" | awk '{print $2}')
```

---

## 📊 测试网领水

```
领水地址：https://testnet.binancefuture.com/futures-activity/faucet

可领取：
- 5000 USDT（每天）
- 5000 USDC（可能需要单独领取）

到账时间：1-2 分钟
```

---

## ⚠️ 常见错误

### 错误 1：符号错误

```bash
# 错误
side: "BUY"  # 做空
side: "SELL" # 做多

# 正确
side: "BUY"  # 做多（低价买入，高价卖出）
side: "SELL" # 做空（高价卖出，低价买回）
```

### 错误 2：止损方向错误

```bash
# 多头止损应该是 SELL（卖出平仓）
# 空头止损应该是 BUY（买入平仓）

# 错误
多头止损 side: "BUY"  # 这是加仓，不是止损！

# 正确
多头止损 side: "SELL"
空头止损 side: "BUY"
```

### 错误 3：忘记 reduceOnly

```bash
# 平仓时必须设置 reduceOnly: "true"
# 否则会开反向仓位

# 错误
平仓单没有 reduceOnly → 开了反向仓位

# 正确
平仓单 reduceOnly: "true" → 只减仓
```

---

## 📝 学习检查清单

- [ ] 理解做多和做空的本质区别
- [ ] 理解杠杆和爆仓的关系
- [ ] 会计算开仓数量
- [ ] 会计算强平价格
- [ ] 会计算盈亏
- [ ] 理解止损止盈的方向
- [ ] 理解 reduceOnly 的作用
- [ ] 会计算 HMAC-SHA256 签名
- [ ] 知道如何领水
- [ ] 知道常见错误及避免方法

---

**东京节点必须完全理解以上内容才能开始实盘！**
