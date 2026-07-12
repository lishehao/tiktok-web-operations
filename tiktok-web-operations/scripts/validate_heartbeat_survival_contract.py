#!/usr/bin/env python3
"""Validate durable Heartbeat survival and continuous-mission scenarios."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (
    ROOT / "SKILL.md",
    ROOT / "references/operating-model.md",
    ROOT / "references/role-and-stage-contract.md",
    ROOT / "references/runtime-and-recovery.md",
    ROOT / "references/stability-and-circuit-breakers.md",
    ROOT / "references/startup-health-check.md",
    ROOT / "references/persistent-feed-operations.md",
    BUNDLE / "thread-supervisor/SKILL.md",
    BUNDLE / "thread-supervisor/references/identity-and-automation.md",
)


def timer_policy(event: str) -> dict[str, object]:
    technical = {
        "network_timeout",
        "err_blocked_by_client",
        "route_fault",
        "chrome_disconnect",
        "blank_renderer",
        "feed_transition_failure",
        "lane_persistence_failure",
    }
    if event in technical:
        return {
            "coordinator": "KEEP_REPEAT_ON",
            "retry": "AUTO_RECHECK_ON_LATER_WAKE",
            "affected_scope": "LANE_OR_SURFACE_ONLY",
        }
    if event == "mutation_uncertain":
        return {
            "coordinator": "KEEP_REPEAT_ON",
            "retry": "NEVER_RETRY_UNCERTAIN_SUBMISSION",
            "affected_scope": "EXACT_ACTION_OR_LANE",
        }
    if event == "misbound_timer":
        return {
            "coordinator": "REPLACE_NO_GAP",
            "retry": "CREATE_VERIFY_SWITCH_THEN_RETIRE_OLD",
            "affected_scope": "SCHEDULER_BINDING",
        }
    if event in {"user_stop", "deadline", "objective_complete"}:
        return {
            "coordinator": "KEEP_UNTIL_EXECUTOR_RELEASED",
            "retry": "TERMINAL_RELEASE_THEN_RETIRE",
            "affected_scope": "WHOLE_RUN",
        }
    if event == "executor_released":
        return {
            "coordinator": "RETIRE",
            "retry": "NONE",
            "affected_scope": "WHOLE_RUN",
        }
    raise ValueError(event)


def main() -> None:
    missing = [str(path) for path in FILES if not path.is_file()]
    assert not missing, f"missing contract files: {missing}"
    joined = "\n".join(path.read_text() for path in FILES)
    domain_joined = "\n".join(
        path.read_text() for path in FILES if ROOT in path.parents or path == ROOT / "SKILL.md"
    )

    required = (
        "Heartbeat survival invariant",
        "failure -> delete Heartbeat",
        "callback-driven",
        "coordinator_heartbeat",
        "no executor-targeted operation Heartbeat",
        "auto_resume_condition",
        "never retries an uncertain submission",
        "create and read back the correct replacement first",
        "switch the registry binding",
        "terminal executor release",
        "operation_stop_at",
        "9–15 qualified search views",
        "20–30 new qualified views",
        "not Codex turns, Heartbeat slots, or fixed-minute promises",
    )
    absent = [term for term in required if term not in joined]
    assert not absent, f"missing Heartbeat/mission assertions: {absent}"

    forbidden = (
        "one bounded block per slot",
        "Run exactly one bounded block per executor wake/turn",
        "creates two long-running repeat-on Heartbeats",
        "targetThreadId=executor_thread_id",
        "pause scheduled continuation without touching Chrome",
        "delete that exact automation immediately",
    )
    present = [term for term in forbidden if term in domain_joined]
    assert not present, f"stale scheduler semantics remain: {present}"

    events = (
        "network_timeout",
        "err_blocked_by_client",
        "route_fault",
        "chrome_disconnect",
        "blank_renderer",
        "feed_transition_failure",
        "lane_persistence_failure",
        "mutation_uncertain",
        "misbound_timer",
        "user_stop",
        "deadline",
        "objective_complete",
        "executor_released",
    )
    scenarios = {event: timer_policy(event) for event in events}

    for event in events[:7]:
        assert scenarios[event]["coordinator"] == "KEEP_REPEAT_ON"
        assert scenarios[event]["retry"] == "AUTO_RECHECK_ON_LATER_WAKE"
    assert scenarios["mutation_uncertain"]["retry"] == "NEVER_RETRY_UNCERTAIN_SUBMISSION"
    assert scenarios["misbound_timer"]["retry"] == "CREATE_VERIFY_SWITCH_THEN_RETIRE_OLD"
    for event in ("user_stop", "deadline", "objective_complete"):
        assert scenarios[event]["coordinator"] == "KEEP_UNTIL_EXECUTOR_RELEASED"
    assert scenarios["executor_released"]["coordinator"] == "RETIRE"

    print(json.dumps({"status": "PASS", "scenarios": scenarios}, sort_keys=True))


if __name__ == "__main__":
    main()
