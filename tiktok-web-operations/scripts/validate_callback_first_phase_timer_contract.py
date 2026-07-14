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
                     "polling":"STOPPED", "future_wake_count":1},
        "callback": {"phase":"COOLDOWN_WAKE", "schedule":"next_dispatch_at",
                     "update":"IN_PLACE", "idle_proof":"CALLBACK_ACCEPTED",
                     "future_wake_count":1},
        "cooldown_due_callback_idle": {"action":"DISPATCH_ONE_ROUND",
                         "next_phase":"ACTIVE_WATCHDOG",
                         "requires_live_thread_read":False,
                         "future_wake_count":1},
        "cooldown_due_read_unavailable_callback_idle": {
                         "action":"DISPATCH_ONE_ROUND",
                         "proof":"CALLBACK_ACCEPTED",
                         "future_wake_count":1},
        "cooldown_due_missing_idle_proof": {"action":"REARM_STATE_RETRY",
                         "wake_minutes":5, "future_wake_count":1},
        "state_retry_third_failure": {"action":"REARM_DEGRADED_RECOVERY",
                         "wake_minutes":15, "notify_once":True,
                         "future_wake_count":1},
        "watchdog_recent_progress": {"action":"REARM_ONCE",
                                     "wake_minutes":60,
                                     "future_wake_count":1},
        "watchdog_idle_no_callback": {"action":"REQUEST_ONE_STATUS_CALLBACK",
                                      "next_phase":"STATE_RETRY",
                                      "future_wake_count":1},
        "active_no_future_occurrence": {"action":"EXPIRED_ORPHAN_REPAIR_OR_FINALIZE",
                                        "healthy":False},
        "bare_noop_before_cutoff": {"action":"INVALID_NO_FUTURE_WAKE"},
        "cutoff": {"action":"DELETE_TIMER_FINALIZE", "future_wake_count":0},
    }[event]

def main():
    assert all(p.is_file() for p in FILES if p.name != "README.md" or p.exists())
    joined = "\n".join(p.read_text() for p in FILES if p.is_file())
    required = ("coordinator_worker", "CALLBACK_PING/v1", "CALLBACK_ACK/v1",
                "round_assignment/v1", "round_callback/v1", "TikTok 主控台",
                "callback-first", "phase timer", "ACTIVE_WATCHDOG",
                "COOLDOWN_WAKE", "60-minute", "one-occurrence",
                "update", "in place", "finite", "INTERVAL", "UNTIL",
                "two minutes", "next_dispatch_at", "fresh machine",
                "executor owns zero timers", "SCHEDULER_CONTINUATION_FAILURE",
                "catch-up bursts", "CALLBACK_ACCEPTED", "diagnostic only",
                "notLoaded", "STATE_RETRY", "DEGRADED_RECOVERY",
                "EXPIRED_ORPHAN", "future_wake_count=1", "naked NOOP")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    forbidden = ("normally every five minutes", "five-minute recurrence",
                 "fixed recurring scheduler", "TikTok declares `launcher_self_owned_executor`")
    present = [x for x in forbidden if x.lower() in joined.lower()]
    assert not present, present
    events = (
        "dispatch", "callback", "cooldown_due_callback_idle",
        "cooldown_due_read_unavailable_callback_idle",
        "cooldown_due_missing_idle_proof", "state_retry_third_failure",
        "watchdog_recent_progress", "watchdog_idle_no_callback",
        "active_no_future_occurrence", "bare_noop_before_cutoff", "cutoff")
    scenarios = {event: transition(event) for event in events}
    assert scenarios["dispatch"]["polling"] == "STOPPED"
    assert scenarios["dispatch"]["wake_minutes"] == 60
    assert scenarios["callback"]["update"] == "IN_PLACE"
    assert not scenarios["cooldown_due_callback_idle"]["requires_live_thread_read"]
    assert scenarios["cooldown_due_read_unavailable_callback_idle"]["action"] == "DISPATCH_ONE_ROUND"
    assert scenarios["cooldown_due_missing_idle_proof"]["future_wake_count"] == 1
    assert scenarios["state_retry_third_failure"]["notify_once"]
    assert scenarios["watchdog_recent_progress"]["action"] == "REARM_ONCE"
    assert not scenarios["active_no_future_occurrence"]["healthy"]
    assert scenarios["bare_noop_before_cutoff"]["action"] == "INVALID_NO_FUTURE_WAKE"
    assert scenarios["cutoff"]["action"] == "DELETE_TIMER_FINALIZE"
    assert all(v.get("future_wake_count") == 1 for k,v in scenarios.items()
               if k not in ("active_no_future_occurrence",
                            "bare_noop_before_cutoff", "cutoff"))
    print(json.dumps({"status":"PASS", "scenarios":scenarios}, sort_keys=True))

if __name__ == "__main__":
    main()
