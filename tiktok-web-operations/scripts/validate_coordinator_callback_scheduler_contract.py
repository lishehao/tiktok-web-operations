#!/usr/bin/env python3
"""Validate TikTok callback loop and coordinator-owned fixed scheduler."""
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

def wake(*, due: bool, active: bool, pending: bool, cutoff: bool) -> str:
    if cutoff: return "DELETE_SCHEDULER_FINALIZE"
    if active or not pending or not due: return "NOOP"
    return "DISPATCH_ONE_ROUND"

def main():
    assert all(p.is_file() for p in FILES)
    joined = "\n".join(p.read_text() for p in FILES)
    required = ("coordinator_worker", "CALLBACK_PING/v1", "CALLBACK_ACK/v1",
                "round_assignment/v1", "round_callback/v1", "TikTok 主控台",
                "fixed scheduler", "recurring", "five-minute", "repeat-on",
                "next_dispatch_at", "fresh machine", "executor owns zero timers",
                "SCHEDULER_CONTINUATION_FAILURE", "no-op", "catch-up bursts")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    forbidden = ("TikTok declares `launcher_self_owned_executor`",
                 "Never callback the distributor",
                 "EXECUTOR_SELF_OWNED_ONE_SHOT_CHAIN")
    present = [x for x in forbidden if x in joined]
    assert not present, present
    scenarios = {
        "before_due": wake(due=False, active=False, pending=True, cutoff=False),
        "executor_active": wake(due=True, active=True, pending=True, cutoff=False),
        "no_pending": wake(due=True, active=False, pending=False, cutoff=False),
        "due_idle": wake(due=True, active=False, pending=True, cutoff=False),
        "cutoff": wake(due=True, active=False, pending=True, cutoff=True),
    }
    assert scenarios["before_due"] == "NOOP"
    assert scenarios["executor_active"] == "NOOP"
    assert scenarios["no_pending"] == "NOOP"
    assert scenarios["due_idle"] == "DISPATCH_ONE_ROUND"
    assert scenarios["cutoff"] == "DELETE_SCHEDULER_FINALIZE"
    print(json.dumps({"status":"PASS","scenarios":scenarios}, sort_keys=True))

if __name__ == "__main__": main()
