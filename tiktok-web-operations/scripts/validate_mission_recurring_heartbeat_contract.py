#!/usr/bin/env python3
"""Validate TikTok mission-scoped recurring Heartbeat scheduling."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
WAKE_TOLERANCE = timedelta(minutes=5)
FILES = (
    ROOT / "SKILL.md",
    ROOT / "references/operating-model.md",
    ROOT / "references/role-and-stage-contract.md",
    ROOT / "references/stability-and-circuit-breakers.md",
    ROOT / "references/runtime-and-recovery.md",
    BUNDLE / "thread-supervisor/SKILL.md",
    BUNDLE / "thread-supervisor/references/identity-and-automation.md",
    BUNDLE / "thread-supervisor/references/canonical-registry.md",
    BUNDLE / "thread-supervisor/references/tiktok-coordinator-worker.md",
    BUNDLE / "README.md",
)


def transition(event: str) -> dict[str, object]:
    return {
        "create": {
            "mode": "MISSION_RECURRING_15M",
            "repeat": True,
            "interval_minutes": 15,
            "count_one": False,
            "cleanup_after_cutoff": True,
        },
        "dispatch": {"action": "DISPATCH_ONE", "schedule": "UNCHANGED"},
        "callback": {
            "action": "STORE_IDLE_AND_NEXT_DISPATCH_AT",
            "round_seq": "INCREMENT",
            "boundary_seq": "RESET_TO_1",
            "schedule": "UNCHANGED",
        },
        "round_yielded": {
            "action": "STORE_RECOVERY_PENDING_SAME_ROUND",
            "round_seq": "UNCHANGED",
            "boundary_seq": "INCREMENT",
            "next_dispatch": "RECOVERY_FIRST",
            "schedule": "UNCHANGED",
        },
        "due_callback_idle": {
            "action": "DISPATCH_ONE",
            "requires_live_thread_read": False,
            "schedule": "UNCHANGED",
        },
        "callback_delivery_lost": {
            "action": "NEXT_RECURRING_TICK_RECOVERS",
            "schedule": "UNCHANGED",
        },
        "active_executor_tick": {
            "action": "NO_DISPATCH",
            "schedule": "UNCHANGED",
            "notify": False,
        },
        "early_cooldown_tick": {
            "action": "NO_DISPATCH",
            "schedule": "UNCHANGED",
            "notify": False,
        },
        "missing_callback": {
            "action": "REQUEST_ONCE_THEN_WAIT",
            "schedule": "UNCHANGED",
        },
        "transient_read_failure": {
            "action": "KEEP_OWNER_AND_RECURRENCE",
            "schedule": "UNCHANGED",
        },
        "active_no_future_occurrence": {
            "action": "MISSION_SCHEDULER_EXPIRED_REPAIR_IN_PLACE",
            "dispatch_allowed_before_repair": False,
        },
        "cutoff": {
            "action": "STOP_TIKTOK_REQUEST_RELEASE_KEEP_CLEANUP_WAKE",
            "schedule": "UNCHANGED_UNTIL_RELEASE_OR_CLEANUP_UNTIL",
        },
        "cleanup_released": {"action": "DELETE_READBACK_RECONCILE_ARCHIVE"},
        "cleanup_expired_unreleased": {
            "action": "RELEASE_UNCERTAIN_DELETE_READBACK_NO_ARCHIVE"
        },
    }[event]


def scheduler_rrule(cutoff: datetime) -> tuple[str, datetime]:
    assert cutoff.tzinfo is not None
    cleanup_until = cutoff.astimezone(timezone.utc) + timedelta(minutes=15)
    return (
        "RRULE:FREQ=MINUTELY;INTERVAL=15;UNTIL="
        + cleanup_until.strftime("%Y%m%dT%H%M%SZ"),
        cleanup_until,
    )


def classify_wake(
    scheduled: datetime, actual: datetime, cutoff: datetime
) -> dict[str, object]:
    assert scheduled.tzinfo is not None
    assert actual.tzinfo is not None
    assert cutoff.tzinfo is not None
    delta_seconds = int((actual - scheduled).total_seconds())
    if actual >= cutoff:
        return {
            "timing": "ON_TIME_WITH_TOLERANCE"
            if abs(delta_seconds) <= WAKE_TOLERANCE.total_seconds()
            else "WAKE_TIME_DRIFT",
            "delta_seconds": delta_seconds,
            "action": "CUTOFF_NO_NEW_WORK",
            "repair": False,
        }
    if abs(delta_seconds) <= WAKE_TOLERANCE.total_seconds():
        return {
            "timing": "ON_TIME_WITH_TOLERANCE",
            "delta_seconds": delta_seconds,
            "action": "CONTINUE_NORMAL_GATE",
            "repair": False,
        }
    return {
        "timing": "WAKE_TIME_DRIFT",
        "delta_seconds": delta_seconds,
        "action": "BOUNDED_DIAGNOSIS_KEEP_RECURRENCE",
        "repair": "ONLY_IF_CONFIGURATION_OR_FUTURE_RUN_PROOF_FAILS",
    }


def main() -> None:
    missing_files = [
        str(path) for path in FILES
        if not path.is_file() and path.name != "README.md"
    ]
    assert not missing_files, missing_files
    joined = "\n".join(path.read_text() for path in FILES if path.is_file())
    required = (
        "coordinator_worker",
        "CALLBACK_PING/v1",
        "CALLBACK_ACK/v1",
        "round_assignment/v1",
        "round_callback/v1",
        "TikTok 主控台",
        "mission recurring",
        "repeat-on",
        "15-minute",
        "RRULE:FREQ=MINUTELY;INTERVAL=15;UNTIL=",
        "COUNT=1",
        "cleanup `UNTIL`",
        "operation_stop_at",
        "next_dispatch_at",
        "fresh machine",
        "executor owns zero timers",
        "SCHEDULER_CONTINUATION_FAILURE",
        "catch-up bursts",
        "CALLBACK_ACCEPTED",
        "diagnostic",
        "notLoaded",
        "MISSION_SCHEDULER_EXPIRED",
        "DONT_NOTIFY",
        "ROUND_YIELDED",
        "RECOVERY_FIRST",
        "boundary_seq",
        "pending_boundary_seq",
        "ROUND_PROGRESS",
        "CHECKPOINT_OR_YIELD/v1",
        "PROGRESS_UNVERIFIED",
        "RELEASE_UNCERTAIN",
        "ON_TIME_WITH_TOLERANCE",
        "WAKE_TIME_DRIFT",
        "five minutes",
    )
    absent = [term for term in required if term.lower() not in joined.lower()]
    assert not absent, absent

    stale_positive_rules = (
        "arm one 60-minute `ACTIVE_WATCHDOG`",
        "update the same timer to one `COOLDOWN_WAKE`",
        "future_wake_count=1",
        "callback-first phase timer",
        "phase/one-occurrence state",
    )
    present = [term for term in stale_positive_rules if term.lower() in joined.lower()]
    assert not present, present

    events = (
        "create",
        "dispatch",
        "callback",
        "round_yielded",
        "due_callback_idle",
        "callback_delivery_lost",
        "active_executor_tick",
        "early_cooldown_tick",
        "missing_callback",
        "transient_read_failure",
        "active_no_future_occurrence",
        "cutoff",
        "cleanup_released",
        "cleanup_expired_unreleased",
    )
    scenarios = {event: transition(event) for event in events}
    cutoff = datetime(2026, 7, 15, 13, 29, 11, tzinfo=timezone.utc)
    rrule, cleanup_until = scheduler_rrule(cutoff)
    scheduled = datetime(2026, 7, 15, 12, 0, 0, tzinfo=timezone.utc)
    wake_scenarios = {
        "early_exactly_5m": classify_wake(
            scheduled, scheduled - timedelta(minutes=5), cutoff
        ),
        "late_exactly_5m": classify_wake(
            scheduled, scheduled + timedelta(minutes=5), cutoff
        ),
        "early_over_5m": classify_wake(
            scheduled, scheduled - timedelta(minutes=5, seconds=1), cutoff
        ),
        "late_over_5m": classify_wake(
            scheduled, scheduled + timedelta(minutes=5, seconds=1), cutoff
        ),
        "within_tolerance_after_cutoff": classify_wake(
            cutoff - timedelta(minutes=1), cutoff + timedelta(minutes=1), cutoff
        ),
    }
    assert scenarios["create"]["repeat"] is True
    assert scenarios["create"]["interval_minutes"] == 15
    assert scenarios["create"]["count_one"] is False
    assert scenarios["callback"]["schedule"] == "UNCHANGED"
    assert scenarios["callback"]["round_seq"] == "INCREMENT"
    assert scenarios["callback"]["boundary_seq"] == "RESET_TO_1"
    assert scenarios["round_yielded"] == {
        "action": "STORE_RECOVERY_PENDING_SAME_ROUND",
        "round_seq": "UNCHANGED",
        "boundary_seq": "INCREMENT",
        "next_dispatch": "RECOVERY_FIRST",
        "schedule": "UNCHANGED",
    }
    assert scenarios["callback_delivery_lost"]["action"] == "NEXT_RECURRING_TICK_RECOVERS"
    assert scenarios["due_callback_idle"]["requires_live_thread_read"] is False
    assert scenarios["active_executor_tick"]["action"] == "NO_DISPATCH"
    assert scenarios["active_executor_tick"]["notify"] is False
    assert scenarios["missing_callback"]["action"] == "REQUEST_ONCE_THEN_WAIT"
    assert scenarios["active_no_future_occurrence"]["dispatch_allowed_before_repair"] is False
    assert scenarios["cutoff"]["action"] == "STOP_TIKTOK_REQUEST_RELEASE_KEEP_CLEANUP_WAKE"
    assert scenarios["cleanup_released"]["action"] == "DELETE_READBACK_RECONCILE_ARCHIVE"
    assert scenarios["cleanup_expired_unreleased"]["action"].endswith("NO_ARCHIVE")
    assert rrule == "RRULE:FREQ=MINUTELY;INTERVAL=15;UNTIL=20260715T134411Z"
    assert "COUNT=" not in rrule
    assert cleanup_until - cutoff == timedelta(minutes=15)
    assert wake_scenarios["early_exactly_5m"]["timing"] == "ON_TIME_WITH_TOLERANCE"
    assert wake_scenarios["late_exactly_5m"]["timing"] == "ON_TIME_WITH_TOLERANCE"
    assert wake_scenarios["early_exactly_5m"]["action"] == "CONTINUE_NORMAL_GATE"
    assert wake_scenarios["late_exactly_5m"]["repair"] is False
    assert wake_scenarios["early_over_5m"]["timing"] == "WAKE_TIME_DRIFT"
    assert wake_scenarios["late_over_5m"]["timing"] == "WAKE_TIME_DRIFT"
    assert wake_scenarios["late_over_5m"]["action"] == "BOUNDED_DIAGNOSIS_KEEP_RECURRENCE"
    assert wake_scenarios["within_tolerance_after_cutoff"]["action"] == "CUTOFF_NO_NEW_WORK"
    print(json.dumps({
        "status": "PASS",
        "rrule": rrule,
        "scenarios": scenarios,
        "wake_scenarios": wake_scenarios,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
