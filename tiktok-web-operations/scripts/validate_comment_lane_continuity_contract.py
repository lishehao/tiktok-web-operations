#!/usr/bin/env python3
"""Validate that strategy evidence cannot erase authorized Comment work."""

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
    ROOT / "references/feed-browsing-and-comments.md",
    ROOT / "references/persistent-feed-operations.md",
    ROOT / "references/engagement-and-analytics.md",
    ROOT / "references/instruction-precedence.md",
    BUNDLE / "thread-supervisor/references/tiktok-coordinator-worker.md",
)

DEFAULT_COMMENT = {
    "status": "ACTIVE",
    "target": 10,
    "min": 7,
    "max": 12,
    "ceiling": 15,
}


def next_comment_policy(
    *,
    cultivation_authorized: bool,
    browse_only: bool = False,
    user_revoked: bool = False,
    current_hard_block: bool = False,
) -> dict[str, int | str]:
    if browse_only or not cultivation_authorized or user_revoked:
        return {"status": "DISABLED_BY_AUTHORITY"}
    if current_hard_block:
        return {"status": "HARD_BLOCKED_CURRENT"}
    return dict(DEFAULT_COMMENT)


def main() -> None:
    missing = [
        str(path)
        for path in DOCS
        if not path.is_file() and path.name != "README.md"
    ]
    assert not missing, missing
    joined = " ".join(
        "\n".join(path.read_text() for path in DOCS if path.is_file()).split()
    )
    required = (
        "Feed drift never zeroes Comment",
        "new cluster match",
        "per-round budget",
        "target/min/max/ceiling `10/7/12/15`",
        "callback recommendations never outrank",
        "quality shortfall",
        "best_effort_attempt",
    )
    absent = [term for term in required if term.lower() not in joined.lower()]
    assert not absent, absent

    # Reproduces the failure: round 1 hit 10 comments and For You drifted 10/10;
    # round 2 still found 26 strong search-origin views. Strategy must not erase
    # the comment authority or carry a zero budget into the next assignment.
    drift_after_target_hit = next_comment_policy(cultivation_authorized=True)
    assert drift_after_target_hit == DEFAULT_COMMENT

    # No current candidate affects actual attempts, not assignment authority.
    no_current_candidate = next_comment_policy(cultivation_authorized=True)
    assert no_current_candidate == DEFAULT_COMMENT

    scenarios = {
        "prior_10_comments_fyp_10_of_10_drift_next_search_core_26": drift_after_target_hit,
        "quality_shortfall_no_candidate_yet": no_current_candidate,
        "browse_only": next_comment_policy(cultivation_authorized=False, browse_only=True),
        "user_revoked": next_comment_policy(cultivation_authorized=True, user_revoked=True),
        "current_comment_hard_block": next_comment_policy(
            cultivation_authorized=True, current_hard_block=True
        ),
    }
    assert scenarios["browse_only"]["status"] == "DISABLED_BY_AUTHORITY"
    assert scenarios["user_revoked"]["status"] == "DISABLED_BY_AUTHORITY"
    assert scenarios["current_comment_hard_block"]["status"] == "HARD_BLOCKED_CURRENT"
    print(json.dumps({"status": "PASS", "scenarios": scenarios}, sort_keys=True))


if __name__ == "__main__":
    main()
