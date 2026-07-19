#!/usr/bin/env python3
"""Validate variable 35-target rounds with one boundary callback."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (BUNDLE/"README.md", ROOT/"SKILL.md",
         ROOT/"references/persistent-feed-operations.md",
         ROOT/"references/operating-model.md")

def boundary(count: int, natural: bool = False) -> str:
    if count < 25: return "CONTINUE"
    if count >= 45: return "CHECKPOINT_REQUIRED"
    if natural: return "CHECKPOINT_ALLOWED"
    return "CONTINUE_TOWARD_35"

def main():
    assert all(p.is_file() for p in FILES if p.name != "README.md" or p.exists())
    joined = " ".join("\n".join(p.read_text() for p in FILES if p.is_file()).split())
    required = ("targets 35 qualified", "25–45", "25–35", "5–10",
                "thumbnails", "duplicates", "do not count",
                "callback", "10–20 minute", "next_dispatch_at",
                "STRICT_QUALIFIED_VIEW_V2", "classified_sample")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    scenarios = {str(n): boundary(n, natural=(n in {25,35,44})) for n in (0,24,25,34,35,44,45,50)}
    assert scenarios["24"] == "CONTINUE"
    assert scenarios["25"] == "CHECKPOINT_ALLOWED"
    assert scenarios["35"] == "CHECKPOINT_ALLOWED"
    assert scenarios["45"] == "CHECKPOINT_REQUIRED"
    assert scenarios["50"] == "CHECKPOINT_REQUIRED"
    print(json.dumps({"status":"PASS","target":35,"min":25,"max":45,"scenarios":scenarios}, sort_keys=True))

if __name__ == "__main__": main()
