#!/usr/bin/env python3
"""Validate Raw-bootstrap versus codeload bundle version authority."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT.parent
README = BUNDLE / "README.md"
VERSION_REFERENCE = ROOT / "references/version-management.md"
DISTRIBUTION_REFERENCE = ROOT / "references/distribution-and-upgrades.md"
MANIFESTS = (
    ROOT / "manifest.json",
    BUNDLE / "thread-supervisor/manifest.json",
)
VERSION_PATTERN = re.compile(r"Protocol version: `([0-9]{4}\.[0-9]{2}\.[0-9]{2}\.[0-9]+)`")


def decide(
    raw_version: str,
    archive_readme_version: str,
    archive_manifest_versions: tuple[str, str],
) -> dict[str, object]:
    archive_versions = (archive_readme_version,) + archive_manifest_versions
    if len(set(archive_versions)) != 1:
        return {
            "status": "ARCHIVE_VERSION_MISMATCH",
            "install_allowed": False,
            "authority": "ARCHIVE_INTERNAL_VERSION_LOCK",
        }
    if raw_version != archive_readme_version:
        return {
            "status": "RAW_README_VERSION_DRIFT",
            "install_allowed": True,
            "authority": "CODELOAD_ARCHIVE",
        }
    return {
        "status": "VERSION_LOCKED",
        "install_allowed": True,
        "authority": "CODELOAD_ARCHIVE",
    }


def main() -> None:
    files = (VERSION_REFERENCE, DISTRIBUTION_REFERENCE) + MANIFESTS
    assert all(path.is_file() for path in files), [
        str(path) for path in files if not path.is_file()
    ]

    manifest_versions = tuple(
        json.loads(path.read_text())["version"] for path in MANIFESTS
    )
    assert len(set(manifest_versions)) == 1
    if README.is_file():
        readme_match = VERSION_PATTERN.search(README.read_text())
        assert readme_match is not None
        archive_readme_version = readme_match.group(1)
        assert manifest_versions == (
            archive_readme_version,
            archive_readme_version,
        )
        context = "REPOSITORY_BUNDLE"
    else:
        archive_readme_version = manifest_versions[0]
        context = "INSTALLED_SKILLS"

    contract = "\n".join(
        path.read_text()
        for path in (VERSION_REFERENCE, DISTRIBUTION_REFERENCE, README)
        if path.is_file()
    )
    required = (
        "RAW_README_VERSION_DRIFT",
        "bootstrap guidance",
        "codeload",
        "root README inside that same extracted archive",
        "Raw drift alone",
        "archive-internal disagreement blocks",
    )
    absent = [term for term in required if term.lower() not in contract.lower()]
    assert not absent, absent

    stale_raw = decide(
        "2026.07.20.1",
        archive_readme_version,
        manifest_versions,
    )
    matching_raw = decide(
        archive_readme_version,
        archive_readme_version,
        manifest_versions,
    )
    internal_mismatch = decide(
        archive_readme_version,
        archive_readme_version,
        (archive_readme_version, "2099.01.01.1"),
    )
    assert stale_raw == {
        "status": "RAW_README_VERSION_DRIFT",
        "install_allowed": True,
        "authority": "CODELOAD_ARCHIVE",
    }
    assert matching_raw["status"] == "VERSION_LOCKED"
    assert matching_raw["install_allowed"] is True
    assert internal_mismatch["status"] == "ARCHIVE_VERSION_MISMATCH"
    assert internal_mismatch["install_allowed"] is False

    print(json.dumps({
        "status": "PASS",
        "context": context,
        "archive_version": archive_readme_version,
        "stale_raw": stale_raw,
        "matching_raw": matching_raw,
        "internal_mismatch": internal_mismatch,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
