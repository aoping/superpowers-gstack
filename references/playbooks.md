# Playbooks（端到端实战演练）

## 1. Small — 两行配置改动

**场景**：改一个常量、修一行 CSS、更新一个版本号。

**不要用**：gstack 决策层；superpowers `brainstorming`。

```
# 1. 直接创建 worktree 并切入（可选，改一行不切也行）
→ superpowers: using-git-worktrees（如果 agent 支持）

# 2. 执行
→ superpowers: executing-plans（plan = "把 X 从 A 改成 B"）

# 3. 验证
→ superpowers: verification-before-completion（跑测试 / 视觉回归）

# 4. 收口
→ superpowers: finishing-a-development-branch
```

**用时**：1–3 轮 Agent 来回。

---

## 2. Feature — 单仓 1–3 天功能

**场景**：实现一个新 API 端点 + 前端表单 + 测试 + 文档。

### Think（gstack 决策层）

```
/office-hours
  → 和用户对齐需求、边界、验收标准
  → 输出：User Story + Acceptance Criteria

/plan-ceo-review   （可选，如果涉及产品方向 / scope expansion）
/plan-design-review （可选，如果涉及 UI/UX 变更）
```

### Plan

```
/plan-eng-review
  → 架构 / 数据流 / 技术风险
  → 输出：批准的技术方向

→ superpowers: writing-plans
  → 把上面的决策写成可执行 plan（任务列表、依赖、顺序）
  → 输出：plan doc
```

### Build

```
→ superpowers: using-git-worktrees  （创建 feature branch + worktree）
→ superpowers: executing-plans + test-driven-development
  → RED (写测试) → GREEN (实现) → REFACTOR

如果有 3+ 可并行子任务：
→ superpowers: subagent-driven-development
  → 每个子 agent 拿到一个 task + TDD 纪律
```

### Review

```
→ superpowers: requesting-code-review
  → 子 agent 按 checklist 跑
→ superpowers: receiving-code-review
  → 不盲目同意，技术质疑先验证再采纳

/review  或  /codex   （二审，可选。特别是安全/性能敏感改动）
```

### Test / QA

```
/qa  或  /qa-only
  → 真浏览器测试、用户视角验收
  → 如果有 bug，回到 Build 重来

→ superpowers: verification-before-completion
  → 证明已完成（测试绿 + 验收标准达标）
```

### Ship

```
→ superpowers: finishing-a-development-branch
  → merge → verify → remove worktree → delete branch

/ship
  → 版本号 + CHANGELOG + PR
  → /land-and-deploy 或 /canary（如有流水线）
```

### Reflect

```
/retro
  → 这次迭代有什么做得好/不好
/learn
  → 有哪些新模式值得记住
```

**用时**：一到多个 session，每 session 几十轮交互。

---

## 3. Project — 跨周 / 跨人 / 多 session 大项目

在 Feature playbook 之上，增加 **GSD 上下文层**：

### 初始化 GSD（首次进入项目时）

创建以下 anchor 文件（GSD v2 格式推荐）：

```
.project/
├── PROJECT.md          → 这个项目是什么（一段话）、长期目标
├── DECISIONS.md        → 已做的关键决策（带日期和原因）
├── KNOWLEDGE.md        → 跨会话规则、约定、避坑点
└── M001-ROADMAP.md     → 第一个 Milestone 的切片 plan（可有多个 M00x）
```

### 每次新 session 启动时

1. 读取 `.project/` anchor 文件，恢复上下文。
2. 确认当前处于哪个 Milestone / 哪个任务。
3. 按 Feature playbook 执行。

### 每次 session 结束时

1. `/learn` + `/retro` 产出写回 `KNOWLEDGE.md` / `DECISIONS.md`。
2. 更新 `M00x-ROADMAP.md` 状态。

### 何时 **不要** 使用 GSD

- 单次会话就能做完的事情。
- 只有你自己一个人、且不超过 2 session 的事情。
- 加了 GSD 但不维护 → 只是噪声，及时删掉。

---

## 4. 决策参考表

| 我的情况… | 推荐组合 |
|---|---|
| 改个常量 / 修 typo | superpowers only，最短闭环 |
| 新增一个普通 API | gstack 决策 + superpowers 执行 |
| 改 Monorepo 里三个包 | gstack 决策 + superpowers subagent 并行 |
| 跨周 Sprint，多人协作 | gstack + superpowers + GSD |
| 不确定需求是什么 | 先只跑 gstack `/office-hours` 理清需求 |
| 要做安全审计 | gstack `/cso` + `/careful` |
| 只要写文档 / release notes | gstack `/document-release` + `/ship` |
