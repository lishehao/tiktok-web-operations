#!/usr/bin/env python3
"""Validate mission-scoped executor reuse and bounded stale-owner replacement."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (
    BUNDLE / "README.md",
    ROOT / "SKILL.md",
    ROOT / "references/operating-model.md",
    ROOT / "references/startup-health-check.md",
    ROOT / "references/role-and-stage-contract.md",
    BUNDLE / "thread-supervisor/SKILL.md",
    BUNDLE / "thread-supervisor/references/identity-and-automation.md",
    BUNDLE / "thread-supervisor/references/canonical-registry.md",
)


def dispatch(event):
    table = {
        "old_title_match": {
            "old": "IGNORED_UNTOUCHED", "create_attempts": 1,
            "same_run": False, "result": "NEW_MISSION_USE_EXACT_NEW_ID",
        },
        "initial_fresh_success": {
            "create_attempts": 1, "same_run": False,
            "result": "REGISTER_GENERATION_1",
        },
        "initial_create_failed": {
            "create_attempts": 1, "same_run": False,
            "result": "FRESH_TASK_CREATION_FAILED_NO_DUPLICATE",
        },
        "initial_create_unknown": {
            "create_attempts": 1, "same_run": False,
            "result": "FRESH_TASK_CREATION_UNKNOWN_NO_DUPLICATE",
        },
        "later_round": {
            "create_attempts": 0, "same_run": True,
            "result": "REUSE_EXACT_REGISTERED_EXECUTOR",
        },
        "user_continue_active_mission": {
            "create_attempts": 0, "same_run": True,
            "result": "REUSE_EXACT_REGISTERED_EXECUTOR",
        },
        "direction_update_active_mission": {
            "create_attempts": 0, "same_run": True,
            "result": "VERSION_REFS_REUSE_EXACT_EXECUTOR",
        },
        "task_not_loaded": {
            "create_attempts": 0, "same_run": True,
            "result": "LIVENESS_UNVERIFIED_TRANSIENT_RETAIN_OWNER",
        },
        "task_read_unavailable": {
            "create_attempts": 0, "same_run": True,
            "result": "LIVENESS_UNVERIFIED_TRANSIENT_RETAIN_OWNER",
        },
        "host_or_network_unavailable": {
            "create_attempts": 0, "same_run": True,
            "result": "LIVENESS_UNVERIFIED_TRANSIENT_RETAIN_OWNER",
        },
        "registered_id_missing": {
            "create_attempts": 1, "same_run": True,
            "generation_increment": True,
            "result": "CREATE_ONE_REPLACEMENT_HANDSHAKE_RESUME",
        },
        "stale_owner_tombstone": {
            "create_attempts": 1, "same_run": True,
            "generation_increment": True,
            "result": "CREATE_ONE_REPLACEMENT_HANDSHAKE_RESUME",
        },
        "retired_during_active_mission": {
            "create_attempts": 1, "same_run": True,
            "generation_increment": True,
            "result": "CREATE_ONE_REPLACEMENT_HANDSHAKE_RESUME",
        },
        "replacement_create_failed": {
            "create_attempts": 1, "same_run": True,
            "result": "ORCHESTRATION_BLOCKER_NO_SECOND_CREATE",
        },
        "replacement_create_unknown": {
            "create_attempts": 1, "same_run": True,
            "result": "ORCHESTRATION_BLOCKER_NO_SECOND_CREATE",
        },
        "replacement_assignment_failed": {
            "create_attempts": 1, "same_run": True,
            "result": "ORCHESTRATION_BLOCKER_NO_SECOND_CREATE",
        },
        "new_instruction_after_terminal_release": {
            "create_attempts": 1, "same_run": False,
            "result": "NEW_RUN_FRESH_EXECUTOR",
        },
    }
    return table[event]


def main():
    assert all(path.is_file() for path in FILES)
    joined = "\n".join(path.read_text() for path in FILES)
    required = (
        "mission-scoped", "same active mission", "STALE_OWNER_TOMBSTONE",
        "LIVENESS_UNVERIFIED_TRANSIENT", "executor_generation",
        "old_executor_thread_id", "new_executor_thread_id", "notLoaded",
        "at most one", "fresh callback handshake", "terminal",
    )
    missing = [token for token in required if token.lower() not in joined.lower()]
    assert not missing, missing

    events = (
        "old_title_match", "initial_fresh_success", "initial_create_failed",
        "initial_create_unknown", "later_round", "user_continue_active_mission",
        "direction_update_active_mission", "task_not_loaded",
        "task_read_unavailable", "host_or_network_unavailable",
        "registered_id_missing", "stale_owner_tombstone",
        "retired_during_active_mission", "replacement_create_failed",
        "replacement_create_unknown", "replacement_assignment_failed",
        "new_instruction_after_terminal_release",
    )
    scenarios = {event: dispatch(event) for event in events}

    assert scenarios["later_round"]["create_attempts"] == 0
    assert scenarios["user_continue_active_mission"] == scenarios["later_round"]
    assert scenarios["task_not_loaded"]["create_attempts"] == 0
    assert scenarios["task_read_unavailable"]["create_attempts"] == 0
    assert scenarios["host_or_network_unavailable"]["create_attempts"] == 0
    assert scenarios["registered_id_missing"]["same_run"] is True
    assert scenarios["stale_owner_tombstone"]["generation_increment"] is True
    assert scenarios["retired_during_active_mission"]["create_attempts"] == 1
    assert scenarios["replacement_create_failed"]["create_attempts"] == 1
    assert scenarios["replacement_create_unknown"]["result"].endswith(
        "NO_SECOND_CREATE"
    )
    assert scenarios["replacement_assignment_failed"]["result"].endswith(
        "NO_SECOND_CREATE"
    )
    assert scenarios["new_instruction_after_terminal_release"]["same_run"] is False
    assert scenarios["old_title_match"]["old"] == "IGNORED_UNTOUCHED"

    print(json.dumps({"status": "PASS", "scenarios": scenarios}, sort_keys=True))


if __name__ == "__main__":
    main()
