#!/usr/bin/env python3
"""Static assertions and isolated scenarios for persistent-owner recovery rules."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
IDENTITY = ROOT / "thread-supervisor/references/identity-and-automation.md"
OPERATING = ROOT / "tiktok-web-operations/references/operating-model.md"
SKILL = ROOT / "tiktok-web-operations/SKILL.md"
README = ROOT / "README.md"


def classify_owner(*, archived: bool = False, error: str = "", ack: bool = False) -> str:
    if archived:
        return "ARCHIVED_RETIRED"
    lowered = error.lower()
    missing_rollout = "failed to resolve rollout path" in lowered and (
        "file does not exist" in lowered or "enoent" in lowered
    )
    if missing_rollout:
        return "STALE_OWNER_TOMBSTONE"
    transient = any(
        marker in lowered
        for marker in (
            "host unavailable",
            "unavailable host",
            "timeout",
            "timed out",
            "connection reset",
            "network",
            "transport",
            "temporarily unavailable",
        )
    )
    if transient:
        return "LIVENESS_UNVERIFIED_TRANSIENT"
    if ack:
        return "LIVE"
    return "CANDIDATE_ONLY"


def recovery_plan(state: str) -> dict[str, object]:
    if state == "STALE_OWNER_TOMBSTONE":
        return {
            "resend_old": False,
            "unarchive_old": False,
            "replacement_count": 1,
            "required_checks": [
                "remove_old_target_automation",
                "record_old_new_ids",
                "verify_new_mission_dispatch",
                "verify_new_automation_binding",
                "orphan_automation_check",
                "duplicate_canonical_owner_check",
            ],
        }
    if state == "LIVENESS_UNVERIFIED_TRANSIENT":
        return {
            "resend_old": False,
            "unarchive_old": False,
            "replacement_count": 0,
            "required_checks": ["bounded_transport_recheck"],
        }
    if state == "ARCHIVED_RETIRED":
        return {
            "resend_old": False,
            "unarchive_old": False,
            "replacement_count": 0,
            "required_checks": ["keep_retired"],
        }
    if state == "LIVE":
        return {
            "resend_old": False,
            "unarchive_old": False,
            "replacement_count": 0,
            "required_checks": ["dispatch_exact_id"],
        }
    return {
        "resend_old": False,
        "unarchive_old": False,
        "replacement_count": 0,
        "required_checks": ["owner_liveness_probe"],
    }


def main() -> None:
    documents = {
        "identity": IDENTITY.read_text(),
        "operating": OPERATING.read_text(),
        "skill": SKILL.read_text(),
        "readme": README.read_text(),
    }
    joined = "\n".join(documents.values())

    required = (
        "STALE_OWNER_TOMBSTONE",
        "LIVENESS_UNVERIFIED_TRANSIENT",
        "failed to resolve rollout path",
        "file does not exist",
        "ARCHIVED_RETIRED",
        "replacement_old_executor_thread_id",
        "replacement_new_executor_thread_id",
        "replacement_mission_dispatch_id",
        "replacement_operation_heartbeat_id",
        "orphan_automation_check",
        "duplicate_canonical_owner_check",
        "at most one replacement",
        "without user confirmation",
    )
    missing = [term for term in required if term not in joined]
    assert not missing, f"missing semantic assertions: {missing}"
    assert "Create a replacement only with explicit user authorization" not in joined
    assert "automatically unarchive it for reuse" in joined

    scenarios = {
        "title_summary_only": classify_owner(),
        "archived_executor": classify_owner(archived=True),
        "missing_rollout": classify_owner(
            error="failed to resolve rollout path /tmp/rollout.jsonl: file does not exist"
        ),
        "missing_rollout_enoent": classify_owner(
            error="failed to resolve rollout path: ENOENT"
        ),
        "host_unavailable": classify_owner(error="host unavailable"),
        "network_timeout": classify_owner(error="network transport timed out"),
        "live_ack": classify_owner(ack=True),
    }
    expected = {
        "title_summary_only": "CANDIDATE_ONLY",
        "archived_executor": "ARCHIVED_RETIRED",
        "missing_rollout": "STALE_OWNER_TOMBSTONE",
        "missing_rollout_enoent": "STALE_OWNER_TOMBSTONE",
        "host_unavailable": "LIVENESS_UNVERIFIED_TRANSIENT",
        "network_timeout": "LIVENESS_UNVERIFIED_TRANSIENT",
        "live_ack": "LIVE",
    }
    assert scenarios == expected, {"actual": scenarios, "expected": expected}
    plans = {name: recovery_plan(state) for name, state in scenarios.items()}
    assert plans["missing_rollout"]["replacement_count"] == 1
    assert plans["missing_rollout"]["resend_old"] is False
    assert plans["host_unavailable"]["replacement_count"] == 0
    assert plans["network_timeout"]["replacement_count"] == 0
    assert plans["archived_executor"]["unarchive_old"] is False
    assert "verify_new_automation_binding" in plans["missing_rollout"]["required_checks"]
    assert "duplicate_canonical_owner_check" in plans["missing_rollout"]["required_checks"]
    print(
        json.dumps(
            {"status": "PASS", "scenarios": scenarios, "plans": plans},
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
