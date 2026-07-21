#!/usr/bin/env python3
"""Validate persistent same-Chrome recovery and optional runtime ledger data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
DOCS = (
    BUNDLE / "README.md",
    ROOT / "SKILL.md",
    ROOT / "references/runtime-and-recovery.md",
    ROOT / "references/blocker-minimization.md",
    ROOT / "references/engagement-and-analytics.md",
    ROOT / "references/stability-and-circuit-breakers.md",
    ROOT / "references/platform-boundaries.md",
    ROOT / "references/operating-model.md",
    ROOT / "references/role-and-stage-contract.md",
    BUNDLE / "thread-supervisor/references/tiktok-coordinator-worker.md",
    BUNDLE / "thread-supervisor/references/identity-and-automation.md",
    BUNDLE / "thread-supervisor/references/canonical-registry.md",
)


def recover(event: str) -> dict[str, Any]:
    return {
        "empty_tab_list": {
            "action": "CREATE_FRESH_OWNED_TAB_KEEP_BROWSER_BINDING",
            "same_turn_pass": True,
            "scheduler": "UNCHANGED",
        },
        "stale_tab": {
            "action": "DISCARD_TAB_BINDING_CREATE_OWNED_TAB",
            "same_turn_pass": True,
            "scheduler": "UNCHANGED",
        },
        "browser_disconnected": {
            "action": "RECONNECT_SAME_CHROME_THEN_OWNED_TAB",
            "binding_invalidated": "BROWSER",
            "same_turn_pass": True,
            "scheduler": "UNCHANGED",
        },
        "metadata_healthy_neutral_goto_timeout": {
            "error_class": "CHROME_CONTENT_CHANNEL_TIMEOUT",
            "control_plane": "HEALTHY",
            "tab_metadata": "HEALTHY",
            "scope": "GLOBAL_CONTENT_CHANNEL",
            "not_classes": (
                "CHROME_DISCONNECTED",
                "TARGET_TAB_NOT_FOUND",
                "ACCOUNT_RISK",
                "TIKTOK_ROUTE_FAULT",
            ),
            "scheduler": "UNCHANGED",
        },
        "navigation_timeout_loaded": {
            "action": "READ_BACK_URL_TITLE_PAGE_STATE_CONTINUE_NO_REPEAT_GOTO",
            "repeat_navigation": False,
            "scheduler": "UNCHANGED",
        },
        "visible_textarea_hidden_input": {
            "action": "USE_VISIBLE_TEXTAREA_IGNORE_HIDDEN_INPUT",
            "selector": 'textarea[name=q][placeholder="Find anything"]',
            "hidden_selector_rejected": "input[name=q]",
        },
        "react_fill_empty_state_not_cleared": {
            "action": "META_A_BACKSPACE_READBACK_VALUE_AND_ENABLED_STATE",
            "fill_empty_sufficient": False,
        },
        "one_boundary_action_per_call": {
            "action": "ONE_POTENTIALLY_BLOCKING_BROWSER_ACTION",
            "forbidden_combo": "GOTO_PLUS_DOM_OR_SCREENSHOT_OR_EVALUATE",
            "outer_budget": "CONFIGURABLE_OR_MEASURED_NOT_PLATFORM_TRUTH",
            "observed_outer_budget_seconds": 120,
            "ambient_network_disable": "OPTIONAL_IF_SUPPORTED_AND_READ_BACK",
        },
        "read_only_tool_timeout": {
            "action": "ONE_RECOVERY_PASS_THEN_ROUND_YIELDED",
            "mutation_freeze": False,
            "scheduler": "UNCHANGED",
        },
        "mutation_tool_timeout": {
            "action": "SUBMISSION_UNCERTAIN_FREEZE_ACTION_KEY",
            "mutation_retry": False,
            "reopen_for_verification": False,
            "scheduler": "UNCHANGED",
        },
        "dns_or_network_persistent": {
            "action": "ROUND_YIELDED_RECOVERY_PENDING_SAME_ROUND",
            "next_assignment": "RECOVERY_FIRST",
            "scheduler": "UNCHANGED",
        },
        "http_403_target_only": {
            "action": "SKIP_OR_ROTATE_TARGET_ROUTE",
            "human_question": False,
            "scheduler": "UNCHANGED",
        },
        "http_429": {
            "action": "HONOR_RETRY_AFTER_NO_BUSY_WAIT",
            "next_assignment": "RECOVERY_FIRST",
            "scheduler": "UNCHANGED",
        },
        "http_429_no_retry_after": {
            "action": "WAIT_UNTIL_NEXT_15M_HEARTBEAT_ONE_SCOPED_PROBE",
            "next_assignment": "RECOVERY_FIRST",
            "scheduler": "UNCHANGED",
        },
        "http_5xx": {
            "action": "LOCAL_RETRY_THEN_LATER_WAKE",
            "scheduler": "UNCHANGED",
        },
        "blocked_by_client": {
            "action": "FRESH_OWNED_TAB_SCOPE_PROBE_THEN_LATER_WAKE",
            "scheduler": "UNCHANGED",
        },
        "blank_or_delayed_hydration": {
            "action": "ONE_HYDRATION_WAIT_ONE_ALTERNATE_READ_THEN_YIELD",
            "scheduler": "UNCHANGED",
        },
        "video_stall": {
            "action": "PLAY_ONCE_OR_REJECT_VIEW_ROTATE",
            "qualified_view": False,
        },
        "search_empty_shell": {
            "action": "NATIVE_SEARCH_ONCE_THEN_ROTATE_QUERY_ROUTE",
            "mission_block": False,
        },
        "dismissible_overlay": {
            "action": "CLOSE_ONCE_NO_CONSENT_OR_APP_OPEN_THEN_REREAD",
            "mission_block": False,
        },
        "consent_or_terms_choice": {
            "action": "SKIP_ROUTE_NEVER_CHOOSE_DURABLE_CONSENT",
            "mission_block": False,
        },
        "gated_content": {
            "action": "SKIP_CANDIDATE_NO_BYPASS",
            "mission_block": False,
        },
        "unavailable_content": {
            "action": "TERMINAL_CANDIDATE_SKIP_NO_RELOAD_LOOP",
            "mission_block": False,
        },
        "persistent_captcha": {
            "action": "HUMAN_REPAIR_PENDING_ASK_ONCE_READ_ONLY_RECHECK",
            "mutation_retry": False,
            "scheduler": "UNCHANGED",
        },
        "callback_delivery_unknown": {
            "action": "STORE_BYTES_HASH_IDLE_NO_BLIND_RESEND",
            "scheduler": "UNCHANGED",
        },
        "dispatch_uncertain": {
            "action": "NO_RESEND_WAIT_EXACT_EVIDENCE",
            "scheduler": "UNCHANGED",
        },
        "cutoff": {
            "action": "STOP_TIKTOK_REQUEST_RELEASE_KEEP_CLEANUP_WAKE",
        },
        "cleanup_expired_unreleased": {
            "action": "RELEASE_UNCERTAIN_DELETE_TIMER_NO_ARCHIVE",
        },
    }[event]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, raw in enumerate(path.read_text().splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise AssertionError(f"invalid JSONL line {line_no}: {exc}") from exc
        assert isinstance(value, dict), f"line {line_no} is not an object"
        rows.append(value)
    return rows


def validate_runtime_ledger(path: Path) -> dict[str, int]:
    rows = load_jsonl(path)
    intents: set[str] = set()
    frozen: set[str] = set()
    recoveries = 0
    for index, row in enumerate(rows, start=1):
        if row.get("schema") == "browser_recovery/v1":
            recoveries += 1
            required = (
                "run_id", "round_id", "round_seq", "boundary_seq",
                "retry_epoch", "phase", "error_class",
                "failed_url", "failure_stage", "submission_certainty",
                "tiktok_probe", "neutral_probe", "account_probe",
                "expected_account_handle", "observed_account_handle",
                "account_proof_surface",
                "next_retry_not_before_utc",
            )
            missing = [key for key in required if key not in row]
            assert not missing, f"recovery row {index} missing {missing}"
            assert isinstance(row["retry_epoch"], int) and row["retry_epoch"] >= 1
            if row["phase"] in ("RECOVERY_PENDING", "HUMAN_REPAIR_PENDING"):
                assert row["next_retry_not_before_utc"], (
                    f"pending recovery row {index} lacks next retry time"
                )
            assert row["account_proof_surface"] in (
                "profile_link", "profile_heading", "account_menu", "none"
            )
            if row["account_probe"] == "MATCH":
                assert row["expected_account_handle"] == row["observed_account_handle"]
                assert row["account_proof_surface"] != "none"
            if row["account_probe"] == "MISMATCH":
                assert row["expected_account_handle"]
                assert row["observed_account_handle"]
                assert row["expected_account_handle"] != row["observed_account_handle"]
            if row["submission_certainty"] == "UNKNOWN_AFTER_TIMEOUT":
                assert row.get("action_key"), f"uncertain row {index} lacks action_key"
                frozen.add(row["action_key"])

        event = row.get("event")
        action_key = row.get("action_key")
        if event == "MUTATION_INTENT":
            assert action_key, f"intent row {index} lacks action_key"
            assert action_key not in intents, f"duplicate mutation intent {action_key}"
            assert action_key not in frozen, f"frozen mutation retried {action_key}"
            intents.add(action_key)
        elif event == "MUTATION_UNKNOWN":
            assert action_key in intents, f"unknown mutation lacks prior intent {action_key}"
            frozen.add(action_key)
        elif event in ("MUTATION_ATTEMPTED", "MUTATION_HARD_BLOCKED"):
            assert action_key in intents, f"mutation result lacks prior intent {action_key}"
            assert action_key not in frozen, f"frozen mutation has later result {action_key}"

    return {"rows": len(rows), "recoveries": recoveries,
            "mutation_intents": len(intents), "frozen_action_keys": len(frozen)}


def validate_contract() -> dict[str, dict[str, Any]]:
    missing_files = [str(path) for path in DOCS if not path.is_file()]
    assert not missing_files, missing_files
    joined = "\n".join(path.read_text() for path in DOCS)
    required_terms = (
        "one bounded recovery pass per active executor turn",
        "cross-wake retry",
        "Chrome health as five separate layers",
        "CHROME_CONTENT_CHANNEL_TIMEOUT",
        "content/navigation channel",
        "potentially blocking browser action",
        "After a navigation timeout",
        "Promise.race",
        "120 seconds",
        "BROWSER_USE_DISABLE_AMBIENT_NETWORK=1",
        "visible `textarea[name=q][placeholder=\"Find anything\"]`",
        "hidden `input[name=q]`",
        "Meta+A",
        "Backspace",
        "minimal snapshot or locator projection",
        "Model switching is not Chrome recovery",
        "empty tab list",
        "explicit browser-disconnected",
        "READ_ONLY",
        "UNKNOWN_AFTER_TIMEOUT",
        "SUBMISSION_UNCERTAIN",
        "MUTATION_UNKNOWN",
        "MUTATION_INTENT",
        "action_key",
        "ROUND_YIELDED",
        "RECOVERY_PENDING",
        "RECOVERY_FIRST",
        "boundary_seq",
        "expected_account_handle",
        "observed_account_handle",
        "account_proof_surface",
        "consent or terms choice",
        "gated content",
        "unavailable content",
        "Labels may be localized",
        "retry_epoch",
        "next_retry_not_before_utc",
        "CALLBACK_DELIVERY_UNKNOWN",
        "DISPATCH_UNCERTAIN",
        "keep the finite cleanup wake",
        "RELEASE_UNCERTAIN",
        "do not archive",
    )
    absent = [term for term in required_terms if term.lower() not in joined.lower()]
    assert not absent, f"missing persistent recovery terms: {absent}"

    events = (
        "empty_tab_list", "stale_tab", "browser_disconnected",
        "metadata_healthy_neutral_goto_timeout", "navigation_timeout_loaded",
        "visible_textarea_hidden_input", "react_fill_empty_state_not_cleared",
        "one_boundary_action_per_call",
        "read_only_tool_timeout", "mutation_tool_timeout",
        "dns_or_network_persistent", "http_403_target_only", "http_429",
        "http_429_no_retry_after", "http_5xx", "blocked_by_client",
        "blank_or_delayed_hydration", "video_stall", "search_empty_shell",
        "dismissible_overlay", "consent_or_terms_choice", "gated_content",
        "unavailable_content", "persistent_captcha",
        "callback_delivery_unknown", "dispatch_uncertain", "cutoff",
        "cleanup_expired_unreleased",
    )
    scenarios = {event: recover(event) for event in events}
    for event in (
        "empty_tab_list", "stale_tab", "browser_disconnected",
        "metadata_healthy_neutral_goto_timeout", "navigation_timeout_loaded",
        "read_only_tool_timeout", "mutation_tool_timeout",
        "dns_or_network_persistent", "http_403_target_only", "http_429",
        "http_429_no_retry_after", "http_5xx", "blocked_by_client",
        "blank_or_delayed_hydration",
    ):
        scenario = scenarios[event]
        if "scheduler" in scenario:
            assert scenario["scheduler"] == "UNCHANGED"
    assert scenarios["empty_tab_list"]["action"].endswith("KEEP_BROWSER_BINDING")
    assert scenarios["stale_tab"]["action"].startswith("DISCARD_TAB_BINDING")
    assert scenarios["browser_disconnected"]["binding_invalidated"] == "BROWSER"
    assert scenarios["metadata_healthy_neutral_goto_timeout"]["error_class"] == (
        "CHROME_CONTENT_CHANNEL_TIMEOUT"
    )
    assert "CHROME_DISCONNECTED" in scenarios[
        "metadata_healthy_neutral_goto_timeout"
    ]["not_classes"]
    assert scenarios["navigation_timeout_loaded"]["repeat_navigation"] is False
    assert scenarios["visible_textarea_hidden_input"]["hidden_selector_rejected"] == (
        "input[name=q]"
    )
    assert scenarios["react_fill_empty_state_not_cleared"]["fill_empty_sufficient"] is False
    assert scenarios["one_boundary_action_per_call"]["observed_outer_budget_seconds"] == 120
    assert scenarios["one_boundary_action_per_call"]["outer_budget"].startswith("CONFIGURABLE")
    assert scenarios["mutation_tool_timeout"]["mutation_retry"] is False
    assert scenarios["mutation_tool_timeout"]["reopen_for_verification"] is False
    assert scenarios["dns_or_network_persistent"]["next_assignment"] == "RECOVERY_FIRST"
    assert scenarios["http_403_target_only"]["human_question"] is False
    assert scenarios["http_429_no_retry_after"]["action"].startswith("WAIT_UNTIL_NEXT_15M")
    assert scenarios["video_stall"]["qualified_view"] is False
    assert scenarios["search_empty_shell"]["mission_block"] is False
    assert scenarios["dismissible_overlay"]["mission_block"] is False
    assert scenarios["consent_or_terms_choice"]["action"].endswith("CONSENT")
    assert scenarios["gated_content"]["action"].endswith("NO_BYPASS")
    assert scenarios["unavailable_content"]["action"].endswith("NO_RELOAD_LOOP")
    assert scenarios["persistent_captcha"]["scheduler"] == "UNCHANGED"
    assert scenarios["callback_delivery_unknown"]["action"].endswith("NO_BLIND_RESEND")
    assert scenarios["dispatch_uncertain"]["action"].startswith("NO_RESEND")
    assert scenarios["cleanup_expired_unreleased"]["action"].endswith("NO_ARCHIVE")
    return scenarios


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path)
    args = parser.parse_args()
    scenarios = validate_contract()
    result: dict[str, Any] = {"status": "PASS", "scenarios": scenarios}
    if args.ledger:
        result["ledger"] = validate_runtime_ledger(args.ledger)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
