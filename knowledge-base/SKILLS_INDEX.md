# OpenHands Skills Index

> 本项目使用以下 OpenHands skill 来增强 AI 智能体的能力。
> Skills 安装在全局目录 `/workspace/.agents/skills/`

## 🎯 已启用 Skills

### 1. intent-recognition
**位置**: `/workspace/.agents/skills/intent-recognition/`
**功能**: 识别用户任务意图、隐藏需求、模糊点
**触发**:
- 接收新用户请求时
- 任务模糊或多义时
- 用户使用间接语言时

**组件**:
- `SKILL.md` - 核心工作流
- `references/intent-patterns.md` - 10 种意图模式
- `references/clarification-questions.md` - 澄清问题模板
- `scripts/extract_intent.py` - 意图提取工具

### 2. task-decomposition
**位置**: `/workspace/.agents/skills/task-decomposition/`
**功能**: 把复杂任务拆分成可执行的子任务
**触发**:
- 复杂/多部分任务
- 涉及 3+ 文件创建
- 需要研究和实现结合

**组件**:
- `SKILL.md` - 核心拆分方法
- `references/decomposition-patterns.md` - 7 种任务类型模式
- `references/dependency-tracking.md` - 依赖追踪
- `scripts/decompose.py` - 任务分解器

### 3. context-self-management
**位置**: `/workspace/.agents/skills/context-self-management/`
**功能**: 防止上下文爆表，自动压缩和管理
**触发**:
- 工具返回 > 5000 tokens
- 累计上下文 > 50% 容量
- 多个子智能体任务时
- 长任务多文件操作

**组件**:
- `SKILL.md` - 核心策略
- `references/compression-patterns.md` - 10 种压缩模式
- `references/continuation-patterns.md` - 跨会话续传
- `scripts/estimate_context.py` - 上下文大小估算
- `scripts/compress_summary.py` - 智能压缩

---

## 📋 使用顺序

当 AI 智能体接收到新任务时：

```
1. intent-recognition
   └→ 解析用户意图、识别隐藏需求

2. task-decomposition (如果复杂)
   └→ 拆分任务、规划执行

3. 执行任务
   └→ 串行优先，max 2 子智能体并行

4. context-self-management (持续)
   └→ 监控上下文、自动压缩
```

## 🔄 自我迭代

每个 skill 都有 `SKILL.md` 作为入口，AI 智能体可以：
1. 通过 `invoke_skill` 调用
2. 通过 trigger phrase 自动触发
3. 在 AGENTS.md 中作为参考

## 📦 安装到其他项目

```bash
# 复制到其他项目
cp -r /workspace/.agents/skills/* /path/to/new/project/.agents/skills/

# 或使用 add-skill skill
# /add-skill https://github.com/your/repo/skills/intent-recognition
```

---

**最后更新**: 2026-06-04
