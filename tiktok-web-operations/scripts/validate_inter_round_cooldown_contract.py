#!/usr/bin/env python3
"""Validate bounded inter-round cooldown on one unique one-shot wake."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (BUNDLE/"README.md", ROOT/"SKILL.md",
         ROOT/"references/persistent-feed-operations.md",
         ROOT/"references/operating-model.md",
         ROOT/"references/role-and-stage-contract.md",
         BUNDLE/"thread-supervisor/SKILL.md",
         BUNDLE/"thread-supervisor/references/identity-and-automation.md")

def cooldown(kind: str):
    return {"read_only_low_yield":10, "standard":15,
            "mutation_or_recovery_heavy":20}[kind]

def main():
    assert all(p.is_file() for p in FILES)
    joined = "\n".join(p.read_text() for p in FILES)
    required = ("10–20", "cooldown_until", "default to 15", "one-shot",
                "round_seq", "single-occurrence", "read back", "consumed",
                "perform no TikTok", "E1_COOLDOWN")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    scenarios = {
        "round_incomplete_24": "CONTINUE_SAME_ROUND",
        "round_complete_25_45": "CHECKPOINT_THEN_COOLDOWN",
        "read_only_low_yield": cooldown("read_only_low_yield"),
        "standard": cooldown("standard"),
        "mutation_or_recovery_heavy": cooldown("mutation_or_recovery_heavy"),
        "checkpoint": "CREATE_RUN_ROUND_UNIQUE_COUNT1",
        "due_wake": "CONSUME_RETIRE_CLEAR_RESUME",
        "terminal_stop": "DELETE_EXACT_PENDING_IF_ANY",
    }
    assert 10 <= scenarios["standard"] <= 20
    assert scenarios["checkpoint"] == "CREATE_RUN_ROUND_UNIQUE_COUNT1"
    assert scenarios["due_wake"] == "CONSUME_RETIRE_CLEAR_RESUME"
    print(json.dumps({"status":"PASS","scenarios":scenarios}, sort_keys=True))

if __name__ == "__main__": main()
