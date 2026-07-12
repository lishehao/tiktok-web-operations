#!/usr/bin/env python3
"""Validate TikTok fresh-only dispatch and no historical owner recovery."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (BUNDLE/"README.md", ROOT/"SKILL.md",
         ROOT/"references/operating-model.md", ROOT/"references/startup-health-check.md",
         BUNDLE/"thread-supervisor/SKILL.md",
         BUNDLE/"thread-supervisor/references/identity-and-automation.md")

def dispatch(event):
    table = {
        "old_title_match": {"old":"IGNORED_UNTOUCHED","create_attempts":1,"use_old":False},
        "old_archived": {"old":"IGNORED_UNTOUCHED","create_attempts":1,"use_old":False},
        "old_live": {"old":"IGNORED_UNTOUCHED","create_attempts":1,"use_old":False},
        "fresh_success": {"old":"NOT_INSPECTED","create_attempts":1,"use_old":False,"result":"USE_EXACT_NEW_ID"},
        "fresh_create_failed": {"old":"NOT_INSPECTED","create_attempts":1,"use_old":False,"result":"FRESH_TASK_CREATION_FAILED"},
        "fresh_create_unknown": {"old":"NOT_INSPECTED","create_attempts":1,"use_old":False,"result":"FRESH_TASK_CREATION_UNKNOWN"},
        "fresh_assignment_failed": {"old":"NOT_INSPECTED","create_attempts":1,"use_old":False,"result":"FRESH_TASK_ASSIGNMENT_FAILED"},
    }
    return table[event]

def main():
    assert all(p.is_file() for p in FILES)
    joined = "\n".join(p.read_text() for p in FILES)
    required = ("fresh_only_dispatch", "exactly once", "FRESH_TASK_CREATION_FAILED",
                "FRESH_TASK_CREATION_UNKNOWN", "FRESH_TASK_ASSIGNMENT_FAILED",
                "same-title", "archived", "currently live", "remain untouched history",
                "do not list", "do not retry creation", "do not fall back")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    forbidden = ("at most one clean replacement", "STALE_OWNER_TOMBSTONE",
                 "LIVENESS_UNVERIFIED_TRANSIENT", "automatically unarchived")
    present = [x for x in forbidden if x in joined]
    assert not present, present
    events = ("old_title_match","old_archived","old_live","fresh_success",
              "fresh_create_failed","fresh_create_unknown","fresh_assignment_failed")
    scenarios = {e: dispatch(e) for e in events}
    assert all(s["create_attempts"] == 1 for s in scenarios.values())
    assert all(s["use_old"] is False for s in scenarios.values())
    assert scenarios["fresh_success"]["result"] == "USE_EXACT_NEW_ID"
    print(json.dumps({"status":"PASS","scenarios":scenarios}, sort_keys=True))

if __name__ == "__main__": main()
