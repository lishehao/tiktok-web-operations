#!/usr/bin/env python3
"""Validate profile-alignment and account-strength operating objectives."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (
    BUNDLE / "README.md",
    ROOT / "SKILL.md",
    ROOT / "references/persistent-feed-operations.md",
    ROOT / "references/engagement-and-analytics.md",
    ROOT / "references/startup-health-check.md",
    ROOT / "references/operating-model.md",
    ROOT / "references/role-and-stage-contract.md",
)


def envelope(intent: str) -> dict[str, object]:
    if intent == "browse_only":
        return {"favorite": "disabled", "repost": "disabled", "comment": "disabled", "like": "disabled"}
    if intent == "cultivation":
        return {
            "favorite": "best_effort_attempt",
            "repost": "best_effort_attempt",
            "comment": "best_effort_attempt",
            "like": "best_effort_attempt",
            "parallel_engagement": True,
        }
    raise ValueError(intent)


def unit_action(*, candidate: bool, lane_verified: bool, safe: bool = True) -> str:
    if candidate and lane_verified and safe:
        return "USE_SMALLEST_GENUINE_SIGNAL"
    return "ZERO_WITH_EXACT_REASON"


def main() -> None:
    missing = [str(path) for path in FILES if not path.is_file() and path.name != "README.md"]
    assert not missing, f"missing objective contract files: {missing}"
    joined = "\n".join(path.read_text() for path in FILES if path.is_file())

    required = (
        "profile_alignment",
        "account_strength_proxy",
        "best_effort_attempt",
        "Favorite",
        "TikTok Repost",
        "proactive comment",
        "parallel_engagement=true",
        "mutation_allowed=false",
        "Zero outward actions is valid only when",
        "not proof of TikTok's private ranking weights",
    )
    absent = [term for term in required if term.lower() not in joined.lower()]
    assert not absent, f"missing dual-objective assertions: {absent}"

    forbidden = (
        "guarantees account weight",
        "every video must receive Favorite, Repost, and Comment",
        "must use all positive actions on every relevant post",
    )
    present = [term for term in forbidden if term in joined]
    assert not present, f"unsafe objective semantics remain: {present}"

    scenarios = {
        "browse_only": envelope("browse_only"),
        "cultivation": envelope("cultivation"),
        "verified_candidate": unit_action(candidate=True, lane_verified=True),
        "no_candidate": unit_action(candidate=False, lane_verified=True),
        "gate_unavailable": unit_action(candidate=True, lane_verified=False),
        "unsafe_candidate": unit_action(candidate=True, lane_verified=True, safe=False),
    }
    assert scenarios["browse_only"] == {
        "favorite": "disabled", "repost": "disabled", "comment": "disabled", "like": "disabled"
    }
    assert scenarios["cultivation"]["favorite"] == "best_effort_attempt"
    assert scenarios["cultivation"]["repost"] == "best_effort_attempt"
    assert scenarios["cultivation"]["comment"] == "best_effort_attempt"
    assert scenarios["cultivation"]["like"] == "best_effort_attempt"
    assert scenarios["cultivation"]["parallel_engagement"] is True
    assert scenarios["verified_candidate"] == "USE_SMALLEST_GENUINE_SIGNAL"
    assert scenarios["no_candidate"] == "ZERO_WITH_EXACT_REASON"
    assert scenarios["gate_unavailable"] == "ZERO_WITH_EXACT_REASON"
    assert scenarios["unsafe_candidate"] == "ZERO_WITH_EXACT_REASON"

    print(json.dumps({"status": "PASS", "scenarios": scenarios}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
