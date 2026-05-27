# 跨 Agent 适配矩阵

> 本文整理 superpowers / gstack 在不同 coding agent 上的适配差异，帮助选择正确的安装方式与 AGENTS.md 片段。
>
> 信息来源：obra/superpowers v5.1.0 README（含 codex-tools.md / copilot-tools.md / opencode 适配说明）与 garrytan/gstack v1.46 README。本文内容只描述使用姿势，不复制官方源码。

## 1. 总览矩阵

| Agent | superpowers 安装入口 | gstack 安装入口 | Skill 加载机制 | Subagent dispatch | Worktree 原生工具 | Hook / sessionStart |
|---|---|---|---|---|---|---|
| **Claude Code** | `/plugin marketplace add obra/superpowers-marketplace` | gstack 官方 `bun` 安装脚本（CLAUDE 适配） | 原生 skill 系统（统一 slash + skills） | `Task(general-purpose)` | `EnterWorktree` / `WorktreeCreate`（agent-callable） | `hookSpecificOutput` |
| **Codex CLI** | superpowers Codex plugin（README "Codex" 段） | gstack codex 适配（agents/openai.yaml） | Codex tools / `worker` dispatch（见 codex-tools.md） | `spawn_agent` / `wait_agent` / `close_agent` | 无 agent-callable 工具，sandbox 内由 harness 预创建 | 无 sessionStart，靠 AGENTS.md 注入 |
| **Codex App** | superpowers Codex 适配（README "Codex App"） | gstack codex 适配 | 与 Codex CLI 类似 | `spawn_agent` / `wait_agent` | 沙箱内**已**在 worktree，不再额外建 | 无 sessionStart |
| **Cursor** | superpowers cursor plugin（README "Cursor"） | gstack cursor 适配 | `.cursor/` 规则 + slash | `cursor-agent -p` | 无 agent-callable，走 `git worktree add` 兜底 | `hooks-cursor.json`（Windows 走 `run-hook.cmd`） |
| **Gemini CLI** | superpowers gemini 适配 | gstack gemini 适配 | `GEMINI.md` + skill 文件 | `@agent-name` / `@generalist`（Task 等价） | 无 agent-callable，走 `git worktree add` 兜底 | sessionStart 不通用，靠 GEMINI.md 注入 |
| **OpenCode** | superpowers opencode adapter（v5.x） | gstack 通用 / `OPENCODE.md` | `experimental.chat.messages.transform` 注入 bootstrap | `experimental.agent` | 无 agent-callable，走 `git worktree add` 兜底 | bootstrap 缓存于模块级（v5.0.x 修复） |
| **Copilot CLI** | superpowers copilot adapter | gstack 暂未官方适配，可走 generic | `additionalContext` | 无原生子 agent，走 superpowers 内嵌 prompt | `additionalContext` |
| **Factory Droid** | superpowers factory adapter | gstack factory 适配 | factory yaml | factory 子 agent 能力 | 走 `git worktree add` 兜底 | factory yaml |
| **Goose / Auggie / Qwen** | superpowers 通用 marketplace 安装 | gstack generic | 通用 skill loader | 各自原生 | 走 `git worktree add` 兜底 | 取决于 host |

## 2. 每个 Agent 的"开箱准备"

### 2.1 Claude Code

```bash
# 1. 添加 marketplace（首次）
/plugin marketplace add obra/superpowers-marketplace

# 2. 安装 superpowers（按提示选择）
/plugin install superpowers

# 3. 安装 gstack（参见 garrytan/gstack README "Install" 段）
curl -fsSL https://raw.githubusercontent.com/garrytan/gstack/main/install.sh | bash
```

CLAUDE.md / AGENTS.md 推荐片段：

```markdown
## Stack discipline (superpowers + gstack)

- **Decision phase** is owned by **gstack**. Use `/office-hours`, `/plan-ceo-review`,
  `/plan-eng-review`, `/plan-design-review`. Do **NOT** invoke superpowers
  `brainstorming` in this phase unless the task is a one-line change.
- **Execution phase** is owned by **superpowers**. Use `writing-plans`,
  `executing-plans`, `subagent-driven-development`, `test-driven-development`,
  `requesting-code-review`, `verification-before-completion`,
  `finishing-a-development-branch`. Do **NOT** invoke gstack `/autoplan`.
- For worktrees, prefer `EnterWorktree` over `git worktree add`.
- For small (<10 LoC) changes, skip the decision phase entirely.
```

### 2.2 Codex CLI

- superpowers v5.x 提供 codex 专属包，Task → `wait_agent` 映射：详见 superpowers `references/codex-tools.md`。
- gstack 通过 `agents/openai.yaml` 加载；注意 codex 会试图改写它，gstack 已加 filesystem boundary（v0.13.2.0）。
- AGENTS.md 片段（codex 专属）：

```markdown
## Tool mapping
- Task returns result → wait_agent
- Spawned-agent waiting → wait_agent (NOT bare `wait`, which is for code-mode exec/wait)
- Subagent dispatch → spawn_agent / close_agent
```

### 2.3 Codex App

沙箱内已经在 worktree，不要再建第二层。superpowers 的 `using-git-worktrees` 会通过 `GIT_DIR != GIT_COMMON_DIR` 检测自动 skip。

### 2.4 Cursor

- Hook 注意点：Windows 必须经 `run-hook.cmd session-start` 路由（superpowers 已修复 v5.1.0 BOM/路径问题）。
- gstack 的 `/browse`、`/connect-chrome`、`/setup-browser-cookies` 在 Cursor 同样可用，但要确保本机有 Chrome 与 Playwright。

### 2.5 Gemini CLI

- subagent dispatch 用 `@agent-name`；并行任务用 `@generalist` + 多次 dispatch（superpowers v5.1.0 已加映射）。
- worktree 全部走 `git worktree add` 兜底（Gemini 暂无 agent-callable 工具）。

### 2.6 OpenCode

- bootstrap 通过 `experimental.chat.messages.transform` 注入，注意只注入到首条 user message（v5.0.x 修复 #750/#894）。
- 模块级缓存：opencode 每步 reload message，superpowers 已加 `_bootstrapCache` 避免每步 fs.readFile。

### 2.7 Copilot CLI

- 没有原生子 agent；superpowers 用 prompt-template 模拟（详见 superpowers `references/copilot-tools.md`）。
- gstack 暂无官方 copilot 适配，走"generic + AGENTS.md"姿势。

### 2.8 Factory Droid / Goose / Auggie / Qwen / OpenClaw

按 superpowers README 的 "Codex / Cursor / OpenCode / Factory Droid / Goose / Auggie / Qwen Code" 安装段处理。gstack 的 host 适配文件位于其 `.gbrain/`、`.factory/`、`.cursor/`、`.agents/` 目录（v1.46 起统一管理）。

## 3. 跨 agent 通用 AGENTS.md 模板

把以下片段加到仓库根目录的 `AGENTS.md`（或对应 host 的 `CLAUDE.md` / `GEMINI.md` / `.cursorrules`）：

```markdown
# Stack discipline (superpowers + gstack + optional GSD)

## Layer ownership
- gstack owns DECISIONS (Think / Plan / QA / Ship steps).
- superpowers owns EXECUTION (Build / Review / Verify / Finish steps).
- GSD owns LONG-TERM CONTEXT (only enabled when project is multi-session).

## Hard rules
1. Never run gstack and superpowers brainstorm/plan/review skills in the same phase.
2. For changes <10 LoC or pure config edits, skip the decision phase.
3. Worktree creation: prefer host-native (EnterWorktree on Claude Code) → fall back to `git worktree add .worktrees/<name>`.
4. Subagents: use the host-native dispatcher (Task / wait_agent / @agent-name / cursor-agent / additionalContext) per superpowers `references/<host>-tools.md`.
5. Before merge, always run superpowers `verification-before-completion` followed by `finishing-a-development-branch`.
```

## 4. 何时直接关掉某个 skill

| 场景 | 关掉 |
|---|---|
| 任务规模 small | superpowers `brainstorming` + gstack `/office-hours` 全部跳过 |
| 不写 product / 没有 UI | gstack `/design-consultation`、`/plan-design-review`、`/design-html` |
| 仓库无前端 | gstack `/browse`、`/connect-chrome`、`/setup-browser-cookies` |
| 单仓单 session | GSD anchor 文件全部 |
| 没有发布流水线 | gstack `/canary`、`/setup-deploy`（用普通 git push 即可） |
