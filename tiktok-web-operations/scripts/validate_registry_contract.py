#!/usr/bin/env python3
"""Validate canonical one-way executor assignment."""
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
    assert all(p.is_file() for p in FILES)
    joined = "\n".join(p.read_text() for p in FILES)
    required = ("executor_bootstrap/v1", "executor_assignment/v1", "canonical", "sort_keys=True",
                "separators=(\",\", \":\")", "assignment_id", "executor_thread_id",
                "direction_ref", "authority_ref", "mission_ref", "NO_CALLBACK_NO_SUPERVISION",
                "gpt-5.6-luna", "thinking\":\"high")
    missing = [x for x in required if x not in joined]
    assert not missing, missing
    assignment = {"schema":"executor_assignment/v1","assignment_id":"a","run_id":"r",
                  "executor_thread_id":"e","role":"TIKTOK_EXECUTOR",
                  "execution_profile":{"model":"gpt-5.6-luna","thinking":"high"},
                  "direction_ref":{"id":"d","version":1,"sha256":"1"*64},
                  "authority_ref":{"id":"a","version":1,"sha256":"2"*64},
                  "mission_ref":{"id":"m","version":1,"sha256":"3"*64},
                  "launcher_contact_policy":"NO_CALLBACK_NO_SUPERVISION"}
    reordered = dict(reversed(list(assignment.items())))
    assert canonical(assignment) == canonical(reordered)
    digest = hashlib.sha256(canonical(assignment)).hexdigest()
    assert len(digest) == 64
    wrong = dict(assignment); wrong["executor_thread_id"] = "other"
    assert hashlib.sha256(canonical(wrong)).hexdigest() != digest
    print(json.dumps({"status":"PASS","assignment_sha256":digest,
                      "scenarios":{"key_order_invariant":True,"exact_executor_required":True,
                                   "no_callback_fields":True}}, sort_keys=True))

if __name__ == "__main__": main()
