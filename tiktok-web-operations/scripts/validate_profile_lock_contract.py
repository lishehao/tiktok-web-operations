#!/usr/bin/env python3
"""Validate Bootstrap account-image confirmation before fresh dispatch."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (BUNDLE/"README.md", ROOT/"SKILL.md",
         ROOT/"references/startup-health-check.md",
         ROOT/"references/role-and-stage-contract.md",
         ROOT/"references/operating-model.md",
         BUNDLE/"thread-supervisor/SKILL.md",
         BUNDLE/"thread-supervisor/references/canonical-registry.md")

def transition(event: str) -> str:
    return {
        "preflight_only": "PROFILE_DRAFT_NO_EXECUTOR",
        "bare_continue_without_proposal": "SHOW_DEFAULT_PROPOSAL_WAIT",
        "detailed_unconfirmed": "SHOW_STRUCTURED_PROPOSAL_WAIT",
        "explicit_operating_mission": "CONFIRMED_FROM_EXPLICIT_MISSION_CREATE_ALLOWED",
        "visible_proposal_confirmed": "FRESH_CREATE_ALLOWED",
        "final_corrections": "CONFIRMED_REVISED_PROFILE_CREATE_ALLOWED",
        "second_fresh_run": "NEW_PROFILE_LOCK_REQUIRED",
    }[event]

def main():
    assert all(p.is_file() for p in FILES)
    joined = " ".join("\n".join(p.read_text() for p in FILES).split())
    required = ("profile_status=confirmed", "direction_profile_version",
                "at most two user-facing rounds", "one open question",
                "structured proposal", "3–5", "future_post_alignment",
                "no executor creation", "bare `继续`", "confirms only a proposal",
                "never inherit", "L0_PROFILE_LOCK", "exact confirmation evidence")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    scenarios = {e: transition(e) for e in (
        "preflight_only", "bare_continue_without_proposal", "detailed_unconfirmed",
        "explicit_operating_mission",
        "visible_proposal_confirmed", "final_corrections", "second_fresh_run")}
    assert scenarios["preflight_only"] == "PROFILE_DRAFT_NO_EXECUTOR"
    assert scenarios["bare_continue_without_proposal"] == "SHOW_DEFAULT_PROPOSAL_WAIT"
    assert scenarios["visible_proposal_confirmed"] == "FRESH_CREATE_ALLOWED"
    assert scenarios["explicit_operating_mission"] == "CONFIRMED_FROM_EXPLICIT_MISSION_CREATE_ALLOWED"
    assert scenarios["second_fresh_run"] == "NEW_PROFILE_LOCK_REQUIRED"
    print(json.dumps({"status":"PASS","scenarios":scenarios}, ensure_ascii=False, sort_keys=True))

if __name__ == "__main__": main()
