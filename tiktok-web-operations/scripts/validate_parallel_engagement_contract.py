#!/usr/bin/env python3
"""Validate that engagement runs inside qualified-video viewing."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (BUNDLE/"README.md", ROOT/"SKILL.md",
         ROOT/"references/persistent-feed-operations.md",
         ROOT/"references/engagement-and-analytics.md",
         ROOT/"references/startup-health-check.md")

def decide(*, qualified: bool, available: bool, fitting: bool) -> str:
    if not qualified: return "NO_ACTION_NOT_QUALIFIED"
    if not available: return "UNAVAILABLE"
    if not fitting: return "NO_ACTION_EXACT_REASON"
    return "ATTEMPT_ONCE_BEFORE_NAVIGATE_AWAY"

def main():
    assert all(p.is_file() for p in FILES if p.name != "README.md" or p.exists())
    joined = " ".join("\n".join(p.read_text() for p in FILES if p.is_file()).split())
    required = ("parallel_engagement=true", "Like", "Favorite", "Repost",
                "proactive comment", "four independent", "before navigating away",
                "do not defer engagement to a separate post-view phase",
                "does not mean mechanically applying all four", "best_effort_attempt",
                "attempts each lane at least once", "attempted | unavailable | hard_blocked",
                "do not perform post-action waiting")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    scenarios = {
        "qualified_available_fitting": decide(qualified=True, available=True, fitting=True),
        "not_qualified": decide(qualified=False, available=True, fitting=True),
        "control_unavailable": decide(qualified=True, available=False, fitting=True),
        "not_fitting": decide(qualified=True, available=True, fitting=False),
    }
    assert scenarios["qualified_available_fitting"] == "ATTEMPT_ONCE_BEFORE_NAVIGATE_AWAY"
    assert scenarios["control_unavailable"] == "UNAVAILABLE"
    print(json.dumps({"status":"PASS","lanes":["like","favorite","repost","comment"],"scenarios":scenarios}, sort_keys=True))

if __name__ == "__main__": main()
