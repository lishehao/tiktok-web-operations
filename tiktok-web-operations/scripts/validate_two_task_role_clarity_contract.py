#!/usr/bin/env python3
"""Validate single-job ownership for TikTok Main and Executor tasks."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
DOCS = (
    BUNDLE / "README.md",
    ROOT / "SKILL.md",
    ROOT / "references/operating-model.md",
    ROOT / "references/role-and-stage-contract.md",
    BUNDLE / "thread-supervisor/references/tiktok-coordinator-worker.md",
)


def owner(decision: str) -> str:
    main = {
        "profile", "mission", "direction", "authority", "next_clusters",
        "round_envelope", "cooldown", "heartbeat", "hard_repair", "finalize",
    }
    executor = {
        "exact_query", "exact_post", "watch_progression", "candidate_fit",
        "comment_text", "action_attempt", "within_round_recovery", "raw_evidence",
    }
    if decision in main:
        return "TIKTOK_COORDINATOR"
    if decision in executor:
        return "TIKTOK_EXECUTOR"
    raise ValueError(decision)


def main() -> None:
    missing = [
        str(path) for path in DOCS
        if not path.is_file() and path.name != "README.md"
    ]
    assert not missing, missing
    joined = " ".join(
        "\n".join(path.read_text() for path in DOCS if path.is_file()).split()
    )
    required = (
        "what the next bounded round is",
        "execute the assigned Chrome round",
        "observed facts",
        "non-binding",
        "never select exact posts",
        "never chooses or dispatches the next round",
        "one decision layer per task",
    )
    absent = [term for term in required if term.lower() not in joined.lower()]
    assert not absent, absent

    scenarios = {
        key: owner(key) for key in (
            "direction", "authority", "next_clusters", "cooldown", "heartbeat",
            "exact_query", "exact_post", "candidate_fit", "comment_text",
            "action_attempt", "within_round_recovery", "raw_evidence",
        )
    }
    assert scenarios["comment_text"] == "TIKTOK_EXECUTOR"
    assert scenarios["cooldown"] == "TIKTOK_COORDINATOR"
    assert scenarios["authority"] == "TIKTOK_COORDINATOR"
    assert scenarios["raw_evidence"] == "TIKTOK_EXECUTOR"
    print(json.dumps({
        "status": "PASS",
        "main_job": "DECIDE_WHAT_WHEN_OR_STOP",
        "executor_job": "EXECUTE_ONE_ROUND_RETURN_FACTS",
        "suggestions": "NON_BINDING",
        "scenarios": scenarios,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
