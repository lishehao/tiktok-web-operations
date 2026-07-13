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

def comment_plan(strong_openings: int) -> dict[str, int | str]:
    attempts = min(strong_openings, 12)
    return {
        "attempts": attempts,
        "status": "QUALITY_SHORTFALL" if attempts < 7 else "IN_RANGE",
    }

def same_video_plan(top_level: int, distinct_reply_openings: int) -> dict[str, int]:
    return {
        "top_level": min(top_level, 1),
        "replies": min(distinct_reply_openings, 2),
        "total": min(top_level, 1) + min(distinct_reply_openings, 2),
    }

def main():
    assert all(p.is_file() for p in FILES if p.name != "README.md" or p.exists())
    joined = " ".join("\n".join(p.read_text() for p in FILES if p.is_file()).split())
    required = ("highest-priority", "target 10", "7–12", "ceiling 15",
                "at most two focused", "Web Search", "visible live comment culture",
                "never copy", "original", "specificity", "context fit",
                "meme resonance", "brevity", "safety", "not proof",
                "at most one proactive top-level", "two replies",
                "distinct existing comments", "8–20")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    scenarios = {str(n): comment_plan(n) for n in (0, 6, 7, 10, 12, 20)}
    assert scenarios["6"]["status"] == "QUALITY_SHORTFALL"
    assert scenarios["7"]["status"] == "IN_RANGE"
    assert scenarios["20"]["attempts"] == 12
    same_video = same_video_plan(top_level=3, distinct_reply_openings=5)
    assert same_video == {"top_level": 1, "replies": 2, "total": 3}
    print(json.dumps({"status":"PASS","target":10,"min":7,"max":12,
                      "absolute_ceiling":15,"web_search_max":2,
                      "same_video":same_video,"scenarios":scenarios}, sort_keys=True))

if __name__ == "__main__": main()
