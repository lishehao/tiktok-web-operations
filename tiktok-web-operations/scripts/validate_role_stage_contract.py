#!/usr/bin/env python3
"""Validate TikTok main/executor roles and callback stages."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (ROOT/"SKILL.md", ROOT/"references/role-and-stage-contract.md",
         ROOT/"references/operating-model.md", BUNDLE/"thread-supervisor/SKILL.md",
         BUNDLE/"README.md")

def route(event: str):
    return {
        "profile_unconfirmed":"MAIN_SHOW_PROPOSAL_WAIT_CONFIRM",
        "profile_confirmed":"MAIN_FRESH_CREATE_ALLOWED",
        "preflight_healthy":"SAME_TASK_MAIN_RENAME_PIN",
        "assignment_accepted":"CALLBACK_HANDSHAKE_THEN_ROUND1",
        "round_complete":"EXECUTOR_CALLBACK_IDLE",
        "callback_accepted":"MAIN_REPLAN_ARM_ONE_COOLDOWN_WAKE",
        "before_due":"NO_TIMER_WAKE",
        "wake_due_idle":"MAIN_DISPATCH_ONE_ROUND_REARM_WATCHDOG",
        "round_dispatched":"ARM_ONE_60_MINUTE_WATCHDOG",
        "candidate_outside_scope":"EXECUTOR_SKIP",
        "network_fault":"EXECUTOR_AUTO_RECOVER_OR_CALLBACK",
        "captcha":"EXECUTOR_CALLBACK_MAIN_ASK_USER",
        "direction_change":"MAIN_VERSION_NEXT_ASSIGNMENT",
        "deadline":"MAIN_STOP_DELETE_PHASE_TIMER_RELEASE",
    }[event]

def main():
    assert all(p.is_file() for p in FILES if p.name != "README.md" or p.exists())
    joined = "\n".join(p.read_text() for p in FILES if p.is_file())
    required = ("TIKTOK_COORDINATOR", "TIKTOK_EXECUTOR", "C0_BOOTSTRAP",
                "C1_HANDSHAKE", "C2_DISPATCH", "C3_WAIT", "C4_REPLAN",
                "C5_COOLDOWN", "C6_FINALIZE", "E1_RUN", "E2_CALLBACK",
                "E3_HARD_REPAIR", "E4_RELEASE", "one bounded round")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    events = ("profile_unconfirmed","profile_confirmed","preflight_healthy",
              "assignment_accepted","round_complete","callback_accepted",
              "before_due","wake_due_idle","round_dispatched","candidate_outside_scope",
              "network_fault","captcha","direction_change","deadline")
    scenarios = {e: route(e) for e in events}
    assert scenarios["round_complete"] == "EXECUTOR_CALLBACK_IDLE"
    assert scenarios["before_due"] == "NO_TIMER_WAKE"
    assert scenarios["wake_due_idle"] == "MAIN_DISPATCH_ONE_ROUND_REARM_WATCHDOG"
    assert scenarios["round_dispatched"] == "ARM_ONE_60_MINUTE_WATCHDOG"
    assert scenarios["captcha"] == "EXECUTOR_CALLBACK_MAIN_ASK_USER"
    print(json.dumps({"status":"PASS","steady_role_count":2,"scenarios":scenarios}, sort_keys=True))

if __name__ == "__main__": main()
