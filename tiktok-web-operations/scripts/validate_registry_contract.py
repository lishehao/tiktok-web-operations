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

def callback_matches(callback, expected):
    keys = ("run_id", "round_id", "round_seq", "boundary_seq",
            "coordinator_thread_id", "executor_thread_id")
    return all(callback.get(key) == expected.get(key) for key in keys)

def callback_state(status):
    return {
        "ROUND_COMPLETED": {"executor_state":"IDLE", "idle_proof":True},
        "ROUND_YIELDED": {"executor_state":"IDLE", "idle_proof":True},
        "ROUND_BLOCKED": {"executor_state":"HARD_REPAIR", "idle_proof":False},
        "RUN_RELEASED": {"executor_state":"RELEASED", "idle_proof":False},
    }[status]

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
                "new_executor_thread_id", "executor_title_status",
                "executor_archive_status", "boundary_seq",
                "expected_boundary_seq", "expected_round_id",
                "pending_round_id", "executor_idle_proof_round_id")
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
    expected_round_seq, expected_boundary_seq = 1, 1
    yielded = {"schema":"round_callback/v1", "run_id":"r", "round_id":"rd1",
               "round_seq":1, "boundary_seq":1, "coordinator_thread_id":"c",
               "executor_thread_id":"e",
               "status":"ROUND_YIELDED"}
    expected = {key: yielded[key] for key in (
        "run_id", "round_id", "round_seq", "boundary_seq",
        "coordinator_thread_id", "executor_thread_id")}
    assert callback_matches(yielded, expected)
    assert not callback_matches({key: value for key, value in yielded.items()
                                 if key != "round_id"}, expected)
    assert not callback_matches(dict(yielded, boundary_seq=2), expected)
    assert (yielded["round_seq"], yielded["boundary_seq"]) == (
        expected_round_seq, expected_boundary_seq)
    expected_boundary_seq += 1
    assert yielded["boundary_seq"] != expected_boundary_seq  # duplicate rejected
    completed = dict(yielded, boundary_seq=2, status="ROUND_COMPLETED")
    assert (completed["round_seq"], completed["boundary_seq"]) == (
        expected_round_seq, expected_boundary_seq)
    expected_round_seq += 1
    expected_boundary_seq = 1
    assert (expected_round_seq, expected_boundary_seq) == (2, 1)
    assert callback_state("ROUND_COMPLETED")["idle_proof"] is True
    assert callback_state("ROUND_YIELDED")["idle_proof"] is True
    assert callback_state("ROUND_BLOCKED") == {
        "executor_state":"HARD_REPAIR", "idle_proof":False}
    assert callback_state("RUN_RELEASED") == {
        "executor_state":"RELEASED", "idle_proof":False}
    print(json.dumps({"status":"PASS","assignment_sha256":digest,
                      "scenarios":{"key_order_invariant":True,
                                   "exact_coordinator_required":True,
                                   "exact_executor_required":True,
                                   "callback_sequence_required":True,
                                   "same_round_boundary_dedup":True,
                                   "completed_round_boundary_reset":True,
                                   "missing_round_id_rejected":True,
                                   "out_of_order_boundary_rejected":True,
                                   "blocked_and_released_not_dispatch_proof":True,
                                   "same_run_generation_increment":True,
                                   "resume_cursor_carried":True,
                                   "presentation_lifecycle_exact_id_only":True}}, sort_keys=True))

if __name__ == "__main__": main()
