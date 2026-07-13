#!/usr/bin/env python3
"""Validate comment weighting, bounded meme research, and originality."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (BUNDLE/"README.md", ROOT/"SKILL.md",
         ROOT/"references/feed-browsing-and-comments.md",
         ROOT/"references/persistent-feed-operations.md",
         ROOT/"references/engagement-and-analytics.md")

def comment_plan(strong_candidates: int) -> dict[str, int | str]:
    attempts = min(strong_candidates, 8)
    return {
        "attempts": attempts,
        "status": "QUALITY_SHORTFALL" if attempts < 4 else "IN_RANGE",
    }

def main():
    assert all(p.is_file() for p in FILES if p.name != "README.md" or p.exists())
    joined = " ".join("\n".join(p.read_text() for p in FILES if p.is_file()).split())
    required = ("highest-priority", "target 6", "4–8", "ceiling 10",
                "at most two focused", "Web Search", "visible live comment culture",
                "never copy", "original", "specificity", "context fit",
                "meme resonance", "brevity", "safety", "not proof")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    scenarios = {str(n): comment_plan(n) for n in (0, 3, 4, 6, 8, 12)}
    assert scenarios["3"]["status"] == "QUALITY_SHORTFALL"
    assert scenarios["4"]["status"] == "IN_RANGE"
    assert scenarios["12"]["attempts"] == 8
    print(json.dumps({"status":"PASS","target":6,"min":4,"max":8,
                      "absolute_ceiling":10,"web_search_max":2,
                      "scenarios":scenarios}, sort_keys=True))

if __name__ == "__main__": main()
