#!/usr/bin/env python3
"""Validate canonical registry semantics and isolated forward scenarios."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


TIKTOK_SKILL = Path(__file__).resolve().parents[1]
BUNDLE_CONTAINER = TIKTOK_SKILL.parent
CANONICAL = BUNDLE_CONTAINER / "thread-supervisor/references/canonical-registry.md"
IDENTITY = BUNDLE_CONTAINER / "thread-supervisor/references/identity-and-automation.md"
SUPERVISOR_SKILL = BUNDLE_CONTAINER / "thread-supervisor/SKILL.md"
TIKTOK_MAIN = TIKTOK_SKILL / "SKILL.md"
OPERATING = TIKTOK_SKILL / "references/operating-model.md"
STARTUP = TIKTOK_SKILL / "references/startup-health-check.md"
STABILITY = TIKTOK_SKILL / "references/stability-and-circuit-breakers.md"
README = BUNDLE_CONTAINER / "README.md"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def ref_for(value: dict[str, Any], *, object_id: str, schema: str, version: int) -> dict[str, Any]:
    return {
        "id": object_id,
        "schema": schema,
        "sha256": hashlib.sha256(canonical_bytes(value)).hexdigest(),
        "version": version,
    }


def registry_gate(
    *, stored_ref: dict[str, Any], self_registry_ref: dict[str, Any], dispatch_ref: dict[str, Any]
) -> str:
    if stored_ref != self_registry_ref:
        return "REGISTRY_RECONCILIATION_REQUIRED"
    if dispatch_ref != stored_ref:
        return "REGISTRY_RECONCILIATION_REQUIRED"
    return "SMOKE_ALLOWED"


def validate_profile(registry: dict[str, Any]) -> str:
    expected = {"model": "gpt-5.6-luna", "thinking": "high"}
    return (
        "PROFILE_ACCEPTED"
        if registry.get("execution_profile") == expected
        else "REGISTRY_PROFILE_MISMATCH"
    )


def main() -> None:
    paths = (
        CANONICAL,
        IDENTITY,
        SUPERVISOR_SKILL,
        TIKTOK_MAIN,
        OPERATING,
        STARTUP,
        STABILITY,
    )
    missing_paths = [str(path) for path in paths if not path.is_file()]
    assert not missing_paths, f"missing contract files: {missing_paths}"
    documents = [path.read_text() for path in paths]
    if README.exists():
        documents.append(README.read_text())
    joined = "\n".join(documents)

    required_terms = (
        "thread_bootstrap/v1",
        "thread_identity_registry/v1",
        "canonical UTF-8 JSON",
        "sort_keys=True",
        "separators=(\",\", \":\")",
        "registry_id",
        "registry_generation",
        "registry_ref",
        "direction_ref",
        "authority_ref",
        "mission_ref",
        "TIKTOK_COORDINATOR",
        "TIKTOK_EXECUTOR",
        "REGISTRY_RECONCILIATION",
        "REGISTRY_BOOTSTRAP_CONTAMINATION",
        "ORCHESTRATION_REGISTRY_BLOCKER",
        "at most one clean replacement",
        "gpt-5.6-luna",
        "thinking\":\"high",
    )
    missing_terms = [term for term in required_terms if term not in joined]
    assert not missing_terms, f"missing semantic assertions: {missing_terms}"

    forbidden = (
        "initial prompt includes the coordinator ID,\n   account, envelope, ledger",
        "Include\n   both IDs, account, ledger, authority, role, and stop time byte-for-byte",
        "mutation authorization, role, model, and thinking as immutable registry fields",
    )
    present_forbidden = [term for term in forbidden if term in joined]
    assert not present_forbidden, f"stale registry rules remain: {present_forbidden}"

    base_registry = {
        "schema": "thread_identity_registry/v1",
        "registry_id": "reg-test",
        "registry_generation": 1,
        "run_id": "run-test",
        "run_nonce": "nonce-test",
        "account": {"platform": "tiktok", "handle": "@shehaolili"},
        "coordinator": {
            "thread_id": "coordinator-id",
            "host_id": "local",
            "role_code": "TIKTOK_COORDINATOR",
        },
        "executor": {
            "thread_id": "executor-id",
            "host_id": "local",
            "role_code": "TIKTOK_EXECUTOR",
            "generation": 1,
        },
        "execution_profile": {"model": "gpt-5.6-luna", "thinking": "high"},
        "ledger_path": "/tmp/tiktok-ledger.jsonl",
        "callback_target_thread_id": "coordinator-id",
        "automation_manager_thread_id": "coordinator-id",
        "dedicated_tab_policy": "EXECUTOR_OWNED_TAB_PER_BLOCK",
        "writer_policy": "EXECUTOR_SOLE_RUN_LEDGER_AND_MUTATION_WRITER",
    }

    reordered_registry = dict(reversed(list(base_registry.items())))
    assert canonical_bytes(base_registry) == canonical_bytes(reordered_registry)
    registry_ref = ref_for(
        base_registry,
        object_id="reg-test",
        schema="thread_identity_registry/v1",
        version=1,
    )
    assert len(registry_ref["sha256"]) == 64
    assert validate_profile(base_registry) == "PROFILE_ACCEPTED"

    wrong_profile = dict(base_registry)
    wrong_profile["execution_profile"] = {"model": "gpt-5.6", "thinking": "high"}
    assert validate_profile(wrong_profile) == "REGISTRY_PROFILE_MISMATCH"

    authority_a = {
        "schema": "authority_envelope/v1",
        "version": 1,
        "actions": {"comment": True, "favorite": True, "like": False, "repost": True},
        "comment_max_words": 30,
    }
    authority_reordered = {
        "comment_max_words": 30,
        "actions": {"repost": True, "like": False, "favorite": True, "comment": True},
        "version": 1,
        "schema": "authority_envelope/v1",
    }
    assert canonical_bytes(authority_a) == canonical_bytes(authority_reordered)
    authority_changed = json.loads(json.dumps(authority_a))
    authority_changed["actions"]["like"] = True
    assert hashlib.sha256(canonical_bytes(authority_a)).hexdigest() != hashlib.sha256(
        canonical_bytes(authority_changed)
    ).hexdigest()

    assert (
        registry_gate(
            stored_ref=registry_ref,
            self_registry_ref=registry_ref,
            dispatch_ref=registry_ref,
        )
        == "SMOKE_ALLOWED"
    )
    bad_ref = dict(registry_ref)
    bad_ref["sha256"] = "0" * 64
    assert (
        registry_gate(
            stored_ref=registry_ref,
            self_registry_ref=bad_ref,
            dispatch_ref=registry_ref,
        )
        == "REGISTRY_RECONCILIATION_REQUIRED"
    )
    assert (
        registry_gate(
            stored_ref=registry_ref,
            self_registry_ref=registry_ref,
            dispatch_ref=bad_ref,
        )
        == "REGISTRY_RECONCILIATION_REQUIRED"
    )

    result = {
        "status": "PASS",
        "scenarios": {
            "key_order_invariant": True,
            "structured_role_codes": True,
            "authorization_key_order_invariant": True,
            "authorization_value_change_requires_new_version": True,
            "wrong_callback_profile_blocked": True,
            "self_registry_mismatch_reconciles": True,
            "dispatch_ref_mismatch_reconciles": True,
            "exact_reference_allows_smoke": True,
        },
        "registry_sha256": registry_ref["sha256"],
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
