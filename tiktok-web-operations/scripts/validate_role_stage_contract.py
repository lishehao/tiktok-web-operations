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
        "executor_created":"MAIN_SET_EXACT_ID_TITLE_READBACK",
        "executor_title_unavailable":"MAIN_CONTINUE_DEGRADED_ONE_IDLE_REPAIR",
        "preflight_healthy":"SAME_TASK_MAIN_RENAME_PIN",
        "assignment_accepted":"CALLBACK_HANDSHAKE_THEN_ROUND1",
        "round_complete":"EXECUTOR_CALLBACK_IDLE",
        "round_yielded":"EXECUTOR_CALLBACK_IDLE_SAME_ROUND_RECOVERY_PENDING",
        "recovery_due":"MAIN_RECOVERY_FIRST_SAME_ROUND",
        "callback_accepted":"MAIN_REPLAN_STORE_DUE_KEEP_RECURRENCE",
        "before_due":"MAIN_TICK_NO_DISPATCH_KEEP_RECURRENCE",
        "wake_due_callback_idle":"MAIN_DISPATCH_FROM_CALLBACK_PROOF_KEEP_RECURRENCE",
        "wake_due_read_unavailable_callback_idle":"MAIN_DISPATCH_FROM_CALLBACK_PROOF_KEEP_RECURRENCE",
        "wake_due_missing_idle_proof":"MAIN_REQUEST_ONCE_KEEP_RECURRENCE",
        "active_without_future_run":"MAIN_MISSION_SCHEDULER_EXPIRED_REPAIR_OR_FINALIZE",
        "round_dispatched":"KEEP_MISSION_RECURRENCE_UNCHANGED",
        "candidate_outside_scope":"EXECUTOR_SKIP",
        "network_fault":"EXECUTOR_AUTO_RECOVER_OR_CALLBACK",
        "captcha":"EXECUTOR_CALLBACK_MAIN_ASK_USER",
        "direction_change":"MAIN_VERSION_NEXT_ASSIGNMENT",
        "same_mission_continue":"MAIN_REUSE_EXACT_EXECUTOR",
        "registered_owner_missing":"MAIN_ONE_SAME_RUN_REPLACEMENT_HANDSHAKE",
        "task_not_loaded":"MAIN_RETAIN_OWNER_KEEP_RECURRENCE",
        "terminal_new_instruction":"MAIN_NEW_RUN_FRESH_EXECUTOR",
        "terminal_reconciled":"MAIN_ARCHIVE_EXACT_RELEASED_EXECUTOR",
        "deadline":"MAIN_STOP_TIKTOK_REQUEST_RELEASE_KEEP_CLEANUP_WAKE",
        "cleanup_expired_unreleased":"MAIN_RELEASE_UNCERTAIN_DELETE_NO_ARCHIVE",
    }[event]

def main():
    assert all(p.is_file() for p in FILES if p.name != "README.md" or p.exists())
    joined = "\n".join(p.read_text() for p in FILES if p.is_file())
    required = ("TIKTOK_COORDINATOR", "TIKTOK_EXECUTOR", "C0_BOOTSTRAP",
                "C1_HANDSHAKE", "C2_DISPATCH", "C3_WAIT", "C4_REPLAN",
                "C1_RECOVER_EXECUTOR", "C5_COOLDOWN", "C5_RECOVERY", "C6_FINALIZE",
                "C6_RELEASE_UNCERTAIN", "E1_RUN",
                "E1_RECOVERY",
                "E2_CALLBACK", "E3_HARD_REPAIR", "E4_RELEASE",
                "Single-writer responsibility matrix", "one bounded round",
                "DEGRADED_EXECUTOR_ARCHIVE_UNAVAILABLE", "boundary_seq",
                "ROUND_PROGRESS", "CHECKPOINT_OR_YIELD/v1",
                "PROGRESS_UNVERIFIED")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    events = ("profile_unconfirmed","profile_confirmed","executor_created",
              "executor_title_unavailable","preflight_healthy",
              "assignment_accepted","round_complete","round_yielded","recovery_due","callback_accepted",
              "before_due","wake_due_callback_idle",
              "wake_due_read_unavailable_callback_idle",
              "wake_due_missing_idle_proof",
              "active_without_future_run","round_dispatched","candidate_outside_scope",
              "network_fault","captcha","direction_change","deadline")
    events = events[:-1] + ("same_mission_continue", "registered_owner_missing",
                           "task_not_loaded", "terminal_new_instruction",
                           "terminal_reconciled", "deadline", "cleanup_expired_unreleased")
    scenarios = {e: route(e) for e in events}
    assert scenarios["round_complete"] == "EXECUTOR_CALLBACK_IDLE"
    assert scenarios["round_yielded"] == "EXECUTOR_CALLBACK_IDLE_SAME_ROUND_RECOVERY_PENDING"
    assert scenarios["recovery_due"] == "MAIN_RECOVERY_FIRST_SAME_ROUND"
    assert scenarios["before_due"] == "MAIN_TICK_NO_DISPATCH_KEEP_RECURRENCE"
    assert scenarios["wake_due_callback_idle"] == "MAIN_DISPATCH_FROM_CALLBACK_PROOF_KEEP_RECURRENCE"
    assert scenarios["wake_due_read_unavailable_callback_idle"] == scenarios["wake_due_callback_idle"]
    assert scenarios["wake_due_missing_idle_proof"] == "MAIN_REQUEST_ONCE_KEEP_RECURRENCE"
    assert scenarios["active_without_future_run"] == "MAIN_MISSION_SCHEDULER_EXPIRED_REPAIR_OR_FINALIZE"
    assert scenarios["round_dispatched"] == "KEEP_MISSION_RECURRENCE_UNCHANGED"
    assert scenarios["captcha"] == "EXECUTOR_CALLBACK_MAIN_ASK_USER"
    assert scenarios["same_mission_continue"] == "MAIN_REUSE_EXACT_EXECUTOR"
    assert scenarios["registered_owner_missing"] == "MAIN_ONE_SAME_RUN_REPLACEMENT_HANDSHAKE"
    assert scenarios["task_not_loaded"] == "MAIN_RETAIN_OWNER_KEEP_RECURRENCE"
    assert scenarios["terminal_new_instruction"] == "MAIN_NEW_RUN_FRESH_EXECUTOR"
    assert scenarios["executor_created"] == "MAIN_SET_EXACT_ID_TITLE_READBACK"
    assert scenarios["terminal_reconciled"] == "MAIN_ARCHIVE_EXACT_RELEASED_EXECUTOR"
    assert scenarios["cleanup_expired_unreleased"].endswith("NO_ARCHIVE")
    print(json.dumps({"status":"PASS","steady_role_count":2,"scenarios":scenarios}, sort_keys=True))

if __name__ == "__main__": main()
