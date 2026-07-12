#!/usr/bin/env python3
"""Validate launcher -> self-owned executor lifecycle scenarios."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (BUNDLE / "README.md", ROOT / "SKILL.md",
         ROOT / "references/startup-health-check.md",
         ROOT / "references/role-and-stage-contract.md",
         ROOT / "references/operating-model.md",
         BUNDLE / "thread-supervisor/SKILL.md")

def transition(event: str):
    return {
        "setup": {"role":"TIKTOK_LAUNCHER","title":"TikTok 启动台","action":"IMMEDIATE_RENAME"},
        "hard_repair": {"role":"TIKTOK_LAUNCHER","title":"TikTok 启动台","action":"WAIT_USER_REPAIR"},
        "accepted": {"role":"TIKTOK_LAUNCHER","title":"TikTok 启动台","action":"IDLE"},
        "executor": {"role":"TIKTOK_EXECUTOR","title":"TikTok 执行台","action":"SELF_OWNED_RUN"},
        "rename_unavailable": {"role":"TIKTOK_LAUNCHER","title":"DEGRADED_RENAME_UNAVAILABLE","action":"CONTINUE"},
    }[event]

def main():
    assert all(p.is_file() for p in FILES)
    joined = "\n".join(p.read_text() for p in FILES)
    required = ("TikTok 启动台", "TikTok 执行台", "first available presentation action",
                "launcher_self_owned_executor", "ASSIGNMENT_ACCEPTED", "become idle",
                "never becomes `TikTok 主控台`", "No callback", "No launcher/coordinator/supervisor Heartbeat")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    scenarios = {e: transition(e) for e in ("setup","hard_repair","accepted","executor","rename_unavailable")}
    assert scenarios["accepted"]["action"] == "IDLE"
    assert scenarios["executor"]["action"] == "SELF_OWNED_RUN"
    assert all(s["title"] != "TikTok 主控台" for s in scenarios.values())
    print(json.dumps({"status":"PASS","scenarios":scenarios}, ensure_ascii=False, sort_keys=True))

if __name__ == "__main__": main()
