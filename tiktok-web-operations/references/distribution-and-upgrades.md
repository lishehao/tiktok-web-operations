# Distribution And Upgrades

Use the installed Skill directory as the working source and the public GitHub repository as the canonical distribution source.

## Fixed surfaces

- Installed Skill: `${CODEX_HOME:-$HOME/.codex}/skills/tiktok-web-operations/`
- Public repository: `https://github.com/lishehao/tiktok-web-operations`
- Repository Skill path: `tiktok-web-operations/`
- Machine installer: repository root `INSTALLER-PROTOCOL.md`
- Shareable Prompt: repository root `INSTALL-AND-USE.md`
- Local shareable Prompt: `~/Downloads/tiktok-web-operations-install-and-use.md`
- Local versioned archive: `~/Downloads/tiktok-web-operations-<version>.zip`

## Release contract

For every material Skill, reference, agent metadata, installer, or Prompt change:

1. Increment the numeric `YYYY.MM.DD.N` version in `manifest.json`; increment `N` for another release on the same date.
2. Update the installer protocol version to match.
3. Validate the installed Skill with `quick_validate.py` when available and equivalent structural checks otherwise.
4. Synchronize the complete Skill directory plus both root distribution documents to the public GitHub repository. Never update only the local copy or only GitHub.
5. Keep the repository and local `INSTALL-AND-USE.md` byte-identical.
6. Rebuild one latest versioned ZIP from the complete Skill directory and run `unzip -t`. Remove superseded same-day TikTok package ZIPs after the new one passes.
7. Download a fresh public `main` archive from `codeload.github.com` into a new temporary directory. Require exactly one target Skill directory, run Skill validation, read back the expected version, compare it with the installed source, and confirm the two-stage Prompt still points to the canonical installer.
8. Report a release only after local validation, ZIP integrity, GitHub readback, and fresh-archive validation all pass.

Consumers install through public HTTPS and do not need Git, GitHub CLI, Python, or a GitHub account. Publisher-side Git or GitHub API is an implementation detail; if local Git is unavailable, use an authenticated GitHub API path and retain the same validation contract.

Do not store credentials, cookies, Chrome profile data, TikTok exports, ledgers, or account-specific private data in the public repository or ZIP.
