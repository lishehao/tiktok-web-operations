#!/usr/bin/env python3
"""Validate temporary bootstrap title -> pinned reusable distributor."""
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
        "setup": ("TikTok 启动台", False, "PREFLIGHT"),
        "hard_repair": ("TikTok 启动台", False, "WAIT_USER"),
        "healthy": ("TikTok 分发台", True, "READY"),
        "pin_failed": ("TikTok 分发台", "DEGRADED", "READY"),
        "explicit_mission": ("TikTok 分发台", True, "DIRECT_DISPATCH"),
        "profile_needed": ("TikTok 分发台", True, "PROFILE_GATE"),
        "handoff_complete": ("TikTok 分发台", True, "REUSABLE_IDLE"),
        "executor": ("TikTok 执行台", False, "ACTIVE"),
    }[event]

def main():
    assert all(p.is_file() for p in FILES)
    joined = "\n".join(p.read_text() for p in FILES)
    required = ("TikTok 启动台", "TikTok 分发台", "same exact task",
                "attempt to pin", "pinned=true", "presentation degradation",
                "Never pin", "reusable", "explicit start", "L0_DISTRIBUTOR_READY")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    events = ("setup","hard_repair","healthy","pin_failed","explicit_mission",
              "profile_needed","handoff_complete","executor")
    scenarios = {e: state(e) for e in events}
    assert scenarios["healthy"] == ("TikTok 分发台", True, "READY")
    assert scenarios["pin_failed"][2] == "READY"
    assert scenarios["explicit_mission"][2] == "DIRECT_DISPATCH"
    assert scenarios["profile_needed"][0] == "TikTok 分发台"
    assert scenarios["executor"][1] is False
    print(json.dumps({"status":"PASS","scenarios":scenarios}, ensure_ascii=False, sort_keys=True))

if __name__ == "__main__": main()
