# Distribution And Upgrades

Use the installed Skills as the normal working sources and the public GitHub
repository as the canonical bundle source. If a registered TikTok runtime is
actively using the installed version, clone both complete Skills into an
isolated release staging directory and edit only staging. Never hot-edit an
active installed tree.

## Fixed surfaces

- Installed Skills: `${CODEX_HOME:-$HOME/.codex}/skills/thread-supervisor/` and `${CODEX_HOME:-$HOME/.codex}/skills/tiktok-web-operations/`
- Public repository: `https://github.com/lishehao/tiktok-web-operations`
- Repository Skill paths: `thread-supervisor/` and `tiktok-web-operations/`
- Machine installer and full operating protocol: repository root `README.md`
- Local shareable Prompt: `~/Downloads/tiktok-web-operations-install-and-use.md`
- Local versioned archive: `~/Downloads/tiktok-web-operations-<version>.zip`
- Version decision protocol: `references/version-management.md`

Keep the public repository root minimal: exactly `README.md`,
`thread-supervisor/`, and `tiktok-web-operations/`. Do not create parallel
installer or usage documents.

## Release contract

For every material Skill, reference, agent metadata, installer, or Prompt change:

1. Increment the shared numeric `YYYY.MM.DD.N` version in both manifests; increment `N` for another release on the same date.
2. Update the root README protocol version to match.
3. Validate both release Skills with `quick_validate.py` when available and equivalent structural checks otherwise. During an active older runtime use only isolated staging.
4. Synchronize both complete Skill directories plus the single root README to the public GitHub repository. Never update only one Skill, only the local copy, or only GitHub.
5. Keep the local shareable Prompt to the single HTTPS sentence published near the top of the root README. It is only a pointer to install/upgrade, run read-only preflight, and return the guided handoff; all direction, duration, authorization, topology, and operating logic stays in the GitHub README and Skill.
6. Rebuild one latest versioned ZIP from README plus both complete Skills and run `unzip -t`. Remove superseded same-day package ZIPs after the new one passes.
7. Download a fresh public `main` archive from `codeload.github.com` into a new temporary directory. Require exactly the two target Skill directories and three intended repository-root entries, validate both Skills, read back matching versions, compare both trees with release source, and confirm the one-sentence local Prompt exactly matches README.
8. Report a release only after source validation, ZIP integrity, GitHub readback, and fresh-archive validation all pass. If the installed Skill remains on an older version because an active runtime is fenced, report `published_version`, `installed_version`, and `upgrade_state=DEFERRED_ACTIVE_RUNTIME`; do not imply the local upgrade already happened.

The consumer-side decision table, lock, fingerprint, force authorization, active-runtime fence, atomic replacement, and rollback rules live only in `version-management.md`; keep README aligned with that protocol instead of creating another installer document.

Consumers install through public HTTPS and do not need Git, GitHub CLI, Python, or a GitHub account. Publisher-side Git or GitHub API is an implementation detail; if local Git is unavailable, use an authenticated GitHub API path and retain the same validation contract.

Do not store credentials, cookies, Chrome profile data, TikTok exports, ledgers, or account-specific private data in the public repository or ZIP.
