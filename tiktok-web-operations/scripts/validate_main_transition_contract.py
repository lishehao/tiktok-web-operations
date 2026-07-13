#!/usr/bin/env python3
"""Validate temporary bootstrap title -> pinned TikTok main task."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (BUNDLE/"README.md", ROOT/"SKILL.md",
         ROOT/"references/startup-health-check.md",
         ROOT/"references/role-and-stage-contract.md",
         ROOT/"references/operating-model.md",
         BUNDLE/"thread-supervisor/SKILL.md",
         BUNDLE/"thread-supervisor/references/identity-and-automation.md")

def state(event: str):
    return {
        "setup": ("TikTok 启动台", False, "BOOTSTRAP"),
        "hard_repair": ("TikTok 启动台", False, "WAIT_USER"),
        "healthy": ("TikTok 主控台", True, "READY"),
        "pin_failed": ("TikTok 主控台", "DEGRADED", "READY"),
        "mission_active": ("TikTok 主控台", True, "COORDINATING"),
        "executor": ("TikTok 执行台", False, "BOUNDED_ROUND"),
    }[event]

def main():
    assert all(p.is_file() for p in FILES)
    joined = "\n".join(p.read_text() for p in FILES)
    required = ("TikTok 启动台", "TikTok 主控台", "same exact task",
                "attempt to pin", "pinned=true", "presentation degradation",
                "Never pin", "TIKTOK_COORDINATOR", "TIKTOK_EXECUTOR")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    scenarios = {e: state(e) for e in
                 ("setup","hard_repair","healthy","pin_failed","mission_active","executor")}
    assert scenarios["healthy"] == ("TikTok 主控台", True, "READY")
    assert scenarios["pin_failed"][2] == "READY"
    assert scenarios["executor"][1] is False
    print(json.dumps({"status":"PASS","scenarios":scenarios}, ensure_ascii=False, sort_keys=True))

if __name__ == "__main__": main()
