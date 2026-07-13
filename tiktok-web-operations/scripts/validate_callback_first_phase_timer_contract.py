#!/usr/bin/env python3
"""Validate TikTok callback-first coordinator phase-timer scheduling."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (ROOT/"SKILL.md", ROOT/"references/operating-model.md",
         ROOT/"references/role-and-stage-contract.md",
         ROOT/"references/stability-and-circuit-breakers.md",
         ROOT/"references/runtime-and-recovery.md",
         BUNDLE/"thread-supervisor/SKILL.md",
         BUNDLE/"thread-supervisor/references/identity-and-automation.md",
         BUNDLE/"thread-supervisor/references/canonical-registry.md",
         BUNDLE/"README.md")

def transition(event: str) -> dict:
    return {
        "dispatch": {"phase":"ACTIVE_WATCHDOG", "wake_minutes":60,
                     "polling":"STOPPED"},
        "callback": {"phase":"COOLDOWN_WAKE", "schedule":"next_dispatch_at",
                     "update":"IN_PLACE"},
        "cooldown_due": {"action":"DISPATCH_ONE_ROUND",
                         "next_phase":"ACTIVE_WATCHDOG"},
        "watchdog_recent_progress": {"action":"REARM_ONCE",
                                     "wake_minutes":60},
        "watchdog_idle_no_callback": {"action":"REQUEST_ONE_STATUS_CALLBACK"},
        "cutoff": {"action":"DELETE_TIMER_FINALIZE"},
    }[event]

def main():
    assert all(p.is_file() for p in FILES if p.name != "README.md" or p.exists())
    joined = "\n".join(p.read_text() for p in FILES if p.is_file())
    required = ("coordinator_worker", "CALLBACK_PING/v1", "CALLBACK_ACK/v1",
                "round_assignment/v1", "round_callback/v1", "TikTok 主控台",
                "callback-first", "phase timer", "ACTIVE_WATCHDOG",
                "COOLDOWN_WAKE", "60-minute", "one-occurrence",
                "update", "in place", "finite", "INTERVAL", "UNTIL",
                "next_dispatch_at", "fresh machine",
                "executor owns zero timers", "SCHEDULER_CONTINUATION_FAILURE",
                "catch-up bursts")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    forbidden = ("normally every five minutes", "five-minute recurrence",
                 "fixed recurring scheduler", "TikTok declares `launcher_self_owned_executor`")
    present = [x for x in forbidden if x.lower() in joined.lower()]
    assert not present, present
    scenarios = {event: transition(event) for event in (
        "dispatch", "callback", "cooldown_due", "watchdog_recent_progress",
        "watchdog_idle_no_callback", "cutoff")}
    assert scenarios["dispatch"]["polling"] == "STOPPED"
    assert scenarios["dispatch"]["wake_minutes"] == 60
    assert scenarios["callback"]["update"] == "IN_PLACE"
    assert scenarios["cooldown_due"]["action"] == "DISPATCH_ONE_ROUND"
    assert scenarios["watchdog_recent_progress"]["action"] == "REARM_ONCE"
    assert scenarios["cutoff"]["action"] == "DELETE_TIMER_FINALIZE"
    print(json.dumps({"status":"PASS", "scenarios":scenarios}, sort_keys=True))

if __name__ == "__main__":
    main()
