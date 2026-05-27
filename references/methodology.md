# 方法论：三层分工 + 七步迭代

本文给出 superpowers + gstack（+ 可选 GSD）的完整方法论。SKILL.md 是总纲，本文是详尽展开。

## 1. 三层分工的根本原因

| 层 | 解决的问题 | 失败时的症状 |
|---|---|---|
| 决策（gstack） | "做什么 / 要不要做 / 用什么姿势做" | 写出来了但不是用户要的；把 yak 全剃了 |
| 执行（superpowers） | "把决定的事按工程纪律做出来" | 代码写出来但没测试、没验收、没 review |
| 上下文（GSD） | "在长项目里别忘了上次自己说过什么" | 同一个项目反复改 spec、互相覆盖 |

**为什么不能让一个框架同时做三层？**
- gstack 的执行命令（`/autoplan`、`/review`）相对粗放，TDD/subagent 闭环不如 superpowers 严格。
- superpowers 的决策 skill（`brainstorming`、`writing-plans`）是工程师视角，缺少 CEO / Designer / QA 这类 product-side 反思。
- 都内置 brainstorm/plan，会**双跑** —— 一次任务跑两遍同类型 skill，token × 2，结论还可能互相否决。

## 2. 七步迭代细节

### Step 1 — Think
- 入口：gstack `/office-hours`（默认必跑）
- 二审（可选）：gstack `/plan-ceo-review`（产品/商业判断），`/plan-design-review`（设计判断）
- 关闭：superpowers `brainstorming`（除非属于 small 规模任务）
- 产出：用户故事 / 验收标准 / "应不应该做"的明确决定

### Step 2 — Plan
- 入口：gstack `/plan-eng-review`（架构 / 数据流 / 风险）
- 然后：superpowers `writing-plans` 把决议落成可执行的计划文档（plan-as-executed）
- 产出：分任务的 plan，可被 `executing-plans` / `subagent-driven-development` 直接消费

### Step 3 — Build
- 主线：superpowers `executing-plans` + `test-driven-development`
- 复杂或可并行：superpowers `subagent-driven-development` / `dispatching-parallel-agents`
- worktree：superpowers `using-git-worktrees`（Claude Code 用 `EnterWorktree`，其他 agent 走 `git worktree add` 兜底）
- 关闭：gstack `/autoplan`（避免和 `executing-plans` 抢主导）

### Step 4 — Review
- 主线：superpowers `requesting-code-review`（dispatch general-purpose subagent，把 review checklist 跑完）
- 二审：gstack `/review` 或 `/codex` 拉外部模型再过一遍
- 接收：superpowers `receiving-code-review`（避免做无意义/盲目的"performative agreement"）

### Step 5 — Test / QA
- 主线：gstack `/qa` / `/qa-only`（含真实浏览器测试 / 用户视角 / 真设备能力）
- 补丁：superpowers `verification-before-completion`（针对 bug 修复的"证明已修复"门禁）

### Step 6 — Ship
- 主线：gstack `/ship`（版本号 + CHANGELOG + PR 流水线）
- 部署：gstack `/land-and-deploy`、`/canary`
- 收口：superpowers `finishing-a-development-branch`（merge → 验证 → 删 worktree → 删 branch 的安全顺序）

### Step 7 — Reflect
- 主线：gstack `/retro`、`/learn`
- 持久化：写入 GSD `KNOWLEDGE.md` / `DECISIONS.md`（如果引入了 GSD 层）

## 3. 决策启发式

回答以下三个问题，反向推出本次任务该用什么组合：

1. **要不要进入决策层？** —— 任务是否需要"重新讨论应不应该做"。是 → gstack 决策；否 → 直接 superpowers 执行。
2. **要不要叠 GSD？** —— 任务是否跨会话/跨人/已经在漂移。是 → 加 GSD anchor 文件；否 → 不要加，纯属拖累。
3. **要不要并行子 agent？** —— 是否存在彼此独立的子任务。是 → superpowers `subagent-driven-development` / `dispatching-parallel-agents`；否 → 单线 `executing-plans`。

## 4. GSD 何时上场

| 触发信号 | 行动 |
|---|---|
| 一个项目要跨多次会话 / 一周以上 | 引入 `PROJECT.md` + `M001-ROADMAP.md` |
| 出现 ≥2 名工程师 / 多 agent 实例 | 引入 `DECISIONS.md` 锁住关键决策 |
| 发现自己在不同会话给出矛盾结论 | 引入 `KNOWLEDGE.md` 把规则写死 |
| 状态 / 进度难追踪 | 引入 `STATE.md`（v1）或 `M00x-ROADMAP.md`（v2） |

**反例**：单 session、两小时能搞定的任务，不要写 GSD —— 它是上下文 anchor，不是流程小红书。

## 5. 常见反模式

| 反模式 | 症状 | 纠正 |
|---|---|---|
| 全开 23 个 gstack + 14 个 superpowers | 启动一次 30k token 全跑预热 | 按七步精选启用，关闭重复角色 |
| 小任务跑完七步 | 改一行 CSS 跑了 20 分钟讨论 | 标记为 `small` 走最短闭环 |
| brainstorm 双跑 | gstack 和 superpowers 各开一轮 | AGENTS.md 写硬约束，决策只让 gstack 跑 |
| 把 GSD 当流程 | 写了 PROJECT.md 但没人维护 | 只在长项目用，并指定"谁负责更新" |
| 把官方 gstack 命令搬进当前 skill | 命令脚本依赖 bun，AIME 容器跑不起来 | 本 skill 只做方法论，命令仍由用户在本地 agent 里执行 |
