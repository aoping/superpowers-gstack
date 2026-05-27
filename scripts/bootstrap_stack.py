#!/usr/bin/env python3
"""bootstrap_stack.py — 输出 superpowers + gstack 在指定 agent 上的安装/启用清单。

用法：
    python3 scripts/bootstrap_stack.py --target claude
    python3 scripts/bootstrap_stack.py --target codex-cli
    python3 scripts/bootstrap_stack.py --target codex-app
    python3 scripts/bootstrap_stack.py --target cursor
    python3 scripts/bootstrap_stack.py --target gemini
    python3 scripts/bootstrap_stack.py --target opencode
    python3 scripts/bootstrap_stack.py --target copilot
    python3 scripts/bootstrap_stack.py --target factory
    python3 scripts/bootstrap_stack.py --target generic

只输出建议命令与 AGENTS.md 片段，不会修改任何文件。
"""

from __future__ import annotations

import argparse
import sys
import textwrap

TARGETS = {
    "claude",
    "codex-cli",
    "codex-app",
    "cursor",
    "gemini",
    "opencode",
    "copilot",
    "factory",
    "generic",
}

COMMON_AGENTS_MD = textwrap.dedent(
    """\
    ## Stack discipline (superpowers + gstack)

    ### Layer ownership
    - **Decision phase** → gstack (`/office-hours`, `/plan-ceo-review`,
      `/plan-eng-review`, `/plan-design-review`).
    - **Execution phase** → superpowers (`writing-plans`, `executing-plans`,
      `subagent-driven-development`, `test-driven-development`,
      `requesting-code-review`, `verification-before-completion`,
      `finishing-a-development-branch`).
    - **Long-term context** (multi-session projects) → optional GSD anchors.

    ### Hard rules
    1. Do NOT run gstack and superpowers brainstorm/plan/review skills in the
       same phase.
    2. Skip the decision phase entirely for changes < 10 LoC or pure config edits.
    3. Worktree: prefer host-native tool (e.g. EnterWorktree on Claude Code)
       → fall back to `git worktree add .worktrees/<name>`.
    4. Always run `verification-before-completion` →
       `finishing-a-development-branch` before merge.
    """
)


def install_block(target: str) -> str:
    if target == "claude":
        return textwrap.dedent(
            """\
            # 1. superpowers (Claude Code plugin)
            /plugin marketplace add obra/superpowers-marketplace
            /plugin install superpowers

            # 2. gstack (Claude Code preset)
            curl -fsSL https://raw.githubusercontent.com/garrytan/gstack/main/install.sh | bash

            # 3. (recommended) keep gstack up to date
            /gstack-upgrade
            """
        )
    if target in ("codex-cli", "codex-app"):
        sub = "Codex CLI" if target == "codex-cli" else "Codex App"
        return textwrap.dedent(
            f"""\
            # superpowers ({sub})
            # See obra/superpowers README → "Codex" / "Codex App" install section.
            # Marketplace install via the Codex plugin manager (npm/bun).
            # Tool mapping (codex-tools.md):
            #   Task returns result → wait_agent
            #   Spawned-agent waiting → wait_agent (NOT bare `wait`)
            #   Subagent dispatch → spawn_agent / close_agent

            # gstack ({sub})
            # gstack ships agents/openai.yaml. Run the official install script:
            curl -fsSL https://raw.githubusercontent.com/garrytan/gstack/main/install.sh | bash
            """
        )
    if target == "cursor":
        return textwrap.dedent(
            """\
            # superpowers (Cursor)
            # See obra/superpowers README → "Cursor" install section.
            # On Windows, hooks must route through ./hooks/run-hook.cmd.

            # gstack (Cursor)
            curl -fsSL https://raw.githubusercontent.com/garrytan/gstack/main/install.sh | bash
            # gstack writes to .cursor/ rules; do not edit them by hand.
            """
        )
    if target == "gemini":
        return textwrap.dedent(
            """\
            # superpowers (Gemini CLI)
            # See obra/superpowers README → "Gemini CLI". Subagent dispatch
            # uses @agent-name / @generalist.

            # gstack (Gemini)
            curl -fsSL https://raw.githubusercontent.com/garrytan/gstack/main/install.sh | bash
            """
        )
    if target == "opencode":
        return textwrap.dedent(
            """\
            # superpowers (OpenCode)
            # Install via OpenCode plugin loader (see obra/superpowers v5.x notes).
            # Bootstrap is injected into the FIRST user message via
            # experimental.chat.messages.transform — do not move it back to system.

            # gstack (OpenCode)
            curl -fsSL https://raw.githubusercontent.com/garrytan/gstack/main/install.sh | bash
            """
        )
    if target == "copilot":
        return textwrap.dedent(
            """\
            # superpowers (Copilot CLI v1.0.11+)
            # sessionStart hook emits SDK-standard top-level additionalContext.
            # See obra/superpowers references/copilot-tools.md for tool mapping.

            # gstack on Copilot CLI
            # No official gstack adapter yet — use the `generic` install path:
            curl -fsSL https://raw.githubusercontent.com/garrytan/gstack/main/install.sh | bash
            # Then mirror the Stack discipline block into AGENTS.md (see below).
            """
        )
    if target == "factory":
        return textwrap.dedent(
            """\
            # superpowers (Factory Droid)
            # See obra/superpowers README → "Factory Droid" install section.

            # gstack (Factory)
            curl -fsSL https://raw.githubusercontent.com/garrytan/gstack/main/install.sh | bash
            # gstack writes to .factory/ host config.
            """
        )
    # generic
    return textwrap.dedent(
        """\
        # Generic agent (Goose / Auggie / Qwen / OpenClaw / custom)
        # 1. superpowers — install via the official marketplace if your host
        #    supports plugin loading; otherwise clone the repo and point your
        #    skill loader at the `skills/` directory.
        # 2. gstack — run the official installer:
        curl -fsSL https://raw.githubusercontent.com/garrytan/gstack/main/install.sh | bash
        # 3. Mirror the Stack discipline block into your host's AGENTS.md /
        #    system prompt entry point so brainstorm/plan/review do not double-fire.
        """
    )


def host_specific_notes(target: str) -> str:
    if target == "claude":
        return "- Use EnterWorktree for worktrees (do NOT call `git worktree add` while EnterWorktree is available)."
    if target == "codex-cli":
        return "- Spawned-agent waiting uses `wait_agent`, NOT bare `wait` (which is exec/wait for code-mode cells)."
    if target == "codex-app":
        return "- Sandbox is already inside a worktree — superpowers `using-git-worktrees` will detect via GIT_DIR != GIT_COMMON_DIR and skip creation."
    if target == "cursor":
        return "- On Windows, ensure hooks-cursor.json routes through ./hooks/run-hook.cmd."
    if target == "gemini":
        return "- For parallel work, dispatch multiple `@generalist` subagents (one per independent task)."
    if target == "opencode":
        return "- Bootstrap is cached at module level; do not introduce per-step file reads (issue #1202)."
    if target == "copilot":
        return "- Copilot CLI has no native subagent — superpowers simulates via prompt template; expect serial execution."
    if target == "factory":
        return "- Factory Droid uses host config in .factory/; let gstack manage it (do NOT edit by hand)."
    return "- Verify your host supports skill auto-discovery; if not, mirror skill descriptions into the system prompt manually."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        required=True,
        choices=sorted(TARGETS),
        help="Target coding agent host.",
    )
    args = parser.parse_args()
    target = args.target

    print(f"# === superpowers + gstack bootstrap for {target} ===\n")

    print("## 1. Install commands\n")
    print(install_block(target))

    print("\n## 2. AGENTS.md / CLAUDE.md / .cursorrules snippet\n")
    print("Append the following to your repo-level agent instruction file:\n")
    print(COMMON_AGENTS_MD)

    print("## 3. Host-specific note\n")
    print(host_specific_notes(target))

    print(
        "\n## 4. Verify\n"
        "After install, ask the agent to print which superpowers and gstack skills\n"
        "are loaded. Cross-check against the catalog in references/skill-catalog.md.\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
