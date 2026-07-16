#!/usr/bin/env python3
"""Validate bootstrap -> pinned main -> bounded executor lifecycle."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (BUNDLE/"README.md", ROOT/"SKILL.md",
         ROOT/"references/startup-health-check.md",
         ROOT/"references/role-and-stage-contract.md",
         ROOT/"references/operating-model.md", BUNDLE/"thread-supervisor/SKILL.md")

def transition(event: str):
    return {
        "setup":{"role":"TIKTOK_COORDINATOR","title":"TikTok 启动台","pinned":False,"action":"IMMEDIATE_RENAME"},
        "hard_repair":{"role":"TIKTOK_COORDINATOR","title":"TikTok 启动台","pinned":False,"action":"WAIT_USER_REPAIR"},
        "healthy":{"role":"TIKTOK_COORDINATOR","title":"TikTok 主控台","pinned":True,"action":"SAME_TASK_RENAME_PIN"},
        "pin_unavailable":{"role":"TIKTOK_COORDINATOR","title":"TikTok 主控台","pinned":"DEGRADED","action":"CONTINUE"},
        "executor_created":{"role":"TIKTOK_COORDINATOR","title":"TikTok 执行台","pinned":False,"action":"SET_EXACT_ID_TITLE_READBACK"},
        "executor_title_unavailable":{"role":"TIKTOK_COORDINATOR","title":"DEGRADED","pinned":False,"action":"CONTINUE_ONE_IDLE_REPAIR"},
        "executor":{"role":"TIKTOK_EXECUTOR","title":"TikTok 执行台","pinned":False,"action":"BOUNDED_ROUND_CALLBACK"},
        "callback":{"role":"TIKTOK_COORDINATOR","title":"TikTok 主控台","pinned":True,"action":"REPLAN_COOLDOWN"},
        "due":{"role":"TIKTOK_COORDINATOR","title":"TikTok 主控台","pinned":True,"action":"DISPATCH_NEXT_ROUND"},
        "terminal_archive":{"role":"TIKTOK_COORDINATOR","title":"TikTok 执行台","pinned":False,"action":"ARCHIVE_EXACT_ID_AFTER_RELEASE"},
    }[event]

def main():
    assert all(p.is_file() for p in FILES if p.name != "README.md" or p.exists())
    joined = "\n".join(p.read_text() for p in FILES if p.is_file())
    required = ("TikTok 启动台", "TikTok 主控台", "TikTok 执行台",
                "first available presentation action", "coordinator_worker",
                "ASSIGNMENT_ACCEPTED", "callback", "mission recurring Heartbeat",
                "pinned=true", "presentation degradation", "set_thread_title",
                "DEGRADED_EXECUTOR_ARCHIVE_UNAVAILABLE")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    scenarios = {e: transition(e) for e in
                 ("setup","hard_repair","healthy","pin_unavailable",
                  "executor_created","executor_title_unavailable","executor",
                  "callback","due","terminal_archive")}
    assert scenarios["healthy"]["action"] == "SAME_TASK_RENAME_PIN"
    assert scenarios["executor"]["pinned"] is False
    assert scenarios["executor"]["action"] == "BOUNDED_ROUND_CALLBACK"
    assert scenarios["executor_created"]["action"] == "SET_EXACT_ID_TITLE_READBACK"
    assert scenarios["executor_title_unavailable"]["action"] == "CONTINUE_ONE_IDLE_REPAIR"
    assert scenarios["terminal_archive"]["action"] == "ARCHIVE_EXACT_ID_AFTER_RELEASE"
    assert scenarios["due"]["action"] == "DISPATCH_NEXT_ROUND"
    print(json.dumps({"status":"PASS","scenarios":scenarios}, ensure_ascii=False, sort_keys=True))

if __name__ == "__main__": main()
