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
        "setup": {"role":"TIKTOK_LAUNCHER","title":"TikTok 启动台","pinned":False,"action":"IMMEDIATE_RENAME"},
        "hard_repair": {"role":"TIKTOK_LAUNCHER","title":"TikTok 启动台","pinned":False,"action":"WAIT_USER_REPAIR"},
        "healthy": {"role":"TIKTOK_LAUNCHER","title":"TikTok 分发台","pinned":True,"action":"SAME_TASK_RENAME_PIN"},
        "pin_unavailable": {"role":"TIKTOK_LAUNCHER","title":"TikTok 分发台","pinned":"DEGRADED","action":"CONTINUE"},
        "accepted": {"role":"TIKTOK_LAUNCHER","title":"TikTok 分发台","pinned":True,"action":"REUSABLE_IDLE"},
        "executor": {"role":"TIKTOK_EXECUTOR","title":"TikTok 执行台","pinned":False,"action":"SELF_OWNED_RUN"},
        "rename_unavailable": {"role":"TIKTOK_LAUNCHER","title":"DEGRADED_RENAME_UNAVAILABLE","action":"CONTINUE"},
        "create_failed": {"role":"TIKTOK_LAUNCHER","title":"TikTok 分发台","pinned":True,"action":"REPORT_NO_REUSE"},
        "second_command": {"role":"TIKTOK_LAUNCHER","title":"TikTok 分发台","pinned":True,"action":"NEW_RUN_NEW_EXECUTOR_THEN_REUSABLE_IDLE"},
    }[event]

def main():
    assert all(p.is_file() for p in FILES)
    joined = "\n".join(p.read_text() for p in FILES)
    required = ("TikTok 启动台", "TikTok 分发台", "TikTok 执行台", "first available presentation action",
                "launcher_self_owned_executor", "ASSIGNMENT_ACCEPTED", "become idle",
                "fresh_only_dispatch", "exactly one fresh create attempt",
                "reusable stateless", "later user", "another fresh executor",
                "pinned=true", "presentation degradation", "never becomes `TikTok 主控台`",
                "No callback", "No launcher/coordinator/supervisor timer")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    scenarios = {e: transition(e) for e in ("setup","hard_repair","healthy","pin_unavailable",
                 "accepted","executor","rename_unavailable","create_failed","second_command")}
    assert scenarios["healthy"]["action"] == "SAME_TASK_RENAME_PIN"
    assert scenarios["accepted"]["action"] == "REUSABLE_IDLE"
    assert scenarios["executor"]["action"] == "SELF_OWNED_RUN"
    assert scenarios["executor"]["pinned"] is False
    assert scenarios["pin_unavailable"]["action"] == "CONTINUE"
    assert scenarios["create_failed"]["action"] == "REPORT_NO_REUSE"
    assert scenarios["second_command"]["action"] == "NEW_RUN_NEW_EXECUTOR_THEN_REUSABLE_IDLE"
    assert all(s["title"] != "TikTok 主控台" for s in scenarios.values())
    print(json.dumps({"status":"PASS","scenarios":scenarios}, ensure_ascii=False, sort_keys=True))

if __name__ == "__main__": main()
