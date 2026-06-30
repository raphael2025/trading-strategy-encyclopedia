# 东京节点 - 加密货币交易学习系统 🦞

> 1 周密集学习合约交易，目标：掌握技能 + 变现

---

## 📊 配置概览

| 参数 | 值 |
|------|-----|
| **测试网本金** | 5000 USDC + 5000 USDT |
| **交易对** | BTC、ETH、SOL |
| **杠杆** | 10x |
| **仓位** | 20% (2000 USDT) |
| **学习频率** | 每小时 |
| **验证频率** | 每 4 小时 |

---

## 🚀 快速部署

### 1️⃣ 克隆仓库

```bash
# 在东京服务器上执行
git clone https://github.com/YOUR_USERNAME/tokyo-trading-learning.git
cd tokyo-trading-learning
```

### 2️⃣ 配置凭证

```bash
# 复制模板并填写真实信息
cp .credentials-tokyo-trading.json.template .credentials-tokyo-trading.json

# 编辑文件，填写：
# - GitHub Token
# - 币安测试网 API Key
# - 币安测试网 Secret Key
nano .credentials-tokyo-trading.json
```

### 3️⃣ 部署 Cron

```bash
# 安装 Cron
crontab tokyo-trading-cron.txt

# 验证
crontab -l
```

### 4️⃣ 启动学习

```bash
# 手动执行第一次学习
bash scripts/trading-learning.sh

# 查看日志
tail -f /tmp/tokyo-trading.log
```

---

## 📁 目录结构

```
tokyo-trading-learning/
├── scripts/
│   ├── trading-learning.sh      # 学习脚本（每小时）
│   ├── trading-verification.sh  # 验证脚本（每 4 小时）
│   ├── market-analysis.sh       # 市场分析（支撑/阻力/形态）
│   ├── trading-signal.sh        # 信号生成（动态止损止盈）
│   └── trading-daily-summary.sh # 每日总结
├── memory/tokyo-trading/
│   ├── knowledge/               # 学习资料
│   ├── verification/            # 验证记录
│   ├── signals/                 # 交易信号
│   └── daily-learning/          # 学习日志
├── .credentials-tokyo-trading.json.template  # 配置模板
└── tokyo-trading-cron.txt       # Cron 配置
```

---

## 📅 学习时间表（东京时间）

| 时间 | 活动 | 时长 |
|------|------|------|
| **每小时** | 学习新知识 | 30 分钟 |
| **每 4 小时** | 测试网验证 | 30 分钟 |
| **06:00** | 每日总结 | 自动 |
| **周日 05:00** | 周总结 | 自动 |

---

## 🎯 1 周学习计划

| 天数 | 学习内容 | 验证内容 | 目标 |
|------|---------|---------|------|
| **Day 1** | K 线基础、合约原理 | API 连接、开平仓 | 熟悉测试网 |
| **Day 2** | 反转形态 | 形态识别 20 例 | 胜率>50% |
| **Day 3** | 持续形态、指标 | 形态 + 指标组合 | 胜率>55% |
| **Day 4** | 订单簿、流动性 | 止损狩猎识别 | 避开 80% 猎杀 |
| **Day 5** | 风险管理 | 仓位计算、止损设置 | 回撤<20% |
| **Day 6** | 综合策略回测 | 回测 100 次 | 夏普>1.5 |
| **Day 7** | 实盘测试 | 小额交易（$20） | 保本或小赚 |

---

## ⚠️ 风险控制

| 规则 | 限制 |
|------|------|
| **单笔最大仓位** | 20% (2000 USDT) |
| **杠杆倍数** | 10x |
| **止损类型** | 动态（根据支撑/阻力） |
| **止盈类型** | 动态（根据形态目标） |
| **最小盈亏比** | 1.5:1 |
| **每日最大亏损** | 200 USDT |
| **每日最大交易** | 10 次 |

---

## 📊 成功指标

| 阶段 | 胜率 | 盈亏比 | 最大回撤 |
|------|------|--------|---------|
| **Day 2** | >50% | >1.5:1 | <30% |
| **Day 4** | >55% | >1.8:1 | <25% |
| **Day 6** | >60% | >2:1 | <20% |
| **Day 7** | 实盘验证 | 实盘验证 | 实盘验证 |

---

## 🔄 同步机制

### 东京节点 → GitHub

```bash
# 每次学习后自动推送
git add memory/tokyo-trading/
git commit -m "learn: $(date +%Y-%m-%d) 学习记录"
git push origin main
```

### GitHub → 其他节点

```bash
# 其他节点可以 pull 学习成果
git pull origin main
```

---

## 💰 变现途径

### 无风险
- 内容创作（Twitter、教程）
- 空投猎人（测试网交互）
- 咨询/教学

### 低风险
- 套利交易（交易所价差）
- 流动性挖矿

### 高风险（不建议）
- ❌ 合约交易（120 USDC 是最后资金）

---

## 🛠️ 故障排除

### Cron 不执行

```bash
# 检查 Cron 状态
systemctl status cron

# 查看日志
tail -f /tmp/tokyo-trading.log
```

### API 连接失败

```bash
# 测试 API 连接
bash scripts/trading-verification.sh

# 检查凭证
cat .credentials-tokyo-trading.json | jq '.binance_testnet'
```

---

## 📞 支持

- GitHub Issues: https://github.com/YOUR_USERNAME/tokyo-trading-learning/issues
- 文档：`memory/tokyo-trading/` 目录

---

**🦞 打造贾维斯，从交易专家开始！**
