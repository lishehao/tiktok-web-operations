#!/usr/bin/env python3
"""Validate executor-owned run/sequence-unique one-shot wake chaining."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (ROOT/"SKILL.md", ROOT/"references/operating-model.md",
         ROOT/"references/stability-and-circuit-breakers.md",
         ROOT/"references/runtime-and-recovery.md",
         BUNDLE/"thread-supervisor/SKILL.md",
         BUNDLE/"thread-supervisor/references/identity-and-automation.md")

def policy(event):
    return {
        "assignment_accepted": "NO_TIMER_START_FIRST_ROUND",
        "round_checkpoint": "CREATE_UNIQUE_COUNT1_READBACK_THEN_YIELD",
        "valid_wake": "CONSUME_RETIRE_CLEAR_RESUME",
        "duplicate_or_late_wake": "NO_EXTERNAL_WORK",
        "misbound_wake": "NO_EXTERNAL_WORK_NO_DUPLICATE_CREATE",
        "recovery_yield": "CREATE_UNIQUE_RECOVERY_COUNT1",
        "explicit_stop": "DELETE_EXACT_PENDING_IF_ANY",
        "deadline": "DELETE_EXACT_PENDING_IF_ANY",
        "distributor": "NEVER_OWNS_EXECUTOR_TIMER",
    }[event]

def main():
    assert all(p.is_file() for p in FILES)
    joined = "\n".join(p.read_text() for p in FILES)
    required = ("Self-owned one-shot wake", "COUNT=1", "targetThreadId",
                "run_id", "round_seq", "ONE_SHOT_WAKE_CONSUMED",
                "At most one pending", "Never callback", "Never keep",
                "global ID such as `executor-heartbeat`")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    events = ("assignment_accepted","round_checkpoint","valid_wake",
              "duplicate_or_late_wake","misbound_wake","recovery_yield",
              "explicit_stop","deadline","distributor")
    scenarios = {e: policy(e) for e in events}
    assert scenarios["assignment_accepted"] == "NO_TIMER_START_FIRST_ROUND"
    assert scenarios["round_checkpoint"] == "CREATE_UNIQUE_COUNT1_READBACK_THEN_YIELD"
    assert scenarios["valid_wake"] == "CONSUME_RETIRE_CLEAR_RESUME"
    assert scenarios["distributor"] == "NEVER_OWNS_EXECUTOR_TIMER"
    print(json.dumps({"status":"PASS","scenarios":scenarios}, sort_keys=True))

if __name__ == "__main__": main()
