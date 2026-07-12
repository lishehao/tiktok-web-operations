#!/usr/bin/env python3
"""Validate TikTok role ownership, stage gates, and isolated routing scenarios."""

from __future__ import annotations

import json
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
BUNDLE = SKILL_ROOT.parent
ROLE_STAGE = SKILL_ROOT / "references/role-and-stage-contract.md"
OPERATING = SKILL_ROOT / "references/operating-model.md"
STARTUP = SKILL_ROOT / "references/startup-health-check.md"
SKILL = SKILL_ROOT / "SKILL.md"
SUPERVISOR = BUNDLE / "thread-supervisor/SKILL.md"
README = BUNDLE / "README.md"


def route_event(
    event: str,
    *,
    actor: str,
    running_block: bool = False,
    human_needed: bool = False,
) -> str:
    if event == "operation_heartbeat":
        return "EXECUTE_ONE_BLOCK" if actor == "executor" and not running_block else "NO_ACTION"
    if event == "supervisor_heartbeat":
        return "READ_ONLY_SUPERVISE" if actor == "coordinator" else "NO_ACTION"
    if event == "candidate_outside_scope":
        return "SKIP_WITHIN_BLOCK" if actor == "executor" else "NO_ACTION"
    if event == "captcha":
        return "RELEASE_AND_RISK_EVENT" if actor == "executor" else "NO_ACTION"
    if event == "direction_change":
        return "QUEUE_NEXT_VERSION" if actor == "coordinator" and running_block else "VERSION_COMMIT"
    if event in {"stop", "deadline"}:
        return "START_FINALIZATION" if actor == "coordinator" else "NO_ACTION"
    if event == "risk_callback":
        if actor != "coordinator":
            return "NO_ACTION"
        return "ASK_USER" if human_needed else "AUTO_RESUME_WAIT"
    return "NO_ACTION"


def main() -> None:
    paths = (ROLE_STAGE, OPERATING, STARTUP, SKILL, SUPERVISOR)
    missing = [str(path) for path in paths if not path.is_file()]
    assert not missing, f"missing contract files: {missing}"
    documents = {path.name + str(index): path.read_text() for index, path in enumerate(paths)}
    if README.exists():
        documents["README"] = README.read_text()
    joined = "\n".join(documents.values())
    role_text = ROLE_STAGE.read_text()
    operating_text = OPERATING.read_text()
    skill_text = SKILL.read_text()

    required = (
        "BOOTSTRAP_STARTER",
        "TIKTOK_COORDINATOR",
        "TIKTOK_EXECUTOR",
        "S0_PREFLIGHT",
        "S1_MISSION",
        "S2_PAIR_BOOTSTRAP",
        "S3_RUNTIME_SMOKE",
        "S4_FIRST_BLOCK",
        "S5_SCHEDULED_RUN",
        "S6_PAUSED",
        "S7_FINALIZE",
        "S8_IDLE_COMPLETE",
        "THREAD_READY",
        "BLOCK_RESULT",
        "RISK_EVENT",
        "EXECUTOR_RELEASED",
        "one accepted block is active at most",
        "Heartbeats are wake signals, not roles or agents",
        "role-and-stage-contract.md",
    )
    missing_terms = [term for term in required if term.lower() not in joined.lower()]
    assert not missing_terms, f"missing role/stage assertions: {missing_terms}"

    assert "never: open/control Chrome" in role_text
    assert "never: choose or change the account direction" in role_text
    assert "raw per-item ledger" in role_text
    assert "Exact comment text within the approved voice" in role_text
    assert "The main console chooses the next bounded outcome" in " ".join(skill_text.split())

    stale_duplicate_sections = (
        "## Topology",
        "## Role cards",
        "## Authority split",
        "## Coordinator loop",
        "## Executor loop",
    )
    present = [heading for heading in stale_duplicate_sections if heading in operating_text]
    assert not present, f"operating-model still duplicates role authority: {present}"
    assert "## Execution Thread Loop" not in skill_text

    scenarios = {
        "correct_operation_wake": route_event("operation_heartbeat", actor="executor"),
        "operation_wakes_coordinator": route_event("operation_heartbeat", actor="coordinator"),
        "overlapping_operation_slot": route_event(
            "operation_heartbeat", actor="executor", running_block=True
        ),
        "correct_supervisor_wake": route_event("supervisor_heartbeat", actor="coordinator"),
        "supervisor_wakes_executor": route_event("supervisor_heartbeat", actor="executor"),
        "executor_candidate_outside_scope": route_event(
            "candidate_outside_scope", actor="executor"
        ),
        "executor_captcha": route_event("captcha", actor="executor"),
        "direction_change_while_running": route_event(
            "direction_change", actor="coordinator", running_block=True
        ),
        "deadline": route_event("deadline", actor="coordinator"),
        "risk_needs_human": route_event(
            "risk_callback", actor="coordinator", human_needed=True
        ),
        "risk_auto_resume": route_event(
            "risk_callback", actor="coordinator", human_needed=False
        ),
    }
    expected = {
        "correct_operation_wake": "EXECUTE_ONE_BLOCK",
        "operation_wakes_coordinator": "NO_ACTION",
        "overlapping_operation_slot": "NO_ACTION",
        "correct_supervisor_wake": "READ_ONLY_SUPERVISE",
        "supervisor_wakes_executor": "NO_ACTION",
        "executor_candidate_outside_scope": "SKIP_WITHIN_BLOCK",
        "executor_captcha": "RELEASE_AND_RISK_EVENT",
        "direction_change_while_running": "QUEUE_NEXT_VERSION",
        "deadline": "START_FINALIZATION",
        "risk_needs_human": "ASK_USER",
        "risk_auto_resume": "AUTO_RESUME_WAIT",
    }
    assert scenarios == expected, {"actual": scenarios, "expected": expected}

    print(
        json.dumps(
            {
                "status": "PASS",
                "steady_role_count": 2,
                "temporary_bootstrap_role": True,
                "stage_count": 9,
                "scenarios": scenarios,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
