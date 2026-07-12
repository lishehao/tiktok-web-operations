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
    mission_running: bool = False,
    human_needed: bool = False,
) -> str:
    if event == "coordinator_heartbeat":
        if actor != "coordinator":
            return "NO_ACTION"
        return "NO_ACTION" if mission_running else "READ_ONLY_CHECK_AND_RESUME_IF_BROKEN"
    if event == "candidate_outside_scope":
        return "SKIP_WITHIN_MISSION" if actor == "executor" else "NO_ACTION"
    if event == "captcha":
        return "RELEASE_AND_RISK_EVENT" if actor == "executor" else "NO_ACTION"
    if event == "direction_change":
        return "QUEUE_SAFE_BOUNDARY_VERSION" if actor == "coordinator" and mission_running else "VERSION_COMMIT"
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
        "S4_FIRST_SEGMENT",
        "S5_CONTINUOUS_RUN",
        "S6_PAUSED",
        "S7_FINALIZE",
        "S8_IDLE_COMPLETE",
        "THREAD_READY",
        "MISSION_CHECKPOINT",
        "RISK_EVENT",
        "EXECUTOR_RELEASED",
        "one accepted mission is active at most",
        "coordinator Heartbeat is a durable supervision/recovery signal",
        "Heartbeat survival invariant",
        "role-and-stage-contract.md",
    )
    missing_terms = [term for term in required if term.lower() not in joined.lower()]
    assert not missing_terms, f"missing role/stage assertions: {missing_terms}"

    assert "never: open/control Chrome" in role_text
    assert "never: choose or change the account direction" in role_text
    assert "raw per-item ledger" in role_text
    assert "Exact comment text within the approved voice" in role_text
    assert "One executor activation may finish multiple logical training units" in " ".join(skill_text.split())

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
        "coordinator_wake_idle": route_event("coordinator_heartbeat", actor="coordinator"),
        "coordinator_wake_running": route_event(
            "coordinator_heartbeat", actor="coordinator", mission_running=True
        ),
        "coordinator_heartbeat_wakes_executor": route_event(
            "coordinator_heartbeat", actor="executor"
        ),
        "executor_candidate_outside_scope": route_event(
            "candidate_outside_scope", actor="executor"
        ),
        "executor_captcha": route_event("captcha", actor="executor"),
        "direction_change_while_running": route_event(
            "direction_change", actor="coordinator", mission_running=True
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
        "coordinator_wake_idle": "READ_ONLY_CHECK_AND_RESUME_IF_BROKEN",
        "coordinator_wake_running": "NO_ACTION",
        "coordinator_heartbeat_wakes_executor": "NO_ACTION",
        "executor_candidate_outside_scope": "SKIP_WITHIN_MISSION",
        "executor_captcha": "RELEASE_AND_RISK_EVENT",
        "direction_change_while_running": "QUEUE_SAFE_BOUNDARY_VERSION",
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
