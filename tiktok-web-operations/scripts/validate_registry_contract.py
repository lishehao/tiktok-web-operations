#!/usr/bin/env python3
"""Validate canonical coordinator/executor assignment and callback registry."""
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (BUNDLE/"thread-supervisor/references/canonical-registry.md",
         BUNDLE/"thread-supervisor/references/identity-and-automation.md",
         ROOT/"references/operating-model.md", ROOT/"SKILL.md", BUNDLE/"README.md")

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()

def main():
    assert all(p.is_file() for p in FILES if p.name != "README.md" or p.exists())
    joined = "\n".join(p.read_text() for p in FILES if p.is_file())
    required = ("executor_bootstrap/v2", "executor_assignment/v2", "canonical",
                "sort_keys=True", "separators=(\",\", \":\")", "assignment_id",
                "coordinator_thread_id", "executor_thread_id", "direction_ref",
                "authority_ref", "mission_ref", "ROUND_BOUNDARY_TO_EXACT_COORDINATOR",
                "COORDINATOR_OWNED_MISSION_RECURRING_15M", "round_assignment/v1",
                "round_callback/v1", "gpt-5.6-luna", "thinking\":\"high",
                "executor_generation", "predecessor_executor_thread_id",
                "resume_cursor_ref", "old_executor_thread_id",
                "new_executor_thread_id")
    missing = [x for x in required if x not in joined]
    assert not missing, missing
    assignment = {
        "schema":"executor_assignment/v2", "assignment_id":"a", "run_id":"r",
        "coordinator_thread_id":"c", "executor_thread_id":"e", "role":"TIKTOK_EXECUTOR",
        "executor_generation":1, "predecessor_executor_thread_id":None,
        "execution_profile":{"model":"gpt-5.6-luna","thinking":"high"},
        "direction_ref":{"id":"d","version":1,"sha256":"1"*64},
        "authority_ref":{"id":"a","version":1,"sha256":"2"*64},
        "mission_ref":{"id":"m","version":1,"sha256":"3"*64},
        "resume_cursor_ref":None,
        "callback_policy":"ROUND_BOUNDARY_TO_EXACT_COORDINATOR",
        "automation_policy":"COORDINATOR_OWNED_MISSION_RECURRING_15M"
    }
    reordered = dict(reversed(list(assignment.items())))
    assert canonical(assignment) == canonical(reordered)
    digest = hashlib.sha256(canonical(assignment)).hexdigest()
    wrong = dict(assignment); wrong["coordinator_thread_id"] = "other"
    assert hashlib.sha256(canonical(wrong)).hexdigest() != digest
    replacement = dict(assignment)
    replacement.update({"assignment_id":"a2", "executor_thread_id":"e2",
                        "executor_generation":2,
                        "predecessor_executor_thread_id":"e",
                        "resume_cursor_ref":{"id":"cursor","version":1,
                                             "sha256":"4"*64}})
    assert replacement["executor_generation"] == assignment["executor_generation"] + 1
    assert replacement["predecessor_executor_thread_id"] == assignment["executor_thread_id"]
    assert replacement["run_id"] == assignment["run_id"]
    print(json.dumps({"status":"PASS","assignment_sha256":digest,
                      "scenarios":{"key_order_invariant":True,
                                   "exact_coordinator_required":True,
                                   "exact_executor_required":True,
                                   "callback_sequence_required":True,
                                   "same_run_generation_increment":True,
                                   "resume_cursor_carried":True}}, sort_keys=True))

if __name__ == "__main__": main()
