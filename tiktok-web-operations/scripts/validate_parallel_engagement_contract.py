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

def decide(*, qualified: bool, verified: bool, fitting: bool) -> str:
    if not qualified: return "NO_ACTION_NOT_QUALIFIED"
    if not verified: return "GATE_OR_SKIP_LANE"
    if not fitting: return "NO_ACTION_EXACT_REASON"
    return "ACT_BEFORE_NAVIGATE_AWAY"

def main():
    assert all(p.is_file() for p in FILES)
    joined = " ".join("\n".join(p.read_text() for p in FILES).split())
    required = ("parallel_engagement=true", "Like", "Favorite", "Repost",
                "proactive comment", "four independent", "before navigating away",
                "do not defer engagement to a separate post-view phase",
                "does not mean mechanically applying all four",
                "each verified lane at least once", "exact no-action reason")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    scenarios = {
        "qualified_verified_fitting": decide(qualified=True, verified=True, fitting=True),
        "not_qualified": decide(qualified=False, verified=True, fitting=True),
        "gate_pending": decide(qualified=True, verified=False, fitting=True),
        "not_fitting": decide(qualified=True, verified=True, fitting=False),
    }
    assert scenarios["qualified_verified_fitting"] == "ACT_BEFORE_NAVIGATE_AWAY"
    assert scenarios["gate_pending"] == "GATE_OR_SKIP_LANE"
    print(json.dumps({"status":"PASS","lanes":["like","favorite","repost","comment"],"scenarios":scenarios}, sort_keys=True))

if __name__ == "__main__": main()
