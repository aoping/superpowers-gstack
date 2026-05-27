#!/usr/bin/env python3
"""print_workflow.py — 输出指定任务规模的 superpowers + gstack 命令序列。

用法：
    python3 scripts/print_workflow.py --scope small
    python3 scripts/print_workflow.py --scope feature
    python3 scripts/print_workflow.py --scope project

参考七步迭代：Think → Plan → Build → Review → Test → Ship → Reflect
"""

from __future__ import annotations

import argparse
import sys
import textwrap

SCOPES = ("small", "feature", "project")

WORKFLOWS = {
    "small": textwrap.dedent(
        """\
        # === SMALL (一两行改动 / 配置 / 文案) ===
        # 跳过决策层；不要让 brainstorming 烧 token。

        [1] Build
            superpowers: using-git-worktrees   (可选)
            superpowers: executing-plans       (plan = "把 X 从 A 改成 B")

        [2] Verify
            superpowers: verification-before-completion

        [3] Finish
            superpowers: finishing-a-development-branch

        # 关闭：所有 gstack slash 命令；superpowers brainstorming / writing-plans。
        """
    ),
    "feature": textwrap.dedent(
        """\
        # === FEATURE (单仓 1–3 天功能) ===
        # 完整七步：gstack 决策 + superpowers 执行。

        [1] Think        gstack: /office-hours
                         (可选) /plan-ceo-review, /plan-design-review

        [2] Plan         gstack: /plan-eng-review
                         superpowers: writing-plans   ← 把决议落成可执行 plan

        [3] Build        superpowers: using-git-worktrees
                         superpowers: executing-plans + test-driven-development
                         (并行) superpowers: subagent-driven-development /
                                              dispatching-parallel-agents

        [4] Review       superpowers: requesting-code-review
                         (二审) gstack: /review or /codex
                         superpowers: receiving-code-review

        [5] Test/QA      gstack: /qa or /qa-only
                         superpowers: verification-before-completion

        [6] Ship         superpowers: finishing-a-development-branch
                         gstack: /ship → /land-and-deploy or /canary

        [7] Reflect      gstack: /retro, /learn

        # 严格关闭：superpowers brainstorming（决策已交给 gstack）。
        # 严格关闭：gstack /autoplan（执行已交给 superpowers）。
        """
    ),
    "project": textwrap.dedent(
        """\
        # === PROJECT (跨周 / 跨人 / 多 session) ===
        # 在 FEATURE 流程之上叠加 GSD 上下文层。

        [0] (一次性) GSD 初始化
            创建 .project/PROJECT.md     (一句话描述项目 + 长期目标)
            创建 .project/DECISIONS.md   (锁定关键决策与时间)
            创建 .project/KNOWLEDGE.md   (跨会话规则、约定、避坑)
            创建 .project/M001-ROADMAP.md (Milestone 切片 plan)

        [1] 每次新 session 启动
            读 .project/ → 恢复上下文
            按 FEATURE playbook 执行（见 --scope feature 输出）

        [2] 每次 session 结束
            gstack: /retro + /learn → 写回 KNOWLEDGE.md / DECISIONS.md
            更新 M00x-ROADMAP.md 状态

        # 重要：GSD 不维护就是噪声；指定一个人 / 一个 agent 实例为 owner。
        """
    ),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", required=True, choices=SCOPES)
    args = parser.parse_args()
    print(WORKFLOWS[args.scope])
    return 0


if __name__ == "__main__":
    sys.exit(main())
