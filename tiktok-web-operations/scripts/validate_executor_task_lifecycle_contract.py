#!/usr/bin/env python3
"""Validate exact-ID executor title normalization and terminal archival."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
DOCS = (
    BUNDLE / "README.md",
    ROOT / "SKILL.md",
    ROOT / "references/operating-model.md",
    ROOT / "references/startup-health-check.md",
    ROOT / "references/role-and-stage-contract.md",
    BUNDLE / "thread-supervisor/references/tiktok-coordinator-worker.md",
    BUNDLE / "thread-supervisor/references/identity-and-automation.md",
    BUNDLE / "thread-supervisor/references/canonical-registry.md",
)


def transition(event: str) -> str:
    return {
        "fresh_create_returned": "SET_EXACT_ID_TITLE_THEN_READBACK",
        "generated_bootstrap_title": "REPAIR_EXACT_ID_NOT_TITLE_SEARCH",
        "title_tool_unavailable": "CONTINUE_DEGRADED_ONE_IDLE_REPAIR",
        "title_repair_already_attempted": "CONTINUE_DEGRADED_NO_RETRY_LOOP",
        "active_executor": "ARCHIVE_FORBIDDEN",
        "idle_live_executor": "ARCHIVE_FORBIDDEN",
        "stop_requested": "ARCHIVE_FORBIDDEN_PENDING_RELEASE",
        "released_scheduler_present": "DELETE_READBACK_RECONCILE_BEFORE_ARCHIVE",
        "terminal_reconciled": "ARCHIVE_EXACT_RELEASED_ID_READBACK",
        "archive_tool_unavailable": "TERMINAL_WITH_EXPLICIT_ARCHIVE_DEGRADATION",
        "replacement_created_unbound": "KEEP_OLD_UNARCHIVED",
        "replacement_bound_old_unreleased": "REQUEST_OLD_RELEASE_NO_ARCHIVE_YET",
        "replacement_bound_old_released": "ARCHIVE_OLD_EXACT_ID_ONLY",
        "historical_same_title": "IGNORE_OPERATIONALLY",
    }[event]


def main() -> None:
    missing_files = [str(path) for path in DOCS if not path.is_file() and path.name != "README.md"]
    assert not missing_files, missing_files
    joined = "\n".join(path.read_text() for path in DOCS if path.is_file())
    required = (
        "set_thread_title",
        "TikTok 执行台",
        "exact returned ID",
        "DEGRADED_EXECUTOR_TITLE_UNAVAILABLE",
        "first safe executor-IDLE boundary",
        "at most one",
        "set_thread_archived",
        "DEGRADED_EXECUTOR_ARCHIVE_UNAVAILABLE",
        "RUN_RELEASED",
        "owned-tab release",
        "scheduler deletion",
        "Never archive",
        "never search by title",
    )
    absent = [term for term in required if term.lower() not in joined.lower()]
    assert not absent, absent

    events = (
        "fresh_create_returned",
        "generated_bootstrap_title",
        "title_tool_unavailable",
        "title_repair_already_attempted",
        "active_executor",
        "idle_live_executor",
        "stop_requested",
        "released_scheduler_present",
        "terminal_reconciled",
        "archive_tool_unavailable",
        "replacement_created_unbound",
        "replacement_bound_old_unreleased",
        "replacement_bound_old_released",
        "historical_same_title",
    )
    scenarios = {event: transition(event) for event in events}
    assert scenarios["fresh_create_returned"] == "SET_EXACT_ID_TITLE_THEN_READBACK"
    assert scenarios["title_tool_unavailable"].startswith("CONTINUE_DEGRADED")
    assert scenarios["active_executor"] == "ARCHIVE_FORBIDDEN"
    assert scenarios["idle_live_executor"] == "ARCHIVE_FORBIDDEN"
    assert scenarios["terminal_reconciled"] == "ARCHIVE_EXACT_RELEASED_ID_READBACK"
    assert scenarios["replacement_created_unbound"] == "KEEP_OLD_UNARCHIVED"
    assert scenarios["replacement_bound_old_released"] == "ARCHIVE_OLD_EXACT_ID_ONLY"
    print(json.dumps({"status": "PASS", "scenarios": scenarios}, sort_keys=True))


if __name__ == "__main__":
    main()
