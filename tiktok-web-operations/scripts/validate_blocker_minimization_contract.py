#!/usr/bin/env python3
"""Validate TikTok scope minimization and hard-blocker routing."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (
    ROOT / "SKILL.md",
    ROOT / "references/blocker-minimization.md",
    ROOT / "references/instruction-precedence.md",
    ROOT / "references/startup-health-check.md",
    ROOT / "references/stability-and-circuit-breakers.md",
    ROOT / "references/runtime-and-recovery.md",
    ROOT / "references/persistent-feed-operations.md",
    ROOT / "references/feed-browsing-and-comments.md",
    ROOT / "references/engagement-and-analytics.md",
    ROOT / "references/platform-boundaries.md",
    BUNDLE / "thread-supervisor/SKILL.md",
    BUNDLE / "README.md",
)


def classify(event: str) -> dict[str, str | bool]:
    table = {
        "missing_region_universal": ("DEFAULT_AND_START", "mission", False),
        "network_timeout": ("AUTO_RETRY_CONTINUE", "route", False),
        "chrome_disconnect": ("RECONNECT_SAME_CHROME", "chrome_activation", False),
        "empty_candidates": ("NO_ACTION_CHECKPOINT", "query", False),
        "route_client_block": ("ROTATE_ROUTE_OR_AUTO_RESUME", "route", False),
        "single_lane_failure": ("SUSPEND_LANE_CONTINUE", "lane", False),
        "uncertain_mutation": ("FREEZE_EXACT_NEVER_RETRY", "exact_mutation", False),
        "timed_rate_limit": ("WAIT_AND_AUTO_RECHECK", "affected_lane", False),
        "prohibited_action": ("SKIP_EXACT_SCOPE", "action", False),
        "persistent_captcha": ("HARD_BLOCKER", "whole_mission", True),
        "unrecoverable_login_mismatch": ("HARD_BLOCKER", "whole_mission", True),
        "explicit_account_lock": ("HARD_BLOCKER", "whole_mission", True),
        "sole_chrome_control_unavailable": ("HARD_BLOCKER", "whole_mission", True),
        "explicit_stop": ("TERMINAL_RELEASE", "whole_mission", False),
        "deadline": ("TERMINAL_RELEASE", "whole_mission", False),
    }
    action, scope, decision = table[event]
    return {"action": action, "scope": scope, "decision_required": decision}


def main() -> None:
    missing = [str(path) for path in FILES if not path.is_file()]
    assert not missing, f"missing contract files: {missing}"
    joined = "\n".join(path.read_text() for path in FILES)

    required = (
        "Hard blocker whitelist",
        "no_action_checkpoint",
        "global English with North American bias",
        "Preferences such as region",
        "auto-recheck",
        "freeze exact target/action",
        "asks the user directly",
        "never returns to the launcher",
        "replacement first",
    )
    absent = [term for term in required if term.lower() not in joined.lower()]
    assert not absent, f"missing blocker-minimization assertions: {absent}"

    forbidden = (
        "requires a new explicit user decision after the stopped validation block",
        "escalate `429` immediately",
        "A persistent infrastructure failure returns one",
        "stops the current block and callbacks the coordinator",
        "ask one necessary question when the fields cannot be",
    )
    present = [term for term in forbidden if term in joined]
    assert not present, f"stale over-blocking rules remain: {present}"

    events = (
        "missing_region_universal",
        "network_timeout",
        "chrome_disconnect",
        "empty_candidates",
        "route_client_block",
        "single_lane_failure",
        "uncertain_mutation",
        "timed_rate_limit",
        "prohibited_action",
        "persistent_captcha",
        "unrecoverable_login_mismatch",
        "explicit_account_lock",
        "sole_chrome_control_unavailable",
        "explicit_stop",
        "deadline",
    )
    scenarios = {event: classify(event) for event in events}

    for event in events[:9]:
        assert scenarios[event]["decision_required"] is False
        assert scenarios[event]["scope"] != "whole_mission"
    for event in events[9:13]:
        assert scenarios[event]["action"] == "HARD_BLOCKER"
        assert scenarios[event]["decision_required"] is True
    for event in ("explicit_stop", "deadline"):
        assert scenarios[event]["action"] == "TERMINAL_RELEASE"
        assert scenarios[event]["decision_required"] is False

    print(json.dumps({"status": "PASS", "scenarios": scenarios}, sort_keys=True))


if __name__ == "__main__":
    main()
