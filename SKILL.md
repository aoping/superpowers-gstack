---
name: superpowers-gstack
description: 在 Claude Code、Codex CLI / App、Cursor、Gemini CLI、OpenCode、Copilot CLI、Factory Droid 等多种 coding agent 中标准化使用 obra/superpowers（执行/方法论层）与 garrytan/gstack（决策/角色层）两大开源框架的统一工作流指南，提供三层分工心智模型、Think→Plan→Build→Review→Test→Ship→Reflect 七步迭代命令序列、跨 agent 工具能力映射，以及避免 brainstorm/plan/review 双跑的冲突规避规则。适用于：用户希望"把 superpowers + gstack 套到我的 Claude Code/Codex/Cursor 上"、"按 gstack/superpowers 完成一个迭代"、"决定该用哪个框架的 brainstorm/plan"、"小改动要不要走完整流程"、"在多种 agent 之间共用同一套工作流"。
---

# superpowers-gstack：跨 Agent 标准化工作流

## 这个 Skill 解决什么问题

[obra/superpowers](https://github.com/obra/superpowers) 与 [garrytan/gstack](https://github.com/garrytan/gstack) 是两套同时被广泛使用、但容易**互相打架**的 coding agent 框架：

- 都内置 brainstorm / plan / review / qa 类 skill。
- 都声称"跨工具可用"（Claude Code、Codex CLI/App、Cursor、Gemini CLI、OpenCode、Copilot CLI、Factory Droid 等）。
- 但默认安装下，Agent 在做"想清楚要做什么"和"动手做"的时候会**双跑**——既烧 token 又出现互相否决。

本 Skill 不替代它们，而是给出一份**官方使用姿势之外的"方法论 + 跨工具适配"**：

1. 三层分工心智模型（决策 / 上下文 / 执行）。
2. 七步迭代标准命令序列。
3. 跨 agent 能力适配矩阵。
4. 安装/启用脚手架与命令推荐脚本。

> 引用：方法论灵感来自 dev.to 文章 *A Claude Code Skills Stack: How to Combine Superpowers, gstack, and GSD Without the Chaos*（Yaohua Chen, ImagineX）。superpowers/gstack 仓库的安装与命令见各自官方 README，本 Skill 不复制其源码。

## 一句话心智模型

> **gstack thinks（决策） → superpowers executes（执行） → 必要时叠加 GSD 稳上下文。**

| 层 | 推荐框架 | 主要职责 | 典型命令/skill |
|---|---|---|---|
| 决策 / 角色 | **gstack** | 想清楚做什么、要不要做、设计与产品判断 | `/office-hours`、`/plan-ceo-review`、`/plan-eng-review`、`/plan-design-review`、`/cso` |
| 执行 / 方法论 | **superpowers** | 把决定的事按 TDD + 子 agent + 验证闭环做出来 | `brainstorming`（轻量细化）、`writing-plans`、`executing-plans`、`subagent-driven-development`、`test-driven-development`、`requesting-code-review`、`verification-before-completion`、`finishing-a-development-branch` |
| 上下文 / 规约（可选） | **GSD v2** | 在跨会话长项目里防止 spec / state 漂移 | `PROJECT.md` / `DECISIONS.md` / `KNOWLEDGE.md` / `M001-ROADMAP.md` 等 anchor 文件 |

**不要在同一阶段让两个框架抢活**——这是后面所有规则的根。

## 七步迭代速览（Think → Ship → Reflect）

```
[1] Think      → gstack: /office-hours  (gstack:plan-ceo-review 二审)
[2] Plan       → gstack: /plan-eng-review  → superpowers: writing-plans
[3] Build      → superpowers: executing-plans / subagent-driven-development
                            + test-driven-development
[4] Review     → superpowers: requesting-code-review
                  (gstack: /review or /codex 二审，可选)
[5] Test/QA    → gstack: /qa or /qa-only  (浏览器/真用户视角)
[6] Ship       → gstack: /ship  → /land-and-deploy / /canary
                  superpowers: verification-before-completion → finishing-a-development-branch
[7] Reflect    → gstack: /retro / /learn  (沉淀决策与教训)
```

**铁律：**
- Think 与 Plan 决策环节由 gstack 主导，关闭 superpowers 的 brainstorming（除非任务非常小，需要它做轻量细化）。
- Build / Review / Verify 闭环由 superpowers 主导，关闭 gstack 的 `/autoplan` 等执行类命令。
- 是否进入完整七步要看任务规模，见下方"任务规模与流程裁剪"。

执行 `python3 scripts/print_workflow.py --scope feature` 可直接打印对应任务规模的命令序列；详见 [references/methodology.md](references/methodology.md)。

## 任务规模与流程裁剪（避免小任务被重流程压垮）

| 规模 | 描述 | 推荐组合 |
|---|---|---|
| `small` | 两行配置 / 改文案 / 改一个常量 | 直接 superpowers `executing-plans`（关掉 brainstorming/写 plan），无需 gstack |
| `feature` | 单仓 1–3 天的功能 | 完整七步：gstack 决策 + superpowers 执行 |
| `project` | 跨会话/跨人/跨周的项目 | 七步 + 叠加 GSD 上下文层（PROJECT/DECISIONS/KNOWLEDGE/ROADMAP） |

执行 `python3 scripts/print_workflow.py --scope <small|feature|project>` 拿到对应清单。

## 跨 Agent 适配（Claude Code / Codex / Cursor / 其他）

不同 agent 对 skill 加载、subagent dispatch、worktree、hook 的支持差异很大。**核心规则**：

1. **superpowers** 用官方 plugin marketplace 安装：`/plugin marketplace add obra/superpowers-marketplace`，然后按 [Claude / Codex App / Codex CLI / Cursor / Gemini / OpenCode / Copilot CLI / Factory Droid] 选择对应包。
2. **gstack** 用官方 `bun` / `curl` 一键脚本（仓库 README 第一段，见 https://github.com/garrytan/gstack）。其内部脚本以 `bun` 为运行时，需要本机存在 `bun`。
3. **AGENTS.md / CLAUDE.md / .cursorrules** 中加入"何时让谁主导"的硬约束，避免 brainstorm 类 skill 被自动召回双跑。
4. **Worktree**：仅 Claude Code 提供 agent 可调用的 `EnterWorktree` 等原生工具；其他 agent 走 `git worktree add` 兜底（superpowers 的 `using-git-worktrees` skill 会自动 detect-and-defer）。
5. **Subagent**：Claude Code 的 `Task`、Codex 的 `wait_agent`、Gemini 的 `@agent-name`、Cursor 的 `cursor-agent`、Copilot CLI 的 `additionalContext`、OpenCode 的 `experimental.chat.messages.transform` 都可承载 superpowers 的 subagent-driven-development，详见 [references/agent-matrix.md](references/agent-matrix.md)。

执行 `python3 scripts/bootstrap_stack.py --target <claude|codex-cli|codex-app|cursor|gemini|opencode|copilot|factory|generic>` 可生成对应环境的：
- 安装命令
- `AGENTS.md` 片段
- skill 召回策略片段
- 推荐启用 / 关闭的 skill 清单

## 冲突规避（强制约束）

执行任何任务前，先按这三条对齐：

1. **决策不双跑**：进入 Think/Plan 时，关闭 superpowers 的 `brainstorming`、保留 gstack `/office-hours`、`/plan-ceo-review`、`/plan-eng-review`。
2. **执行不双跑**：进入 Build 时，关闭 gstack `/autoplan`，让 superpowers 的 `writing-plans` → `executing-plans` 闭环主导。
3. **小改动直接跳过决策层**：`small` 规模任务跳过 gstack，直接走 superpowers 最短闭环；不要为了"讲究"把 7 步全跑。

[references/playbooks.md](references/playbooks.md) 给出 small / feature / project 三种典型 playbook，含具体命令时序与"应该启用 / 应该关闭"的 skill 列表。

## 何时加第三层（GSD）

仅在以下任一条件成立时才引入 GSD：

- 任务跨会话（一次开几次窗、用户中途换设备）。
- 任务跨人（≥2 名工程师）或跨周。
- 已经发现 spec/状态/边界在不同会话间漂移（"上次说要 A，这次又改 B"）。

GSD 的角色是"长上下文 anchor"，不是又一个执行框架。详见 [references/methodology.md](references/methodology.md) 的 *GSD 何时上场*。

## Skill 资源索引

- [references/methodology.md](references/methodology.md) — 三层分工 + 七步迭代完整说明、决策启发式、GSD 触发条件。
- [references/agent-matrix.md](references/agent-matrix.md) — Claude Code / Codex CLI / Codex App / Cursor / Gemini / OpenCode / Copilot CLI / Factory Droid / Goose / Auggie 适配矩阵：skill 加载、subagent、worktree、hook、AGENTS.md 片段。
- [references/skill-catalog.md](references/skill-catalog.md) — superpowers 14 项 skill + gstack 23 项 slash 工具的速查清单与"建议是否启用"。
- [references/playbooks.md](references/playbooks.md) — small / feature / project 三种端到端 playbook。

## 脚本

```bash
# 1. 根据当前 agent 输出安装/启用清单与 AGENTS.md 片段
python3 scripts/bootstrap_stack.py --target claude
python3 scripts/bootstrap_stack.py --target codex-cli
python3 scripts/bootstrap_stack.py --target cursor
python3 scripts/bootstrap_stack.py --target gemini
python3 scripts/bootstrap_stack.py --target opencode
python3 scripts/bootstrap_stack.py --target copilot
python3 scripts/bootstrap_stack.py --target factory
python3 scripts/bootstrap_stack.py --target generic

# 2. 根据任务规模输出推荐命令序列
python3 scripts/print_workflow.py --scope small
python3 scripts/print_workflow.py --scope feature
python3 scripts/print_workflow.py --scope project
```

两个脚本只用 Python 3 stdlib，可直接在任何 agent 容器内运行。它们是"指引"性质，不会修改用户仓库。
