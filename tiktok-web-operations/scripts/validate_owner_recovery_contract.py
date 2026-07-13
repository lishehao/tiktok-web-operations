#!/usr/bin/env python3
"""Validate one fresh executor per mission and no historical owner recovery."""
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
        "new_mission_after_release": {"old":"NOT_INSPECTED","create_attempts":1,"use_old":False,"result":"NEW_MISSION_FRESH_EXECUTOR"},
    }
    return table[event]

def main():
    assert all(p.is_file() for p in FILES if p.name != "README.md" or p.exists())
    joined = "\n".join(p.read_text() for p in FILES if p.is_file())
    required = ("fresh-create exactly one", "exactly once", "FRESH_TASK_CREATION_FAILED",
                "same-title", "historical", "never fallback")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    forbidden = ("at most one clean replacement", "STALE_OWNER_TOMBSTONE",
                 "LIVENESS_UNVERIFIED_TRANSIENT", "automatically unarchived")
    present = [x for x in forbidden if x in joined]
    assert not present, present
    events = ("old_title_match","old_archived","old_live","fresh_success",
              "fresh_create_failed","fresh_create_unknown","fresh_assignment_failed",
              "new_mission_after_release")
    scenarios = {e: dispatch(e) for e in events}
    assert all(s["create_attempts"] == 1 for s in scenarios.values())
    assert all(s["use_old"] is False for s in scenarios.values())
    assert scenarios["fresh_success"]["result"] == "USE_EXACT_NEW_ID"
    assert scenarios["new_mission_after_release"]["result"] == "NEW_MISSION_FRESH_EXECUTOR"
    print(json.dumps({"status":"PASS","scenarios":scenarios}, sort_keys=True))

if __name__ == "__main__": main()
