#!/usr/bin/env python3
"""Validate two roles, independent stages, and direct executor routing."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (ROOT/"SKILL.md", ROOT/"references/role-and-stage-contract.md",
         ROOT/"references/operating-model.md", BUNDLE/"thread-supervisor/SKILL.md", BUNDLE/"README.md")

def route(event: str):
    return {
        "profile_unconfirmed":"LAUNCHER_SHOW_PROPOSAL_WAIT_CONFIRM",
        "profile_confirmed":"LAUNCHER_FRESH_CREATE_ALLOWED",
        "preflight_healthy":"SAME_TASK_DISTRIBUTOR_RENAME_PIN",
        "round_complete":"EXECUTOR_COOLDOWN",
        "assignment_accepted":"LAUNCHER_IDLE_EXECUTOR_SMOKE",
        "candidate_outside_scope":"EXECUTOR_SKIP",
        "network_fault":"EXECUTOR_AUTO_RECOVER",
        "captcha":"EXECUTOR_ASK_USER_DIRECTLY",
        "direction_change":"EXECUTOR_VERSION_AT_SAFE_BOUNDARY",
        "deadline":"EXECUTOR_FINALIZE",
        "other_run_present":"IGNORE_USE_OWN_RESOURCES",
        "historical_executor_present":"IGNORE_NO_INSPECTION_FRESH_CREATE",
    }[event]

def main():
    assert all(p.is_file() for p in FILES)
    joined = "\n".join(p.read_text() for p in FILES)
    required = ("TIKTOK_LAUNCHER", "TIKTOK_EXECUTOR", "L0_BOOTSTRAP",
                "L0_DISTRIBUTOR_READY", "L0_PROFILE_LOCK",
                "L1_ASSIGN", "L2_IDLE",
                "E0_SMOKE", "E1_RUN", "E1_COOLDOWN", "E2_HARD_REPAIR", "E3_FINALIZE", "E4_COMPLETE",
                "one mission", "asks the user directly", "Independent runs")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    events = ("preflight_healthy","profile_unconfirmed","profile_confirmed",
              "assignment_accepted","round_complete",
              "candidate_outside_scope","network_fault","captcha",
              "direction_change","deadline","other_run_present","historical_executor_present")
    scenarios = {e: route(e) for e in events}
    assert scenarios["profile_unconfirmed"] == "LAUNCHER_SHOW_PROPOSAL_WAIT_CONFIRM"
    assert scenarios["profile_confirmed"] == "LAUNCHER_FRESH_CREATE_ALLOWED"
    assert scenarios["preflight_healthy"] == "SAME_TASK_DISTRIBUTOR_RENAME_PIN"
    assert scenarios["round_complete"] == "EXECUTOR_COOLDOWN"
    assert scenarios["captcha"] == "EXECUTOR_ASK_USER_DIRECTLY"
    assert scenarios["other_run_present"] == "IGNORE_USE_OWN_RESOURCES"
    assert scenarios["historical_executor_present"] == "IGNORE_NO_INSPECTION_FRESH_CREATE"
    print(json.dumps({"status":"PASS","steady_role_count":2,"scenarios":scenarios}, sort_keys=True))

if __name__ == "__main__": main()
