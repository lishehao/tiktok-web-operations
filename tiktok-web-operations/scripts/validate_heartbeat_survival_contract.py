#!/usr/bin/env python3
"""Validate executor-owned recurring Heartbeat survival."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (ROOT/"SKILL.md", ROOT/"references/operating-model.md",
         ROOT/"references/stability-and-circuit-breakers.md",
         ROOT/"references/runtime-and-recovery.md", BUNDLE/"thread-supervisor/SKILL.md",
         BUNDLE/"thread-supervisor/references/identity-and-automation.md")

def policy(event):
    if event in {"network_timeout","err_blocked_by_client","chrome_disconnect","empty_candidates","lane_failure"}:
        return {"timer":"KEEP_REPEAT_ON","scope":"LOCAL","retry":"AUTO_RECHECK"}
    if event == "uncertain_mutation":
        return {"timer":"KEEP_REPEAT_ON","scope":"EXACT_MUTATION","retry":"NEVER_RETRY"}
    if event == "misbound_timer":
        return {"timer":"REPLACE_NO_GAP","scope":"TIMER","retry":"CREATE_VERIFY_SWITCH_RETIRE"}
    if event in {"user_stop","deadline","objective_complete"}:
        return {"timer":"RETIRE_AFTER_RELEASE","scope":"RUN","retry":"NONE"}
    raise ValueError(event)

def main():
    assert all(p.is_file() for p in FILES)
    joined = "\n".join(p.read_text() for p in FILES)
    required = ("self-owned Heartbeat", "targetThreadId=executor_thread_id", "repeat=on",
                "operation_stop_at", "ordinary failure -> delete Heartbeat",
                "create/read back the correct replacement first", "switch the executor's stored automation binding")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    events = ("network_timeout","err_blocked_by_client","chrome_disconnect","empty_candidates",
              "lane_failure","uncertain_mutation","misbound_timer","user_stop","deadline","objective_complete")
    scenarios = {e: policy(e) for e in events}
    assert all(scenarios[e]["timer"] == "KEEP_REPEAT_ON" for e in events[:6])
    assert scenarios["misbound_timer"]["timer"] == "REPLACE_NO_GAP"
    print(json.dumps({"status":"PASS","scenarios":scenarios}, sort_keys=True))

if __name__ == "__main__": main()
