# Skill / Slash 命令速查

> 列出 superpowers 14 项 skill 与 gstack 23 项 slash 工具的功能与"建议是否启用"。
> 命令来源于各自官方 README，本文档不复制实现细节。

## 1. superpowers（14 个）

| Skill | 何时使用 | 是否推荐默认启用 |
|---|---|---|
| `using-superpowers` | 解释整套 superpowers 的入口 | ✅（让 agent 知道何时召回其他 skill） |
| `brainstorming` | 用户需求模糊，需要 Socratic 反问 | ⚠️ small 任务关掉；feature 任务交给 gstack `/office-hours` |
| `writing-plans` | 把决策落成可执行 plan 文档 | ✅ 决策完成后必跑 |
| `executing-plans` | 按 plan 文档逐步执行 | ✅ Build 主线 |
| `subagent-driven-development` | 需要并行 / 隔离子任务 | ✅（任务可并行时） |
| `dispatching-parallel-agents` | 派发多个独立 subagent | ✅（并行场景） |
| `test-driven-development` | RED-GREEN-REFACTOR | ✅ Build 主线（不会写测试就别开始写代码） |
| `systematic-debugging` | 4 阶段根因分析 | ✅（出 bug 必跑） |
| `verification-before-completion` | 证明 bug 已修 / 功能已成 | ✅ Test 阶段必跑 |
| `requesting-code-review` | 通过 subagent 跑 review checklist | ✅ Review 阶段必跑 |
| `receiving-code-review` | 不盲目同意 review 反馈 | ✅（review 之后必跑） |
| `using-git-worktrees` | 在隔离分支里改代码 | ✅（功能开发） |
| `finishing-a-development-branch` | merge → 验证 → 删 worktree → 删 branch | ✅ Ship 收口 |
| `writing-skills` | 自己写新的 superpowers skill | ⚠️ 只在你要扩展 superpowers 时开 |

## 2. gstack（23 个 slash 工具，按角色聚类）

### CEO / 产品
- `/office-hours` — Think 阶段入口（与用户对齐"做什么 + 要不要做"）
- `/plan-ceo-review` — 商业 / 产品视角的 plan 审查

### Designer
- `/design-consultation` — 设计咨询
- `/plan-design-review` — 设计视角 plan 审查
- `/design-shotgun` — 多方案对比设计
- `/design-html` — 直接出 HTML 设计稿

### Eng Manager
- `/plan-eng-review` — 架构 / 数据流 / 风险审查
- `/autoplan` — 自动出 plan（**与 superpowers writing-plans 二选一**）

### QA
- `/qa` — 完整 QA（含浏览器/真机）
- `/qa-only` — 只跑 QA，不动代码

### 调试
- `/investigate` — 单点排查（与 superpowers `systematic-debugging` 二选一，复杂 bug 推荐后者）

### Reviewer
- `/review` — gstack 自家 review
- `/codex` — 用 codex 模型再过一遍

### Release Manager
- `/ship` — 版本号 / CHANGELOG / PR
- `/land-and-deploy` — 部署入口
- `/canary` — 灰度 / canary
- `/document-release` — 写发布说明

### CSO / 安全
- `/cso` — 完整安全审计
- `/careful` — 高敏感修改慎跑
- `/freeze` / `/guard` / `/unfreeze` — 重要分支冻结管理

### Observability
- `/learn` — 学到了什么
- `/retro` — Sprint 复盘

### 浏览器 / Performance / Deploy
- `/browse` — 浏览器自动化
- `/connect-chrome` / `/setup-browser-cookies` — 浏览器集成
- `/benchmark` — 性能基准
- `/setup-deploy` — 一次性部署初始化

### Skill 管理
- `/gstack-upgrade` — 升级 gstack 自身

## 3. 与 superpowers 的"重叠 + 取舍"

| 重叠点 | gstack | superpowers | 建议 |
|---|---|---|---|
| Brainstorm | `/office-hours` | `brainstorming` | **决策只走 gstack**，small 任务才考虑 superpowers |
| Plan | `/plan-eng-review` + `/autoplan` | `writing-plans` | gstack 出"该不该 / 怎么走"，superpowers 出"可执行 plan 文档" |
| Code Review | `/review`、`/codex` | `requesting-code-review` | 主跑 superpowers，二审用 gstack |
| Debug | `/investigate` | `systematic-debugging` | 复杂问题用 superpowers，简单点 gstack 即可 |
| QA | `/qa`、`/qa-only` | `verification-before-completion` | 浏览器 / 真用户视角用 gstack；功能完成判定用 superpowers |
| 收口 | `/ship`、`/land-and-deploy` | `finishing-a-development-branch` | 两者结合：先 superpowers 收 branch，再 gstack `/ship` 走发布 |
| Worktree | 无 | `using-git-worktrees` | 用 superpowers 即可 |

## 4. 命令组合速查（按七步）

```
[Think]  /office-hours → /plan-ceo-review (?) → /plan-design-review (?)
[Plan]   /plan-eng-review → writing-plans
[Build]  using-git-worktrees → executing-plans (+ test-driven-development)
         (并行) → subagent-driven-development / dispatching-parallel-agents
[Review] requesting-code-review → /review or /codex (二审) → receiving-code-review
[Test]   /qa or /qa-only → verification-before-completion
[Ship]   finishing-a-development-branch → /ship → /land-and-deploy → /canary
[Reflect] /retro → /learn (→ 写入 GSD KNOWLEDGE/DECISIONS)
```
