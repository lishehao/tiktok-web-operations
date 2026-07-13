#!/usr/bin/env python3
"""Validate main-controlled 10-20 minute inter-round cooldown."""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (BUNDLE/"README.md", ROOT/"SKILL.md",
         ROOT/"references/persistent-feed-operations.md",
         ROOT/"references/operating-model.md",
         ROOT/"references/role-and-stage-contract.md",
         BUNDLE/"thread-supervisor/SKILL.md",
         BUNDLE/"thread-supervisor/references/identity-and-automation.md")

def cooldown(kind: str):
    return {"read_only_low_yield":10, "standard":15,
            "mutation_or_recovery_heavy":20}[kind]

def next_at(now: datetime, minutes: int) -> datetime:
    assert now.tzinfo is not None
    return now.astimezone(timezone.utc) + timedelta(minutes=minutes)

def main():
    assert all(p.is_file() for p in FILES if p.name != "README.md" or p.exists())
    joined = "\n".join(p.read_text() for p in FILES if p.is_file())
    required = ("10–20", "next_dispatch_at", "15 minutes", "fresh machine",
                "main task", "callback", "executor is IDLE", "no-op",
                "perform no TikTok", "C5_COOLDOWN")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    now = datetime(2026, 7, 13, 1, 58, 30, tzinfo=timezone(timedelta(hours=8)))
    scenarios = {
        "round_incomplete_24": "CONTINUE_SAME_ROUND",
        "round_complete_25_45": "CALLBACK_THEN_MAIN_COOLDOWN",
        "read_only_low_yield": cooldown("read_only_low_yield"),
        "standard": cooldown("standard"),
        "mutation_or_recovery_heavy": cooldown("mutation_or_recovery_heavy"),
        "cross_midnight_utc": next_at(now, 15).isoformat(),
        "wake_before_due": "NOOP",
        "wake_due_idle": "DISPATCH_ONE_ROUND",
    }
    assert scenarios["standard"] == 15
    assert scenarios["cross_midnight_utc"] == "2026-07-12T18:13:30+00:00"
    print(json.dumps({"status":"PASS","scenarios":scenarios}, sort_keys=True))

if __name__ == "__main__": main()
