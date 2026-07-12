#!/usr/bin/env python3
"""Validate the concise novice setup handoff and direct next step."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (BUNDLE/"README.md", ROOT/"SKILL.md",
         ROOT/"references/startup-health-check.md",
         ROOT/"agents/openai.yaml")
EXPECTED = (
    "TikTok 已准备好，当前账号：@handle。",
    "下一步只要告诉我：想把账号做成什么方向，以及运营多久。",
    "例如：“做北美宠物账号，持续 10 小时。”不确定就回复：“用默认设置开始。”",
)

def main():
    assert all(p.is_file() for p in FILES)
    joined = "\n".join(p.read_text() for p in FILES)
    for line in EXPECTED:
        assert line in joined, line
    required = ("three-line novice handoff", "without another confirmation round",
                "用默认设置开始", "direction and optional duration",
                "Do not append architecture")
    missing = [x for x in required if x.lower() not in joined.lower()]
    assert not missing, missing
    scenarios = {
        "successful_setup": "SHOW_EXACT_THREE_LINES",
        "direction_duration_reply": "DIRECT_DISPATCH",
        "default_command": "DIRECT_DEFAULT_DISPATCH",
        "advice_only": "PROFILE_PROPOSAL",
        "hard_repair": "SHOW_ONE_CONCRETE_REPAIR_NOT_HANDOFF",
    }
    print(json.dumps({"status":"PASS","line_count":3,"scenarios":scenarios},
                     ensure_ascii=False, sort_keys=True))

if __name__ == "__main__": main()
