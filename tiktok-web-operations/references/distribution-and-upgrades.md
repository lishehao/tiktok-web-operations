# Distribution And Upgrades

Use the installed Skill directory as the normal working source and the public GitHub repository as the canonical distribution source. If a registered TikTok runtime is actively using the installed version, clone that complete version into an isolated release staging directory and edit only the staging copy. Never hot-edit an active installed tree.

## Fixed surfaces

- Installed Skill: `${CODEX_HOME:-$HOME/.codex}/skills/tiktok-web-operations/`
- Public repository: `https://github.com/lishehao/tiktok-web-operations`
- Repository Skill path: `tiktok-web-operations/`
- Machine installer and full operating protocol: repository root `README.md`
- Local shareable Prompt: `~/Downloads/tiktok-web-operations-install-and-use.md`
- Local versioned archive: `~/Downloads/tiktok-web-operations-<version>.zip`
- Version decision protocol: `references/version-management.md`

Keep the public repository root minimal: exactly `README.md` plus the `tiktok-web-operations/` Skill directory. Do not create parallel installer or usage documents.

## Release contract

For every material Skill, reference, agent metadata, installer, or Prompt change:

1. Increment the numeric `YYYY.MM.DD.N` version in `manifest.json`; increment `N` for another release on the same date.
2. Update the root README protocol version to match.
3. Validate the release source with `quick_validate.py` when available and equivalent structural checks otherwise. Normally this is the installed Skill; during an active older runtime it is the isolated release staging copy.
4. Synchronize the complete Skill directory plus the single root README to the public GitHub repository. Never update only the local copy or only GitHub.
5. Keep the local shareable Prompt to the single HTTPS sentence published near the top of the root README. It is only a pointer to install/upgrade, run read-only preflight, and return the guided handoff; all direction, duration, authorization, topology, and operating logic stays in the GitHub README and Skill.
6. Rebuild one latest versioned ZIP from the complete Skill directory and run `unzip -t`. Remove superseded same-day TikTok package ZIPs after the new one passes.
7. Download a fresh public `main` archive from `codeload.github.com` into a new temporary directory. Require exactly one target Skill directory and exactly the two intended repository-root entries, run Skill validation, read back the expected version, compare it with the release source, and confirm the one-sentence local Prompt exactly matches the direct-install sentence in README.
8. Report a release only after source validation, ZIP integrity, GitHub readback, and fresh-archive validation all pass. If the installed Skill remains on an older version because an active runtime is fenced, report `published_version`, `installed_version`, and `upgrade_state=DEFERRED_ACTIVE_RUNTIME`; do not imply the local upgrade already happened.

The consumer-side decision table, lock, fingerprint, force authorization, active-runtime fence, atomic replacement, and rollback rules live only in `version-management.md`; keep README aligned with that protocol instead of creating another installer document.

Consumers install through public HTTPS and do not need Git, GitHub CLI, Python, or a GitHub account. Publisher-side Git or GitHub API is an implementation detail; if local Git is unavailable, use an authenticated GitHub API path and retain the same validation contract.

Do not store credentials, cookies, Chrome profile data, TikTok exports, ledgers, or account-specific private data in the public repository or ZIP.
