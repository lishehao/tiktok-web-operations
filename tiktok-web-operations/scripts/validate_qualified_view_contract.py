#!/usr/bin/env python3
"""Validate STRICT_QUALIFIED_VIEW_V2 wording and duration-gate scenarios."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
FILES = (
    BUNDLE / "README.md",
    ROOT / "SKILL.md",
    ROOT / "references/qualified-view-contract.md",
    ROOT / "references/persistent-feed-operations.md",
    ROOT / "references/feed-browsing-and-comments.md",
    ROOT / "references/operating-model.md",
    BUNDLE / "thread-supervisor/references/tiktok-coordinator-worker.md",
)


def required_watch_seconds(duration_seconds):
    if duration_seconds is None:
        return 15
    duration = float(duration_seconds)
    if duration <= 0:
        raise ValueError("duration must be positive")
    if duration <= 15:
        return math.ceil(duration * 0.80)
    if duration <= 60:
        return math.ceil(max(10, duration * 0.40))
    return math.ceil(min(45, max(20, duration * 0.25)))


def decide(*, core, stable_identity, observations, continuous_watch,
           duration, premise, payoff, source_proof=True, content_changes=0,
           duplicate=False, load_complete=True):
    if not stable_identity or not source_proof or duplicate or not load_complete:
        return "OPENED_ONLY"
    if not core:
        return "CLASSIFIED_SAMPLE"
    required = required_watch_seconds(duration)
    unknown_duration_ok = duration is not None or content_changes >= 2
    if observations < 2 or continuous_watch < required or not unknown_duration_ok:
        return "CLASSIFIED_SAMPLE"
    if not premise or not payoff:
        return "CLASSIFIED_SAMPLE"
    return "QUALIFIED_VIEW"


def main():
    missing_files = [
        str(path) for path in FILES
        if not path.is_file() and path.name != "README.md"
    ]
    assert not missing_files, missing_files
    joined = " ".join(
        "\n".join(path.read_text() for path in FILES if path.is_file()).split()
    )
    required_phrases = (
        "STRICT_QUALIFIED_VIEW_V2",
        "multiple forward playback observations",
        "continuous watch",
        "80%",
        "40%",
        "25%",
        "capped at 45 seconds",
        "premise",
        "payoff",
        "classified_sample",
        "sampled",
        "one-second autoplay",
        "action attempt",
    )
    missing = [phrase for phrase in required_phrases if phrase.lower() not in joined.lower()]
    assert not missing, missing

    floors = {str(d): required_watch_seconds(d) for d in (5, 10, 15, 16, 30, 45, 60, 61, 125, 600)}
    assert floors == {
        "5": 4, "10": 8, "15": 12, "16": 10, "30": 12,
        "45": 18, "60": 24, "61": 20, "125": 32, "600": 45,
    }
    scenarios = {
        "one_second_long_video": decide(core=True, stable_identity=True, observations=2,
                                         continuous_watch=1, duration=125,
                                         premise=True, payoff=True),
        "short_near_complete": decide(core=True, stable_identity=True, observations=2,
                                        continuous_watch=8, duration=10,
                                        premise=True, payoff=True),
        "medium_floor_pass": decide(core=True, stable_identity=True, observations=3,
                                     continuous_watch=18, duration=45,
                                     premise=True, payoff=True),
        "time_without_payoff": decide(core=True, stable_identity=True, observations=3,
                                       continuous_watch=24, duration=60,
                                       premise=True, payoff=False),
        "drift_sample": decide(core=False, stable_identity=True, observations=2,
                                continuous_watch=2, duration=30,
                                premise=True, payoff=False),
        "unknown_duration_pass": decide(core=True, stable_identity=True, observations=3,
                                         continuous_watch=15, duration=None,
                                         premise=True, payoff=True, content_changes=2),
        "duplicate": decide(core=True, stable_identity=True, observations=3,
                             continuous_watch=20, duration=30,
                             premise=True, payoff=True, duplicate=True),
    }
    assert scenarios["one_second_long_video"] == "CLASSIFIED_SAMPLE"
    assert scenarios["short_near_complete"] == "QUALIFIED_VIEW"
    assert scenarios["medium_floor_pass"] == "QUALIFIED_VIEW"
    assert scenarios["time_without_payoff"] == "CLASSIFIED_SAMPLE"
    assert scenarios["drift_sample"] == "CLASSIFIED_SAMPLE"
    assert scenarios["unknown_duration_pass"] == "QUALIFIED_VIEW"
    assert scenarios["duplicate"] == "OPENED_ONLY"
    print(json.dumps({"status": "PASS", "contract": "STRICT_QUALIFIED_VIEW_V2",
                      "floors": floors, "scenarios": scenarios}, sort_keys=True))


if __name__ == "__main__":
    main()
