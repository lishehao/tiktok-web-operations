#!/usr/bin/env python3
"""Validate pre-handoff executor owner classification and independence."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (ROOT/"SKILL.md", ROOT/"references/operating-model.md",
         BUNDLE/"thread-supervisor/SKILL.md",
         BUNDLE/"thread-supervisor/references/identity-and-automation.md", BUNDLE/"README.md")

def classify(error="", archived=False, accepted=False):
    if archived: return "ARCHIVED_RETIRED"
    low = error.lower()
    if "failed to resolve rollout path" in low and ("file does not exist" in low or "enoent" in low):
        return "STALE_OWNER_TOMBSTONE"
    if any(x in low for x in ("host unavailable","timeout","network","transport")):
        return "LIVENESS_UNVERIFIED_TRANSIENT"
    if accepted: return "ASSIGNMENT_ACCEPTED"
    return "NEW"

def plan(state):
    if state == "STALE_OWNER_TOMBSTONE": return {"replacement_max":1,"recheck":False,"launcher_monitor_after":False}
    if state == "LIVENESS_UNVERIFIED_TRANSIENT": return {"replacement_max":0,"recheck":True,"launcher_monitor_after":False}
    return {"replacement_max":0,"recheck":False,"launcher_monitor_after":False}

def main():
    assert all(p.is_file() for p in FILES)
    joined = "\n".join(p.read_text() for p in FILES)
    required = ("STALE_OWNER_TOMBSTONE", "LIVENESS_UNVERIFIED_TRANSIENT",
                "failed to resolve rollout path", "file does not exist", "at most one clean replacement",
                "After accepted handoff the launcher is idle", "never automatically unarchived",
                "never list/read one another")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    scenarios = {
      "stale": classify("failed to resolve rollout path x: file does not exist"),
      "transient": classify("host unavailable timeout"),
      "archived": classify(archived=True), "accepted": classify(accepted=True)}
    plans = {k: plan(v) for k,v in scenarios.items()}
    assert plans["stale"]["replacement_max"] == 1
    assert plans["transient"]["replacement_max"] == 0
    assert not any(p["launcher_monitor_after"] for p in plans.values())
    print(json.dumps({"status":"PASS","scenarios":scenarios,"plans":plans}, sort_keys=True))

if __name__ == "__main__": main()
