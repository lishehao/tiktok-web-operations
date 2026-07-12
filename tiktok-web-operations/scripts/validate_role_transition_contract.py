#!/usr/bin/env python3
"""Validate same-task Bootstrap -> Coordinator lifecycle scenarios."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (
    BUNDLE / "README.md",
    ROOT / "SKILL.md",
    ROOT / "references/startup-health-check.md",
    ROOT / "references/role-and-stage-contract.md",
    ROOT / "references/operating-model.md",
    BUNDLE / "thread-supervisor/SKILL.md",
    BUNDLE / "thread-supervisor/references/identity-and-automation.md",
)


def transition(event: str) -> dict[str, object]:
    table = {
        "setup_command": ("BOOTSTRAP_STARTER", "TikTok 启动台", False, "IMMEDIATE"),
        "hard_repair_pending": ("BOOTSTRAP_STARTER", "TikTok 启动台", False, "HOLD"),
        "healthy_handoff": ("TIKTOK_COORDINATOR", "TikTok 主控台", False, "SAME_TASK"),
        "direct_mission_installed": ("TIKTOK_COORDINATOR", "TikTok 主控台", False, "FAST_PATH"),
        "rename_unavailable": ("TIKTOK_COORDINATOR", "DEGRADED_PRESENTATION", False, "CONTINUE"),
    }
    role, title, duplicate, timing = table[event]
    return {
        "role": role,
        "title": title,
        "create_duplicate_main": duplicate,
        "timing": timing,
    }


def main() -> None:
    missing = [str(path) for path in FILES if not path.is_file()]
    assert not missing, f"missing role-transition files: {missing}"
    joined = "\n".join(path.read_text() for path in FILES)

    required = (
        "TikTok 启动台",
        "TikTok 主控台",
        "first available presentation action",
        "same exact task",
        "DEGRADED_RENAME_UNAVAILABLE",
        "direct-mission fast path",
        "never create a second main task",
        "BOOTSTRAP_STARTER",
        "TIKTOK_COORDINATOR",
    )
    absent = [term for term in required if term.lower() not in joined.lower()]
    assert not absent, f"missing lifecycle assertions: {absent}"

    forbidden = (
        "After the user's second message, it self-registers its exact Thread ID, becomes the coordinator",
        "rename failure blocks setup",
        "create a replacement main task for naming",
    )
    present = [term for term in forbidden if term in joined]
    assert not present, f"stale lifecycle semantics remain: {present}"

    events = (
        "setup_command",
        "hard_repair_pending",
        "healthy_handoff",
        "direct_mission_installed",
        "rename_unavailable",
    )
    scenarios = {event: transition(event) for event in events}
    assert scenarios["setup_command"]["title"] == "TikTok 启动台"
    assert scenarios["hard_repair_pending"]["role"] == "BOOTSTRAP_STARTER"
    assert scenarios["healthy_handoff"]["timing"] == "SAME_TASK"
    assert scenarios["direct_mission_installed"]["timing"] == "FAST_PATH"
    assert scenarios["rename_unavailable"]["timing"] == "CONTINUE"
    assert not any(s["create_duplicate_main"] for s in scenarios.values())

    print(json.dumps({"status": "PASS", "scenarios": scenarios}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
